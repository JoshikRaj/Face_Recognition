# utils/image_processing.py
import cv2
import os
import face_recognition

def load_images(path):
    images = []
    classNames = []
    
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        exit()

    myList = os.listdir(path)
    print("Images found:", myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        if curImg is not None:
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        else:
            print(f"Warning: Unable to read image '{cl}'. Skipping.")
    
    return images, classNames

def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("Warning: Face not detected in one of the images. Skipping.")
    return encodeList
