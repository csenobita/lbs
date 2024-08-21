import cv2
import face_recognition
import pickle
import os

FolderModePath = 'photo'
imgHeroPath = os.listdir(FolderModePath)
imgItem = []
student_id = []

for path in imgHeroPath:
    img = cv2.imread(os.path.join(FolderModePath, path))
    if img is not None:
        imgItem.append(img)
        student_id.append(os.path.splitext(path)[0])
    else:
        print(f"Warning: Unable to read image {path}")

def face_encoding(imgItem):
    encoding_list = []
    for img in imgItem:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img_rgb)
        if encodings:
            encoding_list.append(encodings[0])
        else:
            print("No faces found in image.")
    return encoding_list

print("Encoding Start")
encoding_data = face_encoding(imgItem)
encoding_list_id_encoding = [encoding_data, student_id]
print("Encoding Complete")

with open("encoding_data.p", mode='wb') as file:
    pickle.dump(encoding_list_id_encoding, file)
print('File saved')
