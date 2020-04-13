def upload_new_user_details(uID , uData):
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore




    uData.append(uID)




    #cred = credentials.Certificate('ServiceAccountKey.json')
    #firebase_admin.initialize_app(cred)

    db = firestore.client()
    doc_ref = db.collection(u'UserDetails').document(u'"%s"' % uID)
    doc_ref.set({
        u'Details': uData,
    })




# example of data to upload First variable is the UNIQUE USER ID, second parameter is the USER DETAILS
# from uploadNewUserDetails import upload_new_user_details
# upload_new_user_details("000", ["Gourav Dutta", "Male", "24", "FlatNo - 204", "891007789", "0+", "5.5"])
