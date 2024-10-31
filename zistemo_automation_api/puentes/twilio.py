from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException

class TwilioBridge:

    @staticmethod 
    def send_sms(to, body):

        account_sid=settings.TWILIO_ACCOUNT_SID
        auth_token=settings.TWILIO_AUTH_TOKEN
        twilio_number=settings.TWILIO_NUMBER
        try:
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=body,
                from_=twilio_number,
                to=to
            )
            return message
        except TwilioRestException as e:
            print("TwilioRestException:: "+str(e))
            return False
            
