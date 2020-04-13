import firebase_admin as db
from Tools.scripts import google
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('ServiceAccountKey.json')
db.initialize_app(cred)

db = firestore.client()

def getUID():
    print("indise getUID")
    doc_ref = db.collection(u'LatestUID').document(u'uID')

    try:
        doc = doc_ref.get()
        a = format(doc.to_dict())
        s = convertToString(a)
        # print(s)
        print("getUID Done")
        return s
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')


def setUID(uID):
    doc_ref = db.collection(u'LatestUID').document(u'uID')
    doc_ref.set({
        u'uID': uID,
    })

def convertToString(a):
    l1 = a.split()
    s = l1[1][1:(len(l1[1]) - 2)]
    return s



# getUID()
# setUID("1234")