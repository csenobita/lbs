import cv2
import mediapipe as mp

# Initialize webcam
cam = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
my_hands = mp_hands.Hands()

# Variables to store coordinates of the index finger and thumb tips
x1, y1 = 0, 0
x2, y2 = 0, 0

while True:
    ret, img = cam.read()
    if ret:
        img_h, img_w, _ = img.shape  # Correctly unpack the height and width

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        output = my_hands.process(rgb_img)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                #mp_drawing.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
                landmarks = hand.landmark

                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * img_w)
                    y = int(landmark.y * img_h)

                    # Detect index finger tip (landmark 8) and thumb tip (landmark 4)
                    if id == 8:
                        cv2.circle(img, (x, y), 5, (255, 255, 255), 3)  # Draw a circle
                        x1, y1 = x, y
                    if id == 4:
                        cv2.circle(img, (x, y), 5, (255, 255, 255), 3)
                        x2, y2 = x, y

                # Draw a line between the index finger tip and thumb tip
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        # Display the image
        cv2.imshow('hand_gesture_volume_control', img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(10) == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
