from django.conf import settings
from twilio.rest import Client


def send_otp(mobile):
    number= '+91'+str(mobile)
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    service_id=settings.SERVICES_ID
    client = Client(account_sid, auth_token)

    verification = client.verify \
                        .services(service_id) \
                        .verifications \
                        .create(to=number, channel='sms')

    return(verification.sid)


def verify_otp(mobile,otp):
    number= '+91'+str(mobile)
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    service_id=settings.SERVICES_ID
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
                           .services(service_id) \
                           .verification_checks \
                           .create(to=number, code=otp)

    if verification_check.status=='approved':
        return True
    else:
        return False