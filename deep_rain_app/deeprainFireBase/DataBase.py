import firebase_admin
from firebase_admin import credentials, firestore, storage
import sched
import time
from random import randrange
from datetime import datetime

#
# creats example rain forecast data. upload this data to firebase. every 5 minutes one dataset.
#

if __name__ == '__main__':
    cred = credentials.Certificate('./deeprain-firebase-adminsdk-xpcbj-bcbc99b37e.json')
    default_app = firebase_admin.initialize_app(cred, {'storageBucket': 'deeprain.appspot.com'})
    bucket = storage.bucket()
    db = firestore.client()

    s = sched.scheduler(time.time, time.sleep)

    # Counter for the ID of Data
    ID = 0

    # list with all stored ids
    IDList = []

    def upload_data_to_firbase(sc):
        global ID
        # the current time for firebase document ID
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        # the unique id for the documents of database.
        documentID = 'deeprain_' + current_time + '_' + str(ID)
        IDList.append(documentID)

        # random dummy rainintense
        rainIntense = randrange(100)
        rainIntense = 94

        # upload to firebase
        doc_ref = db.collection('forecast').document(str(documentID))
        doc_ref.set({
            'rainIntense': rainIntense,
            'time': current_time
        })

        # send push notifications to devices.
        if(rainIntense > 90):
            doc_ref = db.collection('RainWarningPushNotification').document(str(documentID))
            doc_ref.set({
                'title': 'Es gibt eine Regenwarnung!',
                'body': 'Nehmen Sie besser Ihren Regenschirm mit, es wird in 30 Minuten regenen!',
                'time_before_raining': '30'
            })

        # increase the ID
        ID = ID + 1
        print('Upload erfolgeich. ID:' + str(ID) + '. rainIntense: ' + str(rainIntense) + '. time: ' + str(current_time))

        # if there are 20 items in the db, alway remove the oldest one
        if len(IDList) > 19:
            # delete in firebase
            db.collection("forecast").document(IDList[0]).delete()
            # delete from local  id list
            IDList.pop(0)

        s.enter(10, 1, upload_data_to_firbase, (sc,))
    s.enter(10, 1, upload_data_to_firbase, (s,))
    s.run()

