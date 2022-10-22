

import cv2 as cv
#import face_recognition

video_thing = cv.VideoCapture(0)

ret, image = video_thing.read()

var = "image.png"
save_file = open(var, "xb")
cv.imwrite(var, image)