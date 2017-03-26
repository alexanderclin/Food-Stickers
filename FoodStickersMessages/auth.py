# /usr/bin/env python
from twilio.rest import TwilioRestClient

account_sid = "AC8b7702bf26e08e4127130812d7e41279"
auth_token = "21ccb590035f3a474a8be5db1bfaef0a"
client = TwilioRestClient(account_sid, auth_token)
