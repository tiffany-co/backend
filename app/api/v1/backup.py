from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
from datetime import datetime

from app.api import deps
from app.models.user import User, UserRole
from app.services.backup import backup_service
from app.schema.error import ErrorDetail

router = APIRouter()

@router.get(
    "/export",
    response_class=StreamingResponse,
    summary="[Admin] Export Database Backup",
    description="Downloads a JSON file containing a backup of all database tables, excluding the audit log.",
    responses={
        200: {
            "description": "Database backup file.",
            "content": {"application/json": {}},
        },
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
    }
)
def export_backup(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    """
    Generates and returns a JSON backup of the database.
    """
    json_str = backup_service.export_data_as_json_str(db)
    
    # Create a file-like object in memory
    file_obj = io.StringIO(json_str)
    
    # Generate a filename with the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"goldshop_backup_{timestamp}.json"
    
    return StreamingResponse(
        file_obj,  # directly stream from StringIO
        # iter([file_obj.read()]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post(
    "/import",
    status_code=status.HTTP_200_OK,
    summary="[Admin] Import Database Backup",
    description="Upload a JSON backup file to restore the database state. This will delete all existing data (except audit logs) before importing.",
     responses={
        200: {"description": "Database restored successfully."},
        400: {"model": ErrorDetail, "description": "Invalid file or JSON format."},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
        500: {"model": ErrorDetail, "description": "Database import failed during the transaction."},
    }
)
async def import_backup(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
    file: UploadFile = File(..., description="The .json backup file to upload."),
):
    """
    Restores the database from an uploaded JSON file.
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Please upload a .json file.")

    contents = await file.read()
    json_str = contents.decode("utf-8")
    
    backup_service.import_data_from_json_str(db, json_str)
    
    return {"detail": "Database restored successfully from backup."}

