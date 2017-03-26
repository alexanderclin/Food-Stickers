from flask import Flask, request
from PIL import Image
# from twilio import twiml
import auth
import requests
from io import BytesIO

app = Flask(__name__)
client = auth.client

details = {
    "Size": "",
    "Topping1": "",
    "Topping2": ""
}


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
    print(nummedia == "3")
    # Get size
    if nummedia == "3":
        print("Gathering detail data")
        sizeurl = request.form['MediaUrl0']
        topping1url = request.form['MediaUrl1']
        topping2url = request.form['MediaUrl2']

        sizetype = get_size_type(sizeurl)
        top1type = get_topping_type(topping1url)
        top2type = get_topping_type(topping2url)
        print(sizetype + top1type + top2type)

        if sizetype == "NULL" or top1type == "NULL" or top2type == "NULL":
            return

        details["Size"] = sizetype
        details["Topping1"] = top1type
        details["Topping2"] = top2type

        print("Sent by " + messenger)
        print("Size: " + sizetype)
        print("Topping1: " + top1type)
        print("Topping2: " + top2type)

        client.messages.create(
            to=messenger,
            from_=twilionumber,
            body="Got details")

    return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
