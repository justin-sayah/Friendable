from firebase_admin import credentials, firestore, initialize_app
from phone_gen import PhoneNumber

def i_love_data(filename):
    cred = credentials.Certificate("google_auth_creds.json")
    initialize_app(cred)
    db = firestore.client()
    users = db.collection('users')

    with open(filename) as f:
        for line in f:
            line = line.replace('\n','').split(',')
            vals = {'Name': line[0],'EF':line[1],'SI':line[2],'TF':line[3],'JP':line[4],'Cereal':line[5],'Hotdog':line[6],'Sleep':line[7],'IceCream':line[8],'Messy':line[9],'Aliens':line[10],'Classes':line[11]}
            num = PhoneNumber('US').get_number()
            print('[*] inserting ' + line[0] + ' with id ' + num)
            users.document(num).set(vals)

    print('<------- All Done :))) ------->')

if __name__== '__main__':
    i_love_data('fake_people.csv')