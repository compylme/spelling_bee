import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import datetime
import pytz

insert_collection = 'spellingbee-found-words'
retrieve_collection = 'spellingbee-letters-docker'
document_id = uuid.uuid4()

class myTimezones:
    
    def ukTime():
        ukTimezone = pytz.timezone('Europe/London')
        current_date = datetime.datetime.now(ukTimezone)
        formatted_time = current_date.strftime("%Y/%m/%d")
        formatted_date = str(formatted_time).replace("-", "/")

        return formatted_date
    
    def timeStamp():
        return datetime.datetime.now()



class db_services():

    def __init__(self):
        cred = credentials.Certificate('service-account-key.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_data(self):
        query = self.db.collection(retrieve_collection) \
            .order_by('timestamp').limit_to_last(1)
        docs = query.get()

        return docs
    
    def insert_data(self, insert_collection, payload, document_id=uuid.uuid4()):
        try:
            collection = self.db.collection(insert_collection)
            document_ref = collection.document(document_id)
            document_ref.set(payload)
            print("Data inserted successfully into DB")
        except Exception as e:
            print("An error has occured", str(e))


