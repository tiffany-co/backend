from app.models.enums.permission import PermissionName

# This file contains the raw data for permissions to be seeded into the database.
PREDEFINED_PERMISSIONS = [
    {
        "name": PermissionName.CONTACT_UPDATE_ALL,
        "name_fa": "ویرایش تمام مخاطبین",
        "description": "این دسترسی به کاربر اجازه می‌دهد تا اطلاعات تمام مخاطبین را، صرف نظر از اینکه چه کسی آنها را ایجاد کرده، ویرایش کند."
    },
]