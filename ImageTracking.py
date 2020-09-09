import numpy as np
import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)
FaceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while(True):
    a = datetime.now()
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = FaceCascade.detectMultiScale(gray,1.1,10)
    for (x,y,w,h) in faces:
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0.255),2)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    b = datetime.now()
    #calculates fps
    c = b - a
    seconds = c.total_seconds()
    fps = 1/seconds
    print(fps,end='\r')

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()