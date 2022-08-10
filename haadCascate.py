from __future__ import print_function
from __future__ import print_function
import cv2 as cv
import argparse

def detectAndDisplay(frame, face_cascade, eyes_cascade):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        frame =  cv.rectangle(frame, (x,y), (x+w,y+h),(255,0,0),2)
        faceROI = frame_gray[y:y+h,x:x+w] 
        eyes = eyes_cascade.detectMultiScale(faceROI)
        cv.putText(frame,"ROSTO",(x+w//2+1,y+h+25),cv.FONT_HERSHEY_DUPLEX,1,(255,0,0))
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            frame = cv.rectangle(frame, (x+x2,y+y2), (x+x2+w2,y+y2+h2),(0,255,0),2)
            cv.putText(frame,"OLHO",(x+x2+w2//2+1,y+y2+h2+25),cv.FONT_HERSHEY_DUPLEX,1,(0,255,0))
    cv.imshow('Capture - Face detection', frame)
def goDetect(camera):
    parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
    parser.add_argument('--face_cascade', help='Path to face cascade.', default=cv.samples.findFile('haarcascade_frontalface_alt2.xml'))
    parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default=cv.samples.findFile('haarcascade_eye_tree_eyeglasses.xml'))
    parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
    args = parser.parse_args()
    face_cascade_name = args.face_cascade
    eyes_cascade_name = args.eyes_cascade
    face_cascade = cv.CascadeClassifier()
    eyes_cascade = cv.CascadeClassifier()
    #-- 1. Load the cascades
    if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
        print('--(!)Error loading face cascade')
        exit(0)
    if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
        print('--(!)Error loading eyes cascade')
        exit(0)
    #-- 2. Read the video stream
    if not camera.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    while True:
        ret, frame = camera.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        detectAndDisplay(frame, face_cascade, eyes_cascade)
        if cv.waitKey(10) == 27:
            break
