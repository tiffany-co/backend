from getpass import getpass
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.user import user_service
from app.schema.user import UserCreate
from app.models.user import UserRole

def main():
    """
    Synchronous script to create a new admin user.
    """
    print("--- Create Admin User ---")
    db: Session = SessionLocal()
    
    try:
        full_name = input("Full Name: ").strip()
        username = input("Username: ").strip()
        phone_number = input("Phone Number: ").strip()
        password = getpass("Password: ")
        
        if not all([full_name, username, phone_number, password]):
            print("All fields are required.")
            return

        user_in = UserCreate(
            full_name=full_name,
            username=username,
            phone_number=phone_number,
            password=password,
            role=UserRole.ADMIN # Explicitly set the role to ADMIN
        )
        
        user = user_service.create_user(db=db, user_in=user_in)
        print(f"Admin user '{user.username}' created successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()

