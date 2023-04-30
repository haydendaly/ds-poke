from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.shared.models import Base

DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
