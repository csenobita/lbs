import cv2
import numpy as np
cam=cv2.VideoCapture(0)
cyan_lower = np.array([80, 100, 100])
cyan_upper = np.array([100, 255, 255])
prev_y=0
prev_x=0
while True:
    ret,frame=cam.read()
    if ret:
        hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv, cyan_lower, cyan_upper)
        contours,hierarchy =cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area=cv2.contourArea(c)
            if area>950:
                #cv2.drawContours(frame, contours, -1, (0, 255, 0))
                #print(area)
                x,y,w,h=cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                if y> prev_y:
                    print('moving up')
                elif y<prev_y:
                    print('moving down')
                elif x<prev_x:
                    print('moving right')
                elif x>prev_x:
                    print("moving left")


                prev_y=y
                prev_x=x
        cv2.imshow('Webcam ',frame)
        if cv2.waitKey(10) == ord("q"):
            break
    else:
        print('NONE')
cam.release()