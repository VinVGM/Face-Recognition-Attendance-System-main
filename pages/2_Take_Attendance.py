import streamlit as st
import pandas as pd
import cv2 
import tempfile
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle


path = 'pages/student_images'

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList


def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'n{name}, {time}, {date}')




def update_status(register_number):
    # Read the CSV file
    df = pd.read_csv("attendance_register.csv")
    
    # Check if 'Status' column exists, if not create one with 'Absent'
    if 'Status' not in df.columns:
        df['Status'] = 'Absent'
    else:
        # Update the 'Status' to 'Absent' where 'Status' is NaN
        df.loc[df['Status'].isna(), 'Status'] = 'Absent'
    
    # Update the 'Status' of the given 'Register Number' to 'Present'
    df.loc[df['Register Number'] == register_number, 'Status'] = 'Present'
    
    # Write the updated DataFrame back to the CSV file
    df.to_csv("attendance_register.csv", index=False)

    print(f"Status updated for Register Number: {register_number}")


press = st.warning("Wait for the system to load")




images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

encoded_face_train = findEncodings(images)

cap = cv2.VideoCapture(0)
frame_placeholder = st.empty()
stop_button_pressed = st.button("Stop")


while cap.isOpened() and not stop_button_pressed:
    
    
    
    
    

    

    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)
        print(matchIndex)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper().lower()
            y1,x2,y2,x1 = faceloc
            # since we scaled down by 4 times
            y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
            
            update_status(name.upper())
            break
    imgo = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(imgo)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # ret, img = cap.read()
    # if not ret:
    #     st.write("Video Capture Ended")
    #     break
    # imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    

    # faces_in_frame = face_recognition.face_locations(imgS)
    # encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    # for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
    #     matches = face_recognition.compare_faces(encoded_face_train, encode_face)
    #     faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
    #     matchIndex = np.argmin(faceDist)
    #     print(matchIndex)
    #     if matches[matchIndex]:
    #         name = classNames[matchIndex].upper().lower()
    #         y1,x2,y2,x1 = faceloc
    #         # since we scaled down by 4 times
    #         y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
    #         cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
    #         cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
    #         cv2.putText(img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    #         markAttendance(name)
    #         break
    # frame_placeholder.image(img,channels="RGB")
    # if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
    #     break
cap.release()
cv2.destroyAllWindows()