from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import uuid

from app.repository.base import BaseRepository, CreateSchemaType, UpdateSchemaType
from app.models.transaction import Transaction
from app.models.transaction_item import TransactionItem
from app.models.user import User, UserRole
from app.models.enums.transaction import TransactionType
from app.models.enums.shared import ApprovalStatus

class TransactionRepository(BaseRepository[Transaction, CreateSchemaType, UpdateSchemaType]):
    """
    Repository for Transaction model operations.
    """
    # just used in seed demo
    def get_by_note(self, db: Session, *, note: str) -> Optional[Transaction]:
        """Get a transaction by its note."""
        return db.query(self.model).filter(self.model.note == note).first()
    
    def search(
        self, 
        db: Session, *, 
        current_user: User,
        recorder_id: Optional[uuid.UUID] = None,
        contact_id: Optional[uuid.UUID] = None,
        status: Optional[ApprovalStatus] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        item_title: Optional[str] = None,
        item_id: Optional[uuid.UUID] = None,
        item_transaction_type: Optional[TransactionType] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Transaction]:
        
        query = db.query(self.model)

        # Admin can see all, user can only see their own
        if not current_user.role == UserRole.ADMIN:
            query = query.filter(self.model.recorder_id == current_user.id)
        
        # Filtering on TransactionItem requires a join
        if item_title or item_id or item_transaction_type:
            query = query.join(TransactionItem)

        if recorder_id:
            query = query.filter(self.model.recorder_id == recorder_id)
        if contact_id:
            query = query.filter(self.model.contact_id == contact_id)
        if status:
            query = query.filter(self.model.status == status)
        if start_time:
            query = query.filter(self.model.created_at >= start_time)
        if end_time:
            query = query.filter(self.model.created_at <= end_time)
        
        # Filters on the joined TransactionItem table
        if item_title:
            query = query.filter(TransactionItem.title.ilike(f"%{item_title}%"))
        if item_id:
            query = query.filter(TransactionItem.item_id == item_id)
        if item_transaction_type:
            query = query.filter(TransactionItem.transaction_type == item_transaction_type)

        return query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

    def get_with_items(self, db: Session, id: uuid.UUID) -> Optional[Transaction]:
        return db.query(self.model).options(joinedload(self.model.items)).filter(self.model.id == id).first()

transaction_repo = TransactionRepository(Transaction)

