from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc, nulls_last, func
from typing import List, Optional, Any
import uuid

from app.repository.base import BaseRepository
from app.models.account_ledger import AccountLedger
from app.schema.account_ledger import AccountLedgerCreate, AccountLedgerUpdate

class AccountLedgerRepository(BaseRepository[AccountLedger, AccountLedgerCreate, AccountLedgerUpdate]):
    """
    Repository for account ledger related database operations.
    """
    def search(
        self,
        db: Session,
        *,
        has_debt: Optional[bool] = None,
        debt: Optional[int] = None,
        bank_name: Optional[str] = None,
        contact_id: Optional[uuid.UUID] = None,
        transaction_id: Optional[uuid.UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AccountLedger]:
        """
        Searches for account ledgers based on a combination of criteria.
        Access is now open to all authenticated users.
        """
        query = db.query(self.model)

        if has_debt is not None:
            if has_debt:
                query = query.filter(self.model.debt != 0)
            else:
                query = query.filter(self.model.debt == 0)
        
        if bank_name:
            query = query.filter(self.model.bank_name.ilike(f"%{bank_name}%"))
        
        if contact_id:
            query = query.filter(self.model.contact_id == contact_id)

        if transaction_id:
            query = query.filter(self.model.transaction_id == transaction_id)
            
        # --- Conditional Sorting ---
        if debt is not None:
            # Order by the absolute difference from the provided debt amount
            query = query.order_by(func.abs(self.model.debt - debt).asc())
        else:
            # Default sort by deadline ascending, with NULLs (no deadline) appearing last.
            query = query.order_by(nulls_last(asc(self.model.deadline)))

        return query.offset(skip).limit(limit).all()

account_ledger_repo = AccountLedgerRepository(AccountLedger)

