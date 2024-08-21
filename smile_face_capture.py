import cv2
import mediapipe as mp


fase_mask=mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cam=cv2.VideoCapture(0)

while True:
    ret,img=cam.read()
    img=cv2.flip(img,1)
    img_w,img_h,_= img.shape
    if ret:
        rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        output= fase_mask.process(rgb_img)
        landmark_poins=output.multi_face_landmarks
        if landmark_poins:

            landmarks=landmark_poins[0].landmark
            for id,landmark in enumerate(landmarks):
                x=int(landmark.x * img_w)
                y=int(landmark.y * img_h)
                print(x,y)
        cv2.imshow("Fase_cam",img)
        if cv2.waitKey(10)==ord("q"):
            break
cam.release()
cv2.destroyAllWindows()