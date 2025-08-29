import asyncio
from getpass import getpass
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.services.user import user_service
from app.schema.user import UserCreate
from app.models.user import UserRole

async def main():
    print("--- Create Admin User ---")
    db: AsyncSession = SessionLocal()
    
    try:
        full_name = input("Full Name: ")
        username = input("Username: ")
        phone_number = input("Phone Number: ")
        password = getpass("Password: ")
        
        user_in = UserCreate(
            full_name=full_name,
            username=username,
            phone_number=phone_number,
            password=password,
            role=UserRole.ADMIN # Explicitly set the role to ADMIN
        )
        
        user = await user_service.create_user(db=db, user_in=user_in)
        print(f"Admin user '{user.username}' created successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
