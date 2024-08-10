from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import queue

# Step 1: Define the SQLite database
engine = create_engine('sqlite:///ticketPrices.db')

# Step 2: Create a base class for declarative models
Base = declarative_base()

# Step 3: Define a sample table
class Stubhub(Base):
    __tablename__ = 'stubhub_prices'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    raw_price = Column(String)
    fees = Column(Integer)
    total_price = Column(Integer)
    lowest_price_time = Column(String)
    lowest_price = Column(Integer)

# Step 4: Create the table in the database
Base.metadata.create_all(engine)

# Step 5: Create a session factory
Session = sessionmaker(bind=engine, future=True)

def add_stubHub(stubhub_obj):
    with Session() as session:
        try:
            # Add the object to the session
            session.add(stubhub_obj)
            # Commit the session to write the object to the database
            session.commit()
            print(f"Inserted time: {stubhub_obj.time}, price: {stubhub_obj.price}")
        except Exception as e:
            session.rollback()
            print(f"An error occured, failed to insert object: {e}") 

q = queue.Queue()