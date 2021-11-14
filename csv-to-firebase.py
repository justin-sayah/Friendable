from firebase_admin import credentials, firestore, initialize_app
from phone_gen import PhoneNumber

def i_love_data(filename):
    cred = credentials.Certificate("google_auth_creds.json")
    initialize_app(cred)
    db = firestore.client()
    users = db.collection('users')

    with open(filename) as f:
        for line in f:
            try:
                line = line.replace('\n','').split(',')
                num = PhoneNumber('US').get_number()
                num = str(num[2:])
                vals = {'Name': line[0],'EF':float(line[1]),'SI':float(line[2]),'TF':float(line[3]),'JP':float(line[4]),'Cereal':int(line[5]),'Hotdog':int(line[6]),'Sleep':int(line[7]),'IceCream':int(line[8]),'Messy':int(line[9]),'Aliens':int(line[10]),'Classes':int(line[11]), 'Phone':num}
                print('[*] inserting ' + line[0] + ' with id ' + num)
                users.document(num).set(vals)
            except:
                continue

    print('<------- All Done :))) ------->')

if __name__== '__main__':
    i_love_data('fake_people.csv')