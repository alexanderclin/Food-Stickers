# /usr/bin/env python
from twilio.rest import TwilioRestClient

account_sid = "ACCOUNT SID"
auth_token = "AUTH TOKEN"
client = TwilioRestClient(account_sid, auth_token)
