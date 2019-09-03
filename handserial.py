# -*- coding:; utf-8 -*-
"""
handserial.py

Sends commands to Arduino Uno via serial port to control a drone
according to gestures tracked by OpenCV and Cascade Classifier
using the nRF24L01 wireless boards.

This uses the msvcrt library, so it only works under Windows. 

Created on Monday Sept 02 2019

@author: Pranshu Tople

"""
import serial, time, msvcrt
import cv2
import sys

#cascPath = "palm.xml"
cascPath = "closed_frontal_palm.xml"
#cascPath = "lbpcascade_profileface.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

throttle=1000
aileron=1500
elevator=1500
rudder=1500 # yaw, rotates the drone

mode = 1

tg=10
ag=50
eg=50
rg=50
try:
    arduino=serial.Serial('COM17', 115200, timeout=.01)
    time.sleep(1) #give the connection a second to settle
    #arduino.write("1500, 1500, 1500, 1500\n")
    
    while True:

        data = arduino.readline()
        if data:
            #String responses from Arduino Uno are prefaced with [AU]
            print "[AU]: "+data 
        
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

     

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            xpos=x+(w/2)
            
            ypos=y+(h/2)

            eqy=((-2)*ypos)+2000

            eqx=((1.6)*xpos)+1000


            if (mode==1):
                throttle=1100
                command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
                # string commands to the Arduino are prefaced with  [PC]           
                print "[PC]: "+command 
                arduino.write(command+"\n")
                mode=mode+1

            throttle=eqy
            aileron=eqx

            command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
            # string commands to the Arduino are prefaced with  [PC]           
            print "[PC]: "+command 
            arduino.write(command+"\n")

        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            throttle=1000
            aileron=1500
            elevator=1500
            rudder=1500
            command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
            # string commands to the Arduino are prefaced with  [PC]           
            print "[PC]: "+command 
            arduino.write(command+"\n")
            break

        if cv2.waitKey(1) & 0xFF == ord('k'):
            throttle=1000
            aileron=1500
            elevator=1500
            rudder=1500
            command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
            # string commands to the Arduino are prefaced with  [PC]           
            print "[PC]: "+command 
            arduino.write(command+"\n")

finally:
    # close the connection
    video_capture.release()
    cv2.destroyAllWindows()
    arduino.close()
    # re-open the serial port which will also reset the Arduino Uno and
    # this forces the quadcopter to power off when the radio loses conection. 
    arduino=serial.Serial('COM17', 115200, timeout=.01)
    arduino.close()
    # close it again so it can be reopened the next time it is run.  