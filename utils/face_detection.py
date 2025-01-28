# utils/face_detection.py
import face_recognition

def detect_faces(imgS):
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    return facesCurFrame, encodesCurFrame
