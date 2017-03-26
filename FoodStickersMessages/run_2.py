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


def get_size_type(imgurl):
    response = requests.get(imgurl)
    img = Image.open(BytesIO(response.content))
    pix = img.load()
    color = pix[3, 3]
    print(color)
    return {
        (255, 0, 0): "S",
        (0, 255, 0): "M",
        (0, 0, 255): "L"
    }.get(color, "NULL")


def get_topping_type(imgurl):
    response = requests.get(imgurl)
    img = Image.open(BytesIO(response.content))
    pix = img.load()
    color = pix[3, 3]
    print(color)
    return {
        (255, 0, 0): "Lettuce",
        (0, 255, 0): "Tomato",
        (0, 0, 255): "Cheese"
    }.get(color, "NULL")


@app.route("/", methods=['GET', 'POST'])
def details_sms():
    # Replies with media url
    messenger = request.form['From']
    twilionumber = request.form['To']
    nummedia = request.form['NumMedia']
    print("Received message with " + nummedia + " media " + " by " + messenger)
    print(int(nummedia) > 1)
    # Get size
    if int(nummedia) > 1:
        print()
        print("Gathering size")
        print("Sent by " + messenger)

        sizeurl = request.form['MediaUrl0']
        sizetype = get_size_type(sizeurl)
        if sizetype == "NULL":
            return 'ERROR'
        details["Size"] = sizetype
        print("Size: " + sizetype)
        print()

        for num in range(1, int(nummedia)):
            print("Checking topping #" + str(num))
            topurl = request.form['MediaUrl' + str(num)]
            print("Obtained URL " + topurl)
            toptype = get_topping_type(topurl)
            print("Obtained type " + toptype)
            if toptype == "NULL":
                continue
            details["Topping" + str(num)] = toptype
            print("Added " + "Topping" + str(num) + " to details dictionary")
            print()

        print(details)
        orderlist.append(details)
        print(orderlist)

        client.messages.create(
            to=messenger,
            from_=twilionumber,
            body="Got order details")

    return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
