import cv2
import sys

#cascPath = "palm.xml"
cascPath = "closed_frontal_palm.xml"
#cascPath = "lbpcascade_profileface.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if(len(faces)==1):
        x,y,w,h =faces[0]
        cv2.rectangle(frame,(x ,y),(x+w,y+h),(0,255,0),2)


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()