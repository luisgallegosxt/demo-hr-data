from core.config import settings
from models import User
from sqlalchemy.orm import sessionmaker, Session
from schemas import UserCreate
from crud import create_user


# Create first superuser if not exists
def init_db(db: Session) -> None:

    user = db.query(User).filter(User.username == settings.FIRST_SUPERUSER).first()
    if not user:
        superuser_data = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD
        )
        create_user(db, superuser_data)
        print("First superuser created")


