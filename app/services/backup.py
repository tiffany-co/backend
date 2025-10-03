import json
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text, select

from app.db.base import Base
from app.models.audit_log import AuditLog
from app.models.user import user_permission_association
from app.core.exceptions import AppException
from fastapi import status
from app.core.utils import json_serializer

# Define the order for data insertion to respect foreign key constraints.
# Parent tables must come before child tables.
TABLE_ORDER = [
    "user",
    "permission",
    "item",
    "saved_bank_account",
    "user_permission",
    "contact",
    "item_financial_profile",
    "investor",
    "transaction",
    "transaction_item",
    "account_ledger",
    "payment",
    "investment",
    "inventory",
]

class BackupService:
    """Service layer for handling database backup and restore operations."""

    def export_data_as_json_str(self, db: Session) -> str:
        """
        Exports all data from the database (except audit_log) to a JSON string.
        """
        backup_data = {}
        inspector = inspect(db.bind)
        
        # Create a mapping from table names to model classes for efficient lookup
        model_map = {mapper.local_table.name: mapper.class_ for mapper in Base.registry.mappers}
        
        for table_name in inspector.get_table_names():
            if table_name == AuditLog.__tablename__:
                continue

            model = model_map.get(table_name)
            if model:
                records = db.query(model).all()
                backup_data[table_name] = [
                    {c.key: getattr(row, c.key) for c in inspect(row).mapper.column_attrs}
                    for row in records
                ]
                
        # --- Manually Backup the Association Table ---
        stmt = select(user_permission_association)
        result = db.execute(stmt).mappings().all()
        backup_data["user_permission"] = [dict(row) for row in result]
        
        return json.dumps(backup_data, indent=4, default=json_serializer)

    def import_data_from_json_str(self, db: Session, json_str: str):
        """
        Imports data from a JSON string, replacing existing data.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format.")

        # Temporarily disable foreign key constraints for the transaction
        db.execute(text("SET session_replication_role = 'replica';")) # specific for postgres

        try:
            # Clear data from tables in reverse order to handle dependencies
            for table_name in reversed(TABLE_ORDER):
                if table_name in Base.metadata.tables:
                    table = Base.metadata.tables[table_name]
                    db.execute(table.delete())

            # Insert data in the specified order
            for table_name in TABLE_ORDER:
                if table_name in data:
                    table = Base.metadata.tables[table_name]
                    records = data[table_name]
                    if records:
                        db.execute(table.insert(), records)
            
            db.commit()

        except Exception as e:
            db.rollback()
            raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database import failed: {e}")
        finally:
            # Re-enable foreign key constraints
            db.execute(text("SET session_replication_role = 'origin';"))


backup_service = BackupService()
