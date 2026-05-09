from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./customer_support.db"

Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text)
    bot_response = Column(Text)
    intent = Column(String)
    status = Column(String, default="resolved") # resolved or escalated
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

from sqlalchemy import create_engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
