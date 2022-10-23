import face_recognition
import cv2
import numpy as np
import time
from app.db import db, User
from flask import Flask, render_template, redirect, request, Blueprint, session, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user




all_users = db.session.query(User).filter(User.face_image!=None).all()

known_face_encodings = [
]
known_face_names = [
]
for one_user in all_users:
    known_face_names.append(current_user.name)
    obama_image = face_recognition.load_image_file(f"app/video/images/{current_user.block_id}.png")
    first_face = face_recognition.face_encodings(obama_image)[0]
    known_face_encodings.append(first_face)



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


camera = cv2.VideoCapture(0)
time.sleep(2)
ret, frame = camera.read()

if process_this_frame:
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unrecognized"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]


        face_names.append(name)




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
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

# Display the resulting image
while True:
    cv2.imshow('Video', frame)

    cv2.waitKey(1)

    if 0xFF == ord('q'):
        cv2.destroyAllWindows()

video_capture.release()
cv2.destroyAllWindows()
