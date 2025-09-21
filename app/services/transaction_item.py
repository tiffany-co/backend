import uuid
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import status

from app.core.exceptions import AppException
from app.models.user import User
from app.models.transaction_item import TransactionItem
from app.models.enums.transaction import TransactionStatus
from app.repository.transaction_item import transaction_item_repo
from app.schema.transaction_item import TransactionItemCreate, TransactionItemUpdate
from app.services.transaction import transaction_service

class TransactionItemService:

    def get_item_by_id(self, db: Session, *, item_id: uuid.UUID, current_user: User) -> TransactionItem:
        item = transaction_item_repo.get(db, id=item_id)
        if not item:
            raise AppException(status.HTTP_404_NOT_FOUND, "Transaction item not found.")
        
        # Piggyback on transaction service to check permissions
        transaction_service.get_transaction_by_id(db, transaction_id=item.transaction_id, current_user=current_user)
        return item

    def create_item(self, db: Session, *, item_in: TransactionItemCreate, current_user: User) -> TransactionItem:
        transaction = transaction_service.get_transaction_by_id(db, transaction_id=item_in.transaction_id, current_user=current_user, with_items=True)
        if transaction.status != TransactionStatus.DRAFT:
            raise AppException(status.HTTP_400_BAD_REQUEST, "Items can only be added to transactions in 'draft' status.")
        
        create_data = item_in.model_dump()
        create_data["total_price"] = self._calculate_item_total_price(item_in)
        
        new_item = transaction_item_repo.create(db, obj_in=create_data)
        transaction_service._recalculate_total_price(db, transaction=transaction)
        return new_item

    def update_item(self, db: Session, *, item_id: uuid.UUID, item_in: TransactionItemUpdate, current_user: User) -> TransactionItem:
        item_to_update = self.get_item_by_id(db, item_id=item_id, current_user=current_user)
        
        transaction = item_to_update.transaction
        if transaction.status != TransactionStatus.DRAFT:
            raise AppException(status.HTTP_400_BAD_REQUEST, "Items can only be updated if the transaction is in 'draft' status.")
        
        updated_item = transaction_item_repo.update(db, db_obj=item_to_update, obj_in=item_in)
        
        # Recalculate total price if relevant fields changed
        update_data = item_in.model_dump(exclude_unset=True)
        recalc_fields = {'unit_price', 'weight_count', 'ojrat', 'profit', 'tax'}
        if any(field in update_data for field in recalc_fields):
            updated_item.total_price = self._calculate_item_total_price(updated_item)
            db.commit()
            db.refresh(updated_item)
            
        transaction_service._recalculate_total_price(db, transaction=transaction)
        return updated_item
        
    def delete_item(self, db: Session, *, item_id: uuid.UUID, current_user: User) -> TransactionItem:
        item_to_delete = self.get_item_by_id(db, item_id=item_id, current_user=current_user)
        
        transaction = item_to_delete.transaction
        if transaction.status != TransactionStatus.DRAFT:
            raise AppException(status.HTTP_400_BAD_REQUEST, "Items can only be deleted if the transaction is in 'draft' status.")
            
        deleted_item = transaction_item_repo.remove(db, id=item_id)
        transaction_service._recalculate_total_price(db, transaction=transaction)
        return deleted_item

    def _calculate_item_total_price(self, item: TransactionItem) -> int:
        unit_price = Decimal(item.unit_price)
        weight_count = Decimal(item.weight_count)
        ojrat = Decimal(item.ojrat or 0) / 100
        profit = Decimal(item.profit or 0) / 100
        tax = Decimal(item.tax or 0) / 100

        wage_per_unit = unit_price * ojrat
        price_after_wage = unit_price + wage_per_unit
        profit_per_unit = price_after_wage * profit
        price_after_profit = price_after_wage + profit_per_unit

        net_price = unit_price * weight_count
        gross_price = price_after_profit * weight_count
        
        tax_amount = (gross_price - net_price) * tax
        
        total_price = gross_price + tax_amount
        return int(total_price)

transaction_item_service = TransactionItemService()
