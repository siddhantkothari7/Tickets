from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Stubhub(Base):
    __tablename__ = 'stubhub_prices'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    raw_price = Column(String)
    fees = Column(Integer)
    total_price = Column(Integer)
    lowest_price_time = Column(String)
    lowest_price = Column(Integer)
