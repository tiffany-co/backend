from sqlalchemy.orm import Session
from typing import List, Any

from app.repository.base import BaseRepository
from app.models.permission import Permission
from app.models.enums.permission import PermissionName

class PermissionRepository(BaseRepository[Permission, Any, Any]):
    """
    Repository for permission-related database operations.
    """
    def get_by_name(self, db: Session, *, name: PermissionName) -> Permission | None:
        """
        Get a permission by its name.
        """
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_all_names(self, db: Session) -> List[PermissionName]:
        """
        Get a list of all permission names currently in the database.
        """
        return [p.name for p in db.query(self.model.name).all()]

permission_repo = PermissionRepository(Permission)
