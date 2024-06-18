import threading
import queue
from producer import producer
from consumer import consumer

# Create a queue
q = queue.Queue()

# Create and start the producer and consumer threads
producer_thread = threading.Thread(target=producer, args=(q,))
consumer_thread = threading.Thread(target=consumer, args=(q,))

producer_thread.start()
consumer_thread.start()

producer_thread.join()
q.put(None)  # Signal the consumer to exit
consumer_thread.join()