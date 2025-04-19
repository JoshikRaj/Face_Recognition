import cv2
import numpy as np
import face_recognition
import os
import geocoder  # Added for location tracking
from datetime import datetime

# Path to the local folder containing student images
path = './student_images'  # Make sure this folder contains images
images = []
classNames = []

# Ensure the path exists and contains images
if not os.path.exists(path):
    print(f"Error: Path '{path}' does not exist.")
    exit()

# List all files in the folder
myList = os.listdir(path)
if not myList:
    print("Error: No images found in the folder.")
    exit()

print("Images found:", myList)

# Load images and class names
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    else:
        print(f"Warning: Unable to read image '{cl}'. Skipping.")

print("Class Names:", classNames)

# Function to encode the images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("Warning: Face not detected in one of the images. Skipping.")
    return encodeList

# Dictionary to track active people with their entry time
activePersons = {}

# Function to get current latitude & longitude
def get_location():
    try:
        g = geocoder.ip('me')  # Fetch location based on IP
        return g.latlng if g.latlng else ("Unknown", "Unknown")
    except Exception as e:
        print(f"Error fetching location: {e}")
        return ("Unknown", "Unknown")

# Function to mark attendance with location
def markAttendance(name):
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now()
    timeNow = now.strftime('%H:%M:%S')

    latitude, longitude = get_location()  # Get location

    # Check if attendance file exists; create if not
    if not os.path.exists('Attendance.csv'):
        print("Creating Attendance.csv")
        with open('Attendance.csv', 'w') as f:
            f.write('Name,Date,Entry Time,Latitude,Longitude\n')  # Added new columns

    # If a person is detected and enters
    if name not in activePersons:
        activePersons[name] = now  # Store entry time
        print(f"{name} entered at {timeNow}, Location: ({latitude}, {longitude})")

        # Write attendance details to the file
        with open('Attendance.csv', 'a') as f:  # Open file in append mode
            f.write(f'{name},{today},{timeNow},{latitude},{longitude}\n')  # Write the attendance

# Encode known faces
encodeListKnown = findEncodings(images)
print('Encoding Complete. Total Encoded Faces:', len(encodeListKnown))

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture image from webcam.")
        break

    # Resize and process the frame for faster performance
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            markAttendance(name)  # Mark attendance

            # Draw bounding box and name
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('Webcam', img)
            cv2.waitKey(3000)  # Show the recognized frame for 3 seconds

            print(f"Recognized {name}. Exiting program.")
            cap.release()  # Release webcam
            cv2.destroyAllWindows()  # Close OpenCV windows
            exit()  # Stop execution

    # Show the frame
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting program.")
        break

# Release resources if loop exits
cap.release()
cv2.destroyAllWindows()
