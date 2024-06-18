
import requests, time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from create_database import Stubhub, q 

global previous_raw_price

def producer(q):
    while True:
        elapsed_time = timedelta(seconds=0)
        expected_time = timedelta(minutes=10)
        if elapsed_time > expected_time:
            print("60 minutes have passed. Exiting program.")
            break
        else:
            time.sleep(10)
            start = datetime.now()
            producer_wrapper(q)
            end = datetime.now()
            elapsed_time += time_difference(start, end)

def producer_wrapper(q):
    url = "https://www.stubhub.com/keinemusik-brooklyn-tickets-7-5-2024/event/152788319/?quantity=1"

    previous_raw_price = float('inf')

    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching the webpage.")
        return None

    content_size = len(response.content)

    # Get the size of the response headers in bytes
    headers_size = sum(len(k) + len(v) for k, v in response.headers.items())
    # Total size of the response (content + headers)
    total_size = content_size + headers_size

    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.find_all(string=True)

    output = ''

    # filter elements as needed
    blacklist = [
    # '[document]',
    # 'noscript',
    # 'header',
    # 'html',
    # 'meta',
    # 'head', 
    # 'input',
    # 'script',
    ]

    # create text chunk to scan through
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    ### extract rawPrice
    raw_price_index = output.find('"rawPrice":')
    raw_price_start = raw_price_index + len('"rawPrice":')
    raw_price_end = output.find('.', raw_price_start)
    raw_price = output[raw_price_start:raw_price_end]
    stubhub_price_raw = int(raw_price)

    ### extract priceWithFees
    price_with_fees_index = output.find('"priceWithFees":"$')
    price_with_fees_start = price_with_fees_index + len('"priceWithFees":"$')
    price_with_fees_end = output.find('"', price_with_fees_start)
    price_with_fees = output[price_with_fees_start:price_with_fees_end]
    stubhub_price_with_fees = int(price_with_fees)

    #### get current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # check for price drop
    if stubhub_price_raw < previous_raw_price and stubhub_price_raw < 250:
        print(f"ALERT: PRICE HAS DROPPED FROM ${previous_raw_price} TO ${stubhub_price_raw}!!!! BUY TICKETS NOW!!!")

    # update raw price
    previous_raw_price = stubhub_price_raw

    # check for low price and alert user
    if stubhub_price_raw < 250:
        print(f"ALERT: PRICE HAS DROPPED TO ${stubhub_price_raw}!!!! BUY TICKETS NOW!!!")
        print(f"ALERT: PRICE HAS DROPPED TO ${stubhub_price_raw}!!!! BUY TICKETS NOW!!!")
        print(f"ACT NOW!!!")

    stubhub = Stubhub(time=current_time, 
                  raw_price=stubhub_price_raw, 
                  fees=stubhub_price_with_fees-stubhub_price_raw, 
                  total_price=stubhub_price_with_fees, 
                  lowest_price_time="prev_time", 
                  lowest_price=stubhub_price_raw)
    
    q.put(stubhub)
    
    print(f"Produced: {stubhub}")
    
    print("Finished fetching data from Stubhub.")


def time_difference(start_time, end_time):
            return end_time - start_time





