from flask import Flask, json, request, render_template, jsonify
import os

from numpy import add
from send_sms import send_message
from firebase_admin import credentials, firestore, initialize_app
from Temp import Temp
from User import User
from flask import jsonify
from random import randint
from get_predictions import get_prediction
from werkzeug.datastructures import ImmutableMultiDict
from make_groups import get_group_object
import requests, io, base64, cv2
import PIL.Image as img
from generate_human import make_human



app = Flask(__name__)
# cred = credentials.Certificate("google_auth_creds.json")
# initialize_app(cred)
db = firestore.client()
users = db.collection('users')  
temp_codes = db.collection('temp_codes')
activies = db.collection('activies')
groups = db.collection('group')


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
        # docs = users.where(u'number', u'==', '5').stream()
        # print(number)

        # size = 0
        # for doc in docs:
        #     if size > 0:
        #         print('something is wrong')
        #     else:
        #         size += 1
        #         # maybe unpack some things about the user


        user = users.document(number).get()
        # print('PRINTING THE USER')
        # print(user.to_dict())
        user = user.to_dict()
        # print(user == None)

        # exists = False
        # print('exists')
        # print(exists)

        # need to verify number either way

        ran_num = 56565
        ran_num = int(''.join(["{}".format(randint(1, 9)) for num in range(0, 5)]))
        print(ran_num)

        new_temp = Temp(number, ran_num)


        if user != None:
            print('sending message')
            # gen random number

            
            send_message(ran_num, toNum=number)
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

    print('is a new user')
    print(new)

    temp_ret = temp_codes.document(number).get().to_dict()
    actual_num = temp_ret['number']

    if str(actual_num) == str(code):
        print('it worked')
        if new == 'True':
            # return form
            return render_template('survey.html', pnum=number)
        else:
            print('is not a new user')
            # return whatever page we show people who already 
            # return render_template('results.html') #will need to give it more 0
            return get_group(number)

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

    dict = request.values.to_dict()
    print(dict)
    dict['Classes'] = int(label)    

    # now put the values in the database

    users.document(number).set(dict)

    print('inserted into database')

    # return render_template('results.html') #will probably make into a method
    return render_template('countdown.html')

def verify_phone(num):
    print('calling the verify method')
    import re
    regex = re.compile(r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    return regex.search(str(num))

def get_group(num):

    print('getting a group for ' + str(num))

    user = users.document(num).get().to_dict()

    print('the user is ' + str(user))
    name = user['name']
    pnum = user['number']

    group = get_group_object(num)



    print('Group')
    print(group)

    #get the people in the group

    people = group['people']

    other_people = []
    other_people_status = []
    other_people_names = []

    for person in people:
        if person != num:
            user = users.document(person).get().to_dict()
            if person in group['confirmed']:
                user['status'] = 'yes'
            elif person in group['not_going']:
                user['status'] = 'no'
            else:
                user['status'] = 'maybe'
            other_people_status.append(user['status'])
            other_people_names.append(user['Name'])

            other_people.append(user)

    activity = group['activity']
    activity = activies.document(activity).get().to_dict()

    group_id = group['group_id']

    if pnum in group['confirmed']:
        status = 'going'
    elif pnum in group['not_going']:
        status = 'not_going'
    else:
        status = 'maybe'

    print('other people')
    print(other_people)
    print('activity')
    print(activity)

    if activity['type'] == 'place':
        #make the api call
        obj = img.open(io.BytesIO(requests.get(activity['api_call']).content))
        obj.save('./static/place.jpeg')
        loc_name = activity['name']
        address = activity['vicinity']
    else:
        loc_name = activity['name']
        address = activity['address'][0]

    create()

    src_list = ['../static/human_' + str(i) + '.jpeg' for i in range(1,6)]
    
    return render_template('results.html',src_list=src_list, other_people_status=other_people_status, other_people_names=other_people_names, loc_name=loc_name,address=address, status=status,name=name,group_id=group_id,pnum=pnum, person=user, other_people=other_people, activity=activity)

@app.route('/test_show_person', methods=['GET'])
def test_show_person():
    return render_template('test_show_person.html')

@app.route('/going', methods=['POST'])
def going():
    print('in the going function')
    group_id = request.values['group_id']
    number = request.values['pnum']

    #get the group
    group = groups.document(group_id).get().to_dict()
    print('type')
    print(group['confirmed'])
    (group['confirmed']).append(number)

    print(group)
    groups.document(group_id).set(group)

    return get_group(number)

@app.route('/not_going', methods=['POST'])
def not_going():
    print('in the not_going function')
    group_id = request.values['group_id']
    number = request.values['pnum']

    #get the group
    group = groups.document(group_id).get().to_dict()
    # print('type')
    # print(group['confirmed'])
    (group['not_going']).append(number)

    # print(group)
    groups.document(group_id).set(group)

    return get_group(number)

def create():
    print('making random avatars')
    for i in range(1,6):
        make_human(i)



    