from flask import Flask
from  helpers.my_functions import db_services, myTimezones
import json
from collections import defaultdict

with open('data/dict_words.json', 'r') as json_file:
    word_data = json.load(json_file)


# Initialize Flask app
app = Flask(__name__)
app.debug = True

myTimeStamp = myTimezones.ukTime()
formatted_date = myTimezones.anchorageTime()

# Initialize Firestore DB
db_connection = db_services()
docs = db_services.get_data(db_connection)

# Define global variables
list_of_letters = []
constant = ''

# @app.route("/")
# def hello_world():
#     return "Hello, :)</p>"

@app.route("/docs")
def collection_data():
    data_list = []
    for doc in docs:
        data = doc.to_dict()
        data.pop('timestamp')
        data_list.append(data)
    return data_list

def order_letters(return_data):
    for one in return_data:
        for each in one['letters']:
            list_of_letters.append(each)
        for each in one['mandatory']:
            if each == '\n':
                continue
            else:
                constant = each
        list_of_letters.append(constant)
    return list_of_letters, constant

try:
    new_data = collection_data()
    print(new_data)
    fetched_data = order_letters(new_data)
    constant = fetched_data[1]
    print('fetched data is:' + str(fetched_data))
except Exception as e:
    print('An error occured', str(e))

@app.route("/")
def find_words():
    
    print('list of letters:'+ str(list_of_letters))
    list_dict = {letter: [] for letter in list_of_letters}

    list_dict = defaultdict(list)

    # Create a dictionary of words starting with each letter
    for word in word_data:
        if word:
            first_char = word[0]
            list_dict[first_char].append(word)

    four_plus = []

    # Find words containing the constant letter 'v'
    for letter in list_of_letters:
        for word in list_dict[letter]:
            if len(word) > 3 and constant in word:
                four_plus.append(word)

    unwanted_words = []

    # Find words that contain letters not in the list_of_letters
    for word in four_plus:
        for letter in word:
            if letter not in list_of_letters:
                unwanted_words.append(word)

    # Calculate the difference
    difference = list(set(four_plus) - set(unwanted_words))
    return (str(difference))

payload_data = {"timestamp": formatted_date , "words": find_words()}


all_db_docs =  db_services.check_db(db_connection)[0]

document_data = []
for doc in all_db_docs:
    document_data.append(doc)

for i in range(len(document_data)):
    for j in range(i +1, len(document_data)):
        if document_data[i] == document_data[j]:
            print(f"Duplicate found between Document {i + 1} and Document {j + 1}.")


insert_my_data = db_services.insert_data(db_connection, insert_collection = 'spellingbee-found-words',payload = payload_data, document_id=formatted_date)
print(all_db_docs)
        
if __name__ == '__main__':
    insert_my_data = db_services.insert_data(db_connection, insert_collection = 'spellingbee-found-words',payload = payload_data, document_id=formatted_date)

    app.run()