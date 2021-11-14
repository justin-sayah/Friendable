from firebase_admin import credentials, firestore, initialize_app
cred = credentials.Certificate("google_auth_creds.json")
initialize_app(cred)
db = firestore.client()

def get_group(user_number):
    print('getting the group for ' + str(user_number))
    groups = db.collection('group')
    docs = groups.where(u'people', u'array_contains', str(user_number)).stream()

    #should only be one doc

    for doc in docs:
        # print(doc.to_dict())
        return doc.to_dict()


def make_groups():
    num_groups = 2

    users = db.collection('users')

    g = 5

    for i in range(1, num_groups + 1):

        print('group number ' + str(i))

        n = 0 

        docs = users.where(u'Classes', u'==', i).stream()

        members = []

        for doc in docs:
            n += 1
            doc = doc.to_dict()
            if doc['Phone'] != None:
                doc['number'] = doc['Phone'][2:]
            print(doc)
            # print(type(doc))
            members.append(doc)
        
        group_nums = [1+max(0,n-(i+1))//(n//g) for i in range(n//g)]

        # create the groups

        i = 0
        current_group = []
        group_index = 0
        while(i < len(members)):
            if group_nums[group_index] == 0:
                #write group to database
                create_group(current_group, group_index)
                group_index += 1
                current_group = []

            current_group.append(members[i])
            i += 1
            group_nums[group_index] -= 1

            
def create_group(current_group, group_index):
    groups = db.collection('group')

    print('creating groups')
    #need to get an activity

    # current_group = ['users/' + str(member['number']) for member in current_group]
    current_group = [str(member['number']) for member in current_group]
    print(current_group)

    dict = {}
    dict['people'] = current_group #need to be references to the collection
    dict['confirmed'] = []
    dict['not_going'] = []
    dict['activity'] = 'TODO' #need to be an activity

    print(dict)

    groups.document(str(group_index)).set(dict)

# make_groups()
# get_group('5057216157')