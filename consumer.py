import queue
from database import Session
from Tickets.models import Stubhub

def consumer(q):
    while True:
        data = q.get()
        if data is None:
            break  # If None is received, exit the loop
        with Session() as session:
            try:
                # new_stubhub = Stubhub(time=data['time'], raw_price=data['raw_price'], fees=data['fees'], total_price=data['total_price'], lowest_price_time=data['lowest_price_time'], lowest_price=data['lowest_price'])
                session.add(data)
                session.commit()
                print("Consumed and Added to DB: " + str(data))
            except Exception as e:
                session.rollback()
                print(f"An error occurred: {e}")
        q.task_done()