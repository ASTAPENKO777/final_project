from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.result import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database and tables created.")
