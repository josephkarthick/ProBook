from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User


def create_admin_user():

    db: Session = SessionLocal()

    try:
        admin = db.query(User).filter(User.username == "admin").first()

        if not admin:

            admin_user = User(
                username="admin",
                password="admin123",  # plain text for now
                role="admin",
                is_active=True
            )

            db.add(admin_user)
            db.commit()

            print("✅ Admin user created")

        else:
            print("ℹ️ Admin user already exists")

    finally:
        db.close()
