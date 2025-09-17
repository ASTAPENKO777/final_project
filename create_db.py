import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.result import Base
from models.team import Team
from models.tournament import Tournaments

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database and tables created.")
