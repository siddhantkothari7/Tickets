from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Define the SQLite database
engine = create_engine('sqlite:///queue_database.db', echo=True)

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine, future=True)