def upload_cam_one_list(list, first):
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    if first:
        cred = credentials.Certificate('ServiceAccountKey.json')
        firebase_admin.initialize_app(cred)

    print("Inside uploadCamOneList")
    db = firestore.client()
    doc_ref = db.collection(u'Camera One').document(u'UserList')
    doc_ref.set({
        u'Details': list,
    })
    print('---------------------- Uploaded Data to Data Base --------------------------')