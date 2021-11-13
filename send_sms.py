from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
import yaml




def send_message(messageToSend, toNum=None):
    print('sending message')
    
    creds = yaml.safe_load(open("creds.yaml", "r"))
    account_sid = creds['ACCOUNT_SID']
    auth_token = creds['AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    fromNum = creds['from']

    message = client.messages.create(
            body='Your verification code for Friendable is ' + str(messageToSend),
            from_=fromNum,
            to=toNum,
        )


