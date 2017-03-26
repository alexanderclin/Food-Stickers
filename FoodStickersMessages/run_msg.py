from flask import Flask, request
from PIL import Image
# from twilio import twiml
import auth
import requests
from io import BytesIO

app = Flask(__name__)
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


class Order:
    toppings = []
    isComplete = False


@app.route("/", methods=['GET', 'POST'])
def sms():
    print(pendingOrderDict)
    print(completedOrderDict)

    usernum = request.form['From']
    twinum = request.form['To']

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

    return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
