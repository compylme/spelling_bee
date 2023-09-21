from flask import Flask, jsonify
import nltk
from nltk.corpus import words
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import date, datetime

# Initialize Flask app
app = Flask(__name__)
app.debug = True

# Initialize NLTK words
nltk.download('words')
all_words = set(words.words())

# Initialize Firebase Admin SDK
cred = credentials.Certificate('service-account-key.json')
firebase_admin.initialize_app(cred)

startTimestamp = datetime(2023, 9, 18, 21, 45, 27, 60)
formatted_date = startTimestamp.strftime("%b %d, %Y, %I:%M:%S.%f %p")

# Initialize Firestore
db = firestore.client()
query = db.collection('spellingbee-letters-docker') \
    .order_by('timestamp').limit_to_last(1)
docs = query.get()

# Define global variables
list_of_letters = []
constant = ''

@app.route("/")
def hello_world():
    return "Hello, :)</p>"

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
            constant=each
    return list_of_letters, constant

new_data = collection_data()
print(new_data)
fetched_data = order_letters(new_data)
print(fetched_data)

@app.route("/nltk")
def find_words():
    
    print('list of letters:'+ str(list_of_letters))
    list_dict = {letter: [] for letter in list_of_letters}

    # Create a dictionary of words starting with each letter
    for word in all_words:
        if word[0] in list_of_letters:
            list_dict[word[0]].append(word)

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

    return jsonify(difference)

if __name__ == '__main__':
    app.run()
