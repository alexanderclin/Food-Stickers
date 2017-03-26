from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from PIL import Image
# from twilio import twiml
import auth
import requests
from io import BytesIO
from twilio.rest import TwilioRestClient



app = Flask(__name__)

account_sid = "AC8b7702bf26e08e4127130812d7e41279"
auth_token = "21ccb590035f3a474a8be5db1bfaef0a"

client = TwilioRestClient(account_sid, auth_token)

client = auth.client

details = {
    "Size": ""
}

orderlist = []

pendingOrderDict = {}
completedOrderDict = {}

burgerColor = (112, 63, 37, 255)
lettuceColor = (140, 198, 98, 255)
garlicColor = (255, 236, 210, 255)
onionColor = (94, 23, 77, 255)
cheeseColor = (229, 172, 19, 255)
tomatoColor = (197, 33, 32, 255)


# Returns a tuple with RGB value of the top left pixel
def get_color(imgurl):
    response = requests.get(imgurl)
    img = Image.open(BytesIO(response.content))
    pix = img.load()
    return pix[1, 1]

class Order(object):
    def __init__(self):
        self.toppings = []


@app.route("/", methods=['GET', 'POST'])
def web():
    return render_template('login.html', pendingorders=pendingOrderDict,
    completedorders=completedOrderDict)

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    print('hi')
    print(pendingOrderDict)
    print(completedOrderDict)

    usernum = request.form['From']
    twinum = request.form['To']
    
    print('RECEIVING MESSAGE FROM' + usernum)
    print('Current TOPPINGS')
    
    text = request.form['Body']
    print('Text following:')
    print(text)
    if text == "👍":
        print('Thumbs up, completing order')
        completedOrderDict[usernum] = pendingOrderDict[usernum]
        print(completedOrderDict)
        print(completedOrderDict[usernum].toppings)
        pendingOrderDict.pop(usernum)

        client.messages.create(
            to=usernum,
            from_=twinum,
            body="Done, preparing an order for a burger with: " +
            str(completedOrderDict[usernum].toppings))

        return 'GOT TEXT'

    imageurl = request.form['MediaUrl0']
    color = get_color(imageurl)
    print(color)
    if color == burgerColor:
        pendingOrderDict[usernum] = Order()
        client.messages.create(
            to=usernum,
            from_=twinum,
            body="Starting order, input toppings:")
        print('Added burger')
        print('CURRENT TOPPINGS')
        print(pendingOrderDict[usernum].toppings)
        return 'GOT BURGER'

    if color == lettuceColor:
        pendingOrderDict[usernum].toppings.append('Lettuce')
        print('Added Lettuce')
        return 'GOT LETTUCE'

    if color == cheeseColor:
        pendingOrderDict[usernum].toppings.append('Cheese')
        print('Added cheese')
        return 'GOT CHEESE'

    if color == tomatoColor:
        pendingOrderDict[usernum].toppings.append('Tomato')
        print('Added tomato')
        return 'GOT TOMATO'

    if color == garlicColor:
        pendingOrderDict[usernum].toppings.append('Garlic')
        print('Added garlic')
        return 'GOT GARLIC'

    if color == onionColor:
        pendingOrderDict[usernum].toppings.append('Onion')
        print('Added onion')
        return 'GOT ONION'
    

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)


