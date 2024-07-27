# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import Client as TwilioRestClient
from handler import *
from random import choice
import os

######################################################
# Warning: you must replace the values below!
# Find these values at https://twilio.com/user/account
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
fromnumber = "+18333133856"  # twilio
tonumber = "+16175133836"  # your phone
body_text = "Hi!  I'm a sample text message!"
######################################################

client = TwilioRestClient(account_sid, auth_token)

# sends a text from fromnumber to to number consisting of body_text 
def send(fromnumber, tonumber, body_text):
	print("Preparing to send sms text from %s to %s: %s" % (fromnumber, tonumber, body_text))

	message = client.messages.create(to=tonumber, 
									 from_=fromnumber, 
									 body=body_text)

	print("SMS text successfully sent!")

# sends a media text from fromnumber to tonumber consisting of media_links (list of links to media)
def send_media(fromnumber, tonumber, media_links):
	print("Preparing to send media text from %s to %s: %s" % (fromnumber, tonumber, media_links))

	message = client.messages.create(to=tonumber, 
									 from_=fromnumber, 
									 media_url=media_links)

	print("Media text successfully sent!")

# send(fromnumber, tonumber, body_text)

# media_links = ["http://i.telegraph.co.uk/multimedia/archive/03597/POTD_chick_3597497k.jpg", 'https://upload.wikimedia.org/wikipedia/commons/5/55/Phillips_Academy_Andover_Coat_of_Arms.png', 'http://vignette1.wikia.nocookie.net/pokemon/images/f/fc/025Pikachu_OS_anime_5.png/revision/20150101093704', "http://all4desktop.com/data_images/original/4238212-pictures.jpg", "http://i.telegraph.co.uk/multimedia/archive/03519/potd-squirrel_3519920k.jpg", "http://i.telegraph.co.uk/multimedia/archive/03571/potd-squirrel_3571152k.jpg"]
# send_media(fromnumber, tonumber, choice(media_links))



print(send(fromnumber, tonumber, body_text))
