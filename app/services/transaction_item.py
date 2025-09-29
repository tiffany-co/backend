import uuid
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import status

from app.core.exceptions import AppException
from app.models.user import User
from app.models.transaction_item import TransactionItem
from app.models.enums.transaction import TransactionType
from app.models.enums.shared import ApprovalStatus
from app.repository.transaction_item import transaction_item_repo
from app.schema.transaction_item import TransactionItemCreate, TransactionItemUpdate
from app.services.transaction import transaction_service
from app.services.item import item_service # Import item service for validation

class TransactionItemService:

    def get_item_by_id(self, db: Session, *, item_id: uuid.UUID, current_user: User) -> TransactionItem:
        item = transaction_item_repo.get(db, id=item_id)
        if not item:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction item not found."
            )
        
        # Piggyback on transaction service to check permissions
        transaction_service.get_by_id(db, transaction_id=item.transaction_id, current_user=current_user)
        return item

    def create_item(self, db: Session, *, item_in: TransactionItemCreate, current_user: User) -> TransactionItem:
        transaction = transaction_service.get_by_id(db, transaction_id=item_in.transaction_id, current_user=current_user, with_items=True)
        if transaction.status != ApprovalStatus.DRAFT:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Items can only be added to transactions in 'draft' status."
            )
        
        # Validate that the item template exists
        item_service.get_by_id(db, item_id=item_in.item_id)
        
        create_data = item_in.model_dump()
        
        create_data["total_price"] = self._calculate_item_total_price(item_in, item_in.transaction_type)
        
        new_item = transaction_item_repo.create(db, obj_in=create_data)
        transaction_service._recalculate_total_price(db, transaction=transaction)
        return new_item

    def update_item(self, db: Session, *, item_id: uuid.UUID, item_in: TransactionItemUpdate, current_user: User) -> TransactionItem:
        item_to_update = self.get_item_by_id(db, item_id=item_id, current_user=current_user)
        
        transaction = item_to_update.transaction
        if transaction.status != ApprovalStatus.DRAFT:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Items can only be updated if the transaction is in 'draft' status."
            )
        
        if item_in.item_id: # check if new item exist
            item_service.get_by_id(db, item_id=item_id)
        
        updated_item = transaction_item_repo.update(db, db_obj=item_to_update, obj_in=item_in)
        
        # Recalculate total price if relevant fields changed
        update_data = item_in.model_dump(exclude_unset=True)
        recalc_fields = {'unit_price', 'weight_count', 'ojrat', 'profit', 'tax'}
        if any(field in update_data for field in recalc_fields):
            updated_item.total_price = self._calculate_item_total_price(updated_item, updated_item.transaction_type)
            db.commit()
            db.refresh(updated_item)
            
        transaction_service._recalculate_total_price(db, transaction=transaction)
        return updated_item
        
    def delete_item(self, db: Session, *, item_id: uuid.UUID, current_user: User) -> TransactionItem:
        item_to_delete = self.get_item_by_id(db, item_id=item_id, current_user=current_user)
        
        transaction = item_to_delete.transaction
        if transaction.status != ApprovalStatus.DRAFT:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Items can only be deleted if the transaction is in 'draft' status."
            )
            
        deleted_item = transaction_item_repo.remove(db, id=item_id)
        transaction_service._recalculate_total_price(db, transaction=transaction)
        return deleted_item

    def _calculate_item_total_price(self, item: TransactionItem, transaction_type: TransactionType) -> int:
        """
        BUY: When we want to buy something, tax, profit, and labor (ojrat) are currently calculated as zero
        SELL: Calculation according to the formula given in Excel (simplified)
        """
        unit_price = Decimal(item.unit_price) # مظنه
        weight_count = Decimal(item.weight_count) # وزن / تعداد
        ojrat = Decimal(item.ojrat or 0) / 100 # اجرت
        profit = Decimal(item.profit or 0) / 100 # سود
        tax = Decimal(item.tax or 0) / 100 # مالیات

        wage_per_unit = unit_price * ojrat # اجرت به ازای واحد (گرم/تعداد)
        price_after_wage = unit_price + wage_per_unit # قیمت هر واحد بعد از اجرت
        profit_per_unit = price_after_wage * profit # سود به ازای هر واحد (گرم/تعداد)
        price_after_profit = price_after_wage + profit_per_unit # قیمت بعد از سود به ازای هر واحد
        
        net_price = unit_price * weight_count # قیمت خالص
        gross_price = price_after_profit * weight_count # قیمت ناخالص
        
        tax_amount = (gross_price - net_price) * tax # قیمت نهایی بعد از مالیات
        
        total_price = gross_price + tax_amount
        
        return int(total_price)

transaction_item_service = TransactionItemService()
