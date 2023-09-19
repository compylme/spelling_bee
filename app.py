from flask import Flask
import nltk
from nltk.corpus import words
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('service-account-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
collection_ref = db.collection('spellingbee-letters-docker')
docs = collection_ref.stream()

app = Flask(__name__)
app.debug = True \

nltk.download('words')
all_words = words.words()
list_of_words = []
list_of_letters = ['g','n','l','e','u','i','v']
constant = 'v'
word_values = None
four_plus = []
unwanted_words = []
the_words = []
doc_ids = []

@app.route("/")
def hello_world():
    return "Hello, :)</p>"

@app.route("/docs")
def collection_data():
    for doc in docs:
        doc_ids.append(doc.id)

    return doc_ids



@app.route("/nltk")
def math():
    list_dict = {letter: [] for letter in list_of_letters}

    for word in all_words:
        if word[0] in list_of_letters:
            list_dict[word[0]].append(word)

    for each in list_dict.values():
        for word in each:
            if len(word) > 3 and constant in word:
                four_plus.append(word)

    for word in four_plus:
        for letter in word:
            if letter not in list_of_letters:
                unwanted_words.append(word)

    set1 = set(four_plus)
    set2 = set(unwanted_words)

    difference = set1 - set2
    
    return str(difference)

app.run()