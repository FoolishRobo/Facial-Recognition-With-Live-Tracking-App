import os
import cv2
from getSetUID import getUID, setUID
from uploadNewUserDetails import upload_new_user_details

# using Haar Cascade for face detection
# loading face cascade
dataset_path_name = "Dataset"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# capturing video feed from the only web cam the system has
vid = cv2.VideoCapture(0)
image_size = (200,200)
i = 0

uData = [None] * 6
uData[0] = input("enter your name : ")
uData[1] = input("enter your gender : ")
uData[2] = input("enter your age : ")
uData[3] = input("enter your address : ")
uData[4] = input("enter your phone number : ")
uData[5] = input("enter your blood group : ")

uID = str(int(getUID()) + 1)
setUID(uID)

folderName = uID

upload_new_user_details(uID, uData)

os.mkdir(os.path.join(dataset_path_name, folderName))
print("Folders created")

while True:
	# returns two parameters -
	# 1.'ret' contains the returned boolean value if the frame is read correctly.
	# 2. 'frame' contains the frame itself

	ret, frame = vid.read()

	# converts the frame from RGB color to gray

	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

	# looping on each face with 'x','y' co-ordinate and 'w' & 'h' which denotes width and height respectively.
	# for (x,y,w,h) in faces:

	# drawing a rectangle around the face. (0,255,0) denotes color 'green' & '2' is line width.

	# cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

	# cv2.imshow() to display a frame in a window.
	for (x, y, w, h) in faces:
		# drawing a rectangle around the face. (0,255,0) denotes color 'green' & '2' is line width.
		img_resized = cv2.resize(gray_frame[y:y + w, x:x + h], image_size)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imshow('Video', frame)

	if len(faces) != 0:
		y = str(i) + '.png'
		n = os.path.join(folderName, y)
		print(os.path.join(dataset_path_name, n))
		cv2.imwrite(os.path.join(dataset_path_name, n), img_resized)
		i = i + 1

	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('a'):
		break
	if i >= 500:
		break


# closes the camera
vid.release()

# destroys frame window
cv2.destroyAllWindows()

