from face_rec import *
import cv2
import os
import requests
import base64
import pickle
import json
import time

register = Register()

for img in os.listdir('known_faces'):
    name = os.path.splitext(img)[0]
    print("Known face : {}".format(name))
    register.register_user(name, os.path.join('known_faces', img))

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

url = 'http://localhost:5001/predict'

video_capture = cv2.VideoCapture(0)

while True:

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        time.sleep(1)
        try :
            # face_locations, face_names = Predict.get_predictions(rgb_small_frame, register)
            serialized = pickle.dumps(rgb_small_frame)
            # data_json = {"frame": base64.b64encode(serialized)}
            response = requests.post(url=url, data=base64.b64encode(serialized))
            # help(response)
            face_locations, face_names = pickle.loads(base64.b64decode(response.text))
        except:
            continue

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 20), font, 1.0, (0, 0, 255), 1)


    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
