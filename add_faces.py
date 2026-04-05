import cv2
import pickle
import numpy as np
import os

# PART 1 : DATA COLLECTION

# for creating frame and video capture

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

video = cv2.VideoCapture(0)   # For Webcam in leptop
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')   # by defult for image recognition

i=0
faces_data = []   # Empty list for store faces

import sys

# for assign the name of person
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Enter your name: ")


while True:
    ret,frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # used to conver RBG color to gray so it can easily predict by haarcascade

    # For Face Detection
    faces = facedetect.detectMultiScale(gray,1.3,5) # get the coordinate value from the faces (X,Y,H,W)

    #  For Finding X,Y,H,W
    for (x,y,w,h) in faces:

        # Crop the images from rectangle frame
        crop_img = frame[y:y+h,x:x+w, :]  #[y to y+h, X to X+W , All number of channel (100x100)]

        resize_img = cv2.resize(crop_img,(50,50)) #Resize the Crop Images

        # Put the resized image into face data list
        # take  up to 100 picture at a time  and after 10 frame it can take picture
        if len(faces_data) <100 and i%10==0:
            faces_data.append(resize_img)
        i+=1

        # shows how many picture is detected        (coordinate,Font,thickness,Color)
        cv2.putText(frame,str(len(faces_data)),(50,50),cv2.FONT_HERSHEY_DUPLEX, 1 , (50,50,255))

        # (original frame,(Coordinate Value),(width and height of channel),(Color),(thickness))
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),1)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)   # Breaking infinite loop

    if k == ord('q') or len(faces_data) >= 100:
        break

video.release()
cv2.destroyAllWindows()

#  Convert Data into numpy array
faces_data = np.array(faces_data)
faces_data = faces_data.reshape(100,-1) # Reshape the array data so it can easily be used by ML model


#  For the Name
if 'names.pkl' not in os.listdir('data/'):
    names = [name]*100
    with open('data/names.pkl','wb') as f:
        pickle.dump(names, f)

else:
    with open('data/names.pkl','rb') as f:
        names = pickle.load(f)
    names = names + [name] * 100   # When multiple faces with same name is come (overwrite)

    # Dump again bcz new name is added
    with open('data/names.pkl','wb') as f:
        pickle.dump(names, f)



#  For the Faces
if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl','wb') as f:
        pickle.dump(faces_data, f)

else:
    with open('data/faces_data.pkl','rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)

    # Dump again bcz new name is added
    with open('data/faces_data.pkl','wb') as f:
        pickle.dump(faces, f)



