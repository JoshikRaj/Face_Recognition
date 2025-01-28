# utils/attendance.py
import os
from datetime import datetime

activePersons = {}

def markAttendance(name, status):
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now()
    timeNow = now.strftime('%H:%M:%S')

    if not os.path.exists('Attendance.csv'):
        print("Creating Attendance.csv")
        with open('Attendance.csv', 'w') as f:
            f.write('Name,Date,Entry Time,Exit Time\n')

    if status == "enter":
        if name not in activePersons:
            activePersons[name] = now
            print(f"{name} entered at {timeNow}")

    elif status == "exit":
        if name in activePersons:
            entryTime = activePersons.pop(name).strftime('%H:%M:%S')
            print(f"{name} exited at {timeNow} (Entry: {entryTime})")
            with open('Attendance.csv', 'a') as f:
                f.write(f"{name},{today},{entryTime},{timeNow}\n")
