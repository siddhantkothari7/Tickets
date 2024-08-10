from twilio.rest import Client
import os
import boto3
from botocore.exceptions import ClientError
import json

def get_secret():
    secret_name = "twilio/dev"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"The requested secret {secret_name} was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print(f"The request was invalid due to: {e}")
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print(f"The request had invalid params: {e}")
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print(f"The requested secret can't be decrypted using the provided KMS key: {e}")
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print(f"An error occurred on service side: {e}")
        else:
            print(f"An unexpected error occurred: {e}")
        return None
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = get_secret_value_response['SecretBinary']
            secret = secret.decode('utf-8')

        return json.loads(secret)

def send_whatsapp_message():
    secret = get_secret()
    print(secret)
    if secret is None:
        print("Failed to retrieve secret")
        return

    account_sid = secret.get('account_sid')
    print(account_sid)
    auth_token = secret.get('auth_token')
    print(auth_token)
    
    if not account_sid or not auth_token:
        print("Missing Twilio credentials in the secret")
        return

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Hey! Programatic test message using lambda1!',
        to='whatsapp:+16175133836'
    )

    print(f"Message sent with SID: {message.sid}")

if __name__ == '__main__':
    send_whatsapp_message()