# main.py

from utils.image_processing import load_images, find_encodings
from utils.attendance import markAttendance
from utils.face_detection import detect_faces
import cv2
import face_recognition 
import numpy as np

def face_recognition_logic(encodeListKnown, encodeFace, classNames):
    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    matchIndex = np.argmin(faceDis)

    if matches[matchIndex]:
        name = classNames[matchIndex].upper()
        return matches, matchIndex, name
    else:
        return matches, matchIndex, None

def main():
    path = './student_images'
    images, classNames = load_images(path)
    encodeListKnown = find_encodings(images)
    print('Encoding Complete. Total Encoded Faces:', len(encodeListKnown))

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    prev_detected = set()  # Track previously detected people in the frame

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture image from webcam.")
            break

        # Resize and process the frame for faster performance
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame, encodesCurFrame = detect_faces(imgS)

        current_detected = set()  # Track currently detected people in the frame

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches, matchIndex, name = face_recognition_logic(encodeListKnown, encodeFace, classNames)

            if matches[matchIndex]:
                current_detected.add(name)

                # If the person is newly detected, mark as "enter"
                if name not in prev_detected:
                    markAttendance(name, "enter")

                # Draw bounding box and name
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # Detect people who exited
        for name in prev_detected - current_detected:
            markAttendance(name, "exit")

        prev_detected = current_detected

        # Show the result
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting program.")
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
