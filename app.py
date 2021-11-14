from flask import Flask, json, request, render_template, jsonify
import os
from send_sms import send_message
from firebase_admin import credentials, firestore, initialize_app
from Temp import Temp
from User import User
from flask import jsonify
from random import randint
from get_predictions import get_prediction
from werkzeug.datastructures import ImmutableMultiDict



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

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    print('got a request')
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # Do stuff here
        print('in here')

        # try:
        #     ret = request.get_json()
        # except:
        #     print('could not get json')
        #     return render_template('index.html')
        # print('got here')
        # if ret == None:
        #     return render_template('index.html')

        # number = ret['number']

        number = request.values.get('phone')
        print(request.values)
        print(number)

        if not verify_phone(number):
            print('could not verify number')
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
        ran_num = int(''.join(["{}".format(randint(1, 9)) for num in range(0, 5)]))
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
            temp_ret = temp_codes.document(number).get().to_dict()
            temp_ret['number'] = ran_num
            temp_codes.document(number).set(temp_ret)
            print('updated')
            return render_template('verify.html', new=False, pnum=number)
        else:
            # going to create a new user
            print('need to verify number first')
            send_message(ran_num, toNum=number)
            temp_codes.document(number).set(new_temp.serialize())
            print('should return verify')
            # return render_template('sign_in.html')
            return render_template('verify.html', new=True, pnum=number)


@app.route('/verify', methods=['GET', 'Post'])
def verify():
    if request.method == 'GET':
        return render_template('verify.html', new=True, pnum=6)


    print(request.values)

    new = request.values.get('new')
    number = request.values.get('pnum')
    code = request.values.get('code')

    print('the number is')
    print(number)

    temp_ret = temp_codes.document(number).get().to_dict()
    actual_num = temp_ret['number']

    if str(actual_num) == str(code):
        print('it worked')
        if new:
            # return form
            return render_template('survey.html', pnum=number)
        else:
            # return whatever page we show people who already 
            return render_template('sign_in.html') #this is just a placeholder

    else:
        print('actual code')
        print(actual_num)
        print('inputed code')
        print(code)
        print('wrong code')
        return render_template('verify.html', new=new, pnum=number)



@app.route('/survey', methods=['GET', 'Post'])
def survey():

    print('Getting survey results')

    if request.method == "GET":
        return render_template('survey.html')

    print(request.values)
    number = request.values['number']

    label = get_prediction(request.values)

    print(label)

    dict = request.values.to_dict(flat=False)
    dict['Classes'] = int(label)    

    # now put the values in the database

    users.document(number).set(dict)

    print('inserted into database')


def verify_phone(num):
    print('calling the verify method')
    import re
    regex = re.compile(r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    return regex.search(str(num))