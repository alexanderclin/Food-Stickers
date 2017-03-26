from flask import Flask, flash, redirect, render_template, request, session, abort
import os
 
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

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"

@app.route("/sms", methods=['GET', 'POST'])
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

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    app.run(host='0.0.0.0', port=4000)
