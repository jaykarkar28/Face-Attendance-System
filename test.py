# PART 2 : RECOGNITION


from sklearn.neighbors import KNeighborsClassifier

import cv2
import pickle
import numpy as np
import os
import csv
import time
from _datetime import datetime
from win32com.client import Dispatch


# for speak
def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# for creating frame and video capture

# Create Attendance directory if it doesn't exist
os.makedirs('Attendance', exist_ok=True)

video = cv2.VideoCapture(0)  # For Webcam in laptop
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # by defult for image recognition

with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)

with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# KNN classifier object call

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Background
img_background = cv2.imread('background.png')

# for Data in csv
COL_NAMES = ['NAME','TIME']

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame,
                        cv2.COLOR_BGR2GRAY)  # used to conver RBG color to gray so it can easily predict by haarcascade

    # For Face Detection
    faces = facedetect.detectMultiScale(gray, 1.3, 5)  # get the coordinate value from the faces (X,Y,H,W)

    current_attendances = []

    #  For Finding X,Y,H,W
    for (x, y, w, h) in faces:
        # Crop the images from rectangle frame
        crop_img = frame[y:y + h, x:x + w, :]  # [y to y+h, X to X+W , All number of channel (100x100)]

        resize_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)  # Reshape picture

        output = knn.predict(resize_img)  # Make the Prediction

        # FOR DATE AND TIME
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        # Check If Any Current Date's Attendance file is exist or not
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

        # For the highliting name
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)

        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # (original frame,(Coordinate Value),(width and height of channel),(Color),(thickness))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

        #  For Taking Attendance
        current_attendances.append([str(output[0]), str(timestamp)])

    #  Set Background
    img_background[162:162 + 480,55:55+640] = frame

    cv2.imshow('frame', img_background)
    k = cv2.waitKey(1)  # Breaking infinite loop

    if k == ord('o') or k == ord('O'):
        if len(current_attendances) > 0:
            names_recognized = ", ".join([att[0] for att in current_attendances])
            speak("Attendance taken.. Hello " + names_recognized)
            time.sleep(1)
            
            with open('Attendance/Attendance_' + date + '.csv', '+a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not exist:
                    writer.writerow(COL_NAMES)
                for att in current_attendances:
                    writer.writerow(att)


    if k == ord('q') or k == ord('Q'):
        break

video.release()
cv2.destroyAllWindows()
