import cv2
import os
import numpy as np
from sklearn import preprocessing
import random
from uploadCamOneList import upload_cam_one_list
from getUnique import unique


# using Haar Cascade for face detection
# loading face cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# dataset location
dataset_folder_path = 'Dataset'


def detect_face(image):
    # converts the picture from RGB color to gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    if len(faces) != 0:
        (x, y, w, h) = faces[0]
        return gray_image[y:y + w, x:x + h], faces[0]
    else:
        return None, None


def prep_dataset(dataset_folder_path):
    labels = []
    encoded_labels = []
    faces = []
    subjects = []

    # used for label encoding
    le = preprocessing.LabelEncoder()

    # traversing folder
    for names in os.listdir(dataset_folder_path):
        # joining paths
        name_folder = os.path.join(dataset_folder_path, names)
        for images in os.listdir(name_folder):
            img = os.path.join(name_folder, images)
            # loading image
            image = cv2.imread(img)
            face, rect = detect_face(image)
            if face is not None:
                faces.append(face)
                labels.append(names)

    # randomizing lists
    c = list(zip(faces, labels))
    random.shuffle(c)
    faces, labels = zip(*c)

    # fitting labels in label encoding model of sklearn
    le.fit(labels)

    #  unique classes
    subjects = le.classes_

    # transforming into encoded labels
    encoded_labels = le.transform(labels)

    return faces, subjects, encoded_labels


def recognize_realtime():
    faces, subjects, encoded_labels = prep_dataset(dataset_folder_path)
    listOfUsers = []
    # using LBPHF model of opencv for face recognition

    countEmptyFrames = 0
    isFirst = True;

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # training model
    face_recognizer.train(faces, np.array(encoded_labels))

    # capturing video feed from the only webcam the system has
    vid = cv2.VideoCapture(0)
    while True:

        # returns two parameters-1.'ret' contains the returned boolean value if the frame is read correctly.2. 'frame' contains the frame
        ret, frame = vid.read()

        # converts the frame from RGB color to gray
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        # looping on each face with 'x','y' co-ordinate and 'w' & 'h' which denotes width and height respectively.
        if len(faces) == 0:
            countEmptyFrames = countEmptyFrames +1

        if countEmptyFrames > 100:
            countEmptyFrames = 0
            upload_cam_one_list([], isFirst)
            isFirst = False

        for (x, y, w, h) in faces:
            face_image = gray_frame[y:y + w, x:x + h]

            # predicting label
            label, confidence = face_recognizer.predict(face_image)

            print(subjects[label])
            print(confidence)
            # drawing a rectangle around the face. (0,255,0) denotes color 'green' & '2' is line width.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # predicted label is only shown if confidence is less than 120 (lesser is better)
            # this is done to prevent prediction on untrained faces.
            if confidence < 100:
                # decoding label
                label_text = subjects[label]
                countEmptyFrames = 0
                listOfUsers.append(label_text)
                # inserting bound label text
                cv2.putText(frame, label_text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

        # cv2.imshow() to display a frame in a window.
        cv2.imshow('Video', frame)

        if len(listOfUsers) > 9:
            print("length is 10")
            #listOfUsers2 = []
            listOfUsers2 = unique(listOfUsers, len(faces))
            upload_cam_one_list(listOfUsers2, isFirst)
            isFirst = False
            listOfUsers.clear()
            listOfUsers2.clear()
        # this line is used to wait for a key event for each millisecond that should be equal to 'a'.
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break

    # closes the camera
    vid.release()

    # destroys frame window
    cv2.destroyAllWindows()


recognize_realtime()
