import os
import pickle
import cv2
import face_recognition
import time

# Initialize webcam
cam = cv2.VideoCapture(0)
cam.set(3, 320)  # Set width
cam.set(4, 240)  # Set height

# Load background image
background_img = cv2.imread("BBPI_back.png")

# Load mode images
FolderModePath = 'mode'
imgModePath = os.listdir(FolderModePath)
imgModes = [cv2.imread(os.path.join(FolderModePath, path)) for path in imgModePath]

print('Encode file Opening ......')
with open('endcoding_data.p', 'rb') as file:
    imge_endcode_data, student_id = pickle.load(file)

print('Encode file loading .......')

frame_rate = 15  # Process 15 frames per second
prev_time = 0

while True:
    current_time = time.time()
    if current_time - prev_time >= 1. / frame_rate:
        prev_time = current_time

        ret, img = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Resize and convert the image for face recognition
        imgs = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgs)
        encodeFrame = face_recognition.face_encodings(imgs, faceCurFrame)

        if encodeFrame:
            for encoface, faceloc in zip(encodeFrame, faceCurFrame):
                matchs = face_recognition.compare_faces(imge_endcode_data, encoface)
                face_dis = face_recognition.face_distance(imge_endcode_data, encoface)
                print("matches:", matchs)
                print("face distances:", face_dis)
        else:
            print("No faces detected")

        # Resize the webcam image to 450x350
        resized_img = cv2.resize(img, (450, 350))

        # Define the position and size where the webcam image will be placed on the background
        start_x, start_y = 200, 300
        end_x, end_y = start_x + 450, start_y + 350
        m_start_x, m_start_y = 770, 260
        m_img_w, m_img_h = 350, 444
        m_end_x, m_end_y = m_start_x + m_img_w, m_start_y + m_img_h

        # Ensure the background image is large enough to accommodate the overlay
        if end_x <= background_img.shape[1] and end_y <= background_img.shape[0]:
            # Overlay the resized webcam image onto the background image
            background_img[start_y:end_y, start_x:end_x] = resized_img
            if imgModes:
                background_img[m_start_y:m_end_y, m_start_x:m_end_x] = imgModes[0]

        # Display the result
        cv2.imshow("background_img", background_img)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(10) == ord("q"):
            break

# Release resources
cam.release()
cv2.destroyAllWindows()
