from firebase_admin import credentials, firestore, initialize_app
from generate_suggestion import gen_result

cred = credentials.Certificate("google_auth_creds.json")
# initialize_app(cred)
db = firestore.client()

def get_group_object(user_number):
    print('getting the group for ' + str(user_number))
    groups = db.collection('group')
    docs = groups.where(u'people', u'array_contains', str(user_number)).stream()

    #should only be one doc
    for doc in docs:
        print(doc.to_dict())
        return doc.to_dict()


def make_groups():
    num_groups = 10

    users = db.collection('users')

    g = 5

    for i in range(0, num_groups):

        print('group number ' + str(i))

        n = 0 

        docs = users.where(u'Classes', u'==', i).stream()

        members = []

        for doc in docs:
            n += 1
            doc = doc.to_dict()
            # if doc['Phone'] != None:
            #     doc['number'] = doc['Phone']
            # print(doc)
            # print(type(doc))
            members.append(doc)

        # print('this group has ' + str(n))
        
        group_nums = [1+max(0,n-(j+1))//(n//g) for j in range(n//g)]

        # print(group_nums)

        # create the groups

        j = 0
        current_group = []
        group_index = 0
        while(j < len(members)):
            if group_nums[group_index] == 0:
                #write group to database
                create_group(current_group, group_index, i)
                group_index += 1
                current_group = []

            current_group.append(members[j])
            j += 1
            group_nums[group_index] -= 1

        # print('the group index is')
        # print(group_index)
        # print(group_nums)
        if current_group != []:
            create_group(current_group, group_index, i)
        # print(current_group)

            
def create_group(current_group, group_index, class_num):
    groups = db.collection('group')

    print('creating groups')
    print(group_index)
    print(class_num)
    #need to get an activity

    activity = gen_result()

    # current_group = ['users/' + str(member['number']) for member in current_group]
    current_group = [str(member['number']) for member in current_group]
    print(current_group)

    dict = {}
    dict['people'] = current_group #need to be references to the collection
    dict['confirmed'] = []
    dict['not_going'] = []
    dict['activity'] = activity #need to be an activity

    # print(dict)

    groups.document(str(group_index) + str(class_num)).set(dict)

# make_groups()
# get_group_object('9788065553')