from flask import Flask, json, request, render_template, jsonify
import os
from send_sms import send_message
from firebase_admin import credentials, firestore, initialize_app
from Temp import Temp
from User import User
from flask import jsonify
from random import randint


def verify_phone(num):
    import re
    regex = re.compile(r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    return regex.search(str(num))

app = Flask(__name__)
cred = credentials.Certificate("google_auth_creds.json")
initialize_app(cred)
db = firestore.client()
users = db.collection('users')
temp_codes = db.collection('temp_codes')

@app.route('/')
def test():
    print('got a request here')
    return render_template("index.html")

@app.route('/sign_in', methods=['GET', 'Post'])
def sign_in():
    print('got a request')
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        # Do stuff here
        print('in here')
        ret = request.get_json()

        number = ret['number']

        if not verify_phone(number):
            return render_template('index.html', message="Please enter a valid phone number.")
            
        # Check to see if the number is in the data base
        docs = users.where(u'number', u'==', '5').stream()
        print(number)

        size = 0
        for doc in docs:
            if size > 0:
                print('something is wrong')
            else:
                size += 1
                # maybe unpack some things about the user

        exists = size == 1

        exists = False

        # need to verify number either way

        ran_num = 56565
        ran_num = int(''.join(["{}".format(randint(0, 9)) for num in range(0, 5)]))
        print(ran_num)

        new_temp = Temp(number, ran_num)


        if exists:
            print('sending message')
            # gen random number

            
            send_message(ran_num, toNum=number[2:])
            # update random number in the database
            # print('created new temp')
            # print(number[2:])
            # print(json.dumps(new_temp.serialize()))
            temp_ret = temp_codes.document(number[2:]).get().to_dict()
            temp_ret['number'] = ran_num
            temp_codes.document(number[2:]).set(temp_ret)
            print('updated')
            return render_template('verify.html', new=False, pnum=number)
        else:
            # going to create a new user
            print('need to verify number first')
            send_message(ran_num, toNum=number[2:])
            temp_codes.document(number[2:]).set(new_temp.serialize())
            return render_template('verify.html', new=True, pnum=number)