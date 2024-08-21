import cv2
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)


while True:
    ret,img=cam.read()
    if ret:
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.5, 4)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

        cv2.imshow("face-recon", img)
        if cv2.waitKey(10) == ord('q'):
            break
cam.release()
cv2.destroyAllWindows()