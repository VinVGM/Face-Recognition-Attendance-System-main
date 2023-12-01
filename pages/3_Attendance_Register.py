import streamlit as st
from streamlit import components
import pandas as pd
import cv2
import tempfile
import os



def save_image(img, path='student_images', img_name='webcam_image.jpg'):
    cv2.imwrite(os.path.join(path, img_name), img)




def main():

    st.set_page_config(
    page_title="Attendace Register Database Mangaement",
    
    )
    st.sidebar.header("Create your Class Attendance Register")
    
    FRAME_WINDOW = st.image([])

    

    # Load existing data or create an empty DataFrame
    try:
        df = pd.read_csv("attendance_register.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Register Number", "Student Name"])
    col1,col2 = st.columns([0.5,0.5])
    # Input form to add students to the register
    with col1:
        st.title("Attendance Register")
        register_number = st.text_input("Enter Register Number:")
        student_name = st.text_input("Enter Student Name:")
        press = st.button("Add to register")


  
        if press:
          while True:  
            if register_number and student_name:
                # Check if the register number already exists
                if register_number in df["Register Number"].values:
                    st.warning("Register number already exists. Please enter a unique register number.")
                    break
                else:
                    # Add the student to the DataFrame
                    df = df._append({"Register Number": register_number, "Student Name": student_name}, ignore_index=True)

                with col2:
        
        
                            st.title("Web Cam")
                            FRAME_WINDOW = st.empty()
                        
                            if True:
                                cap = cv2.VideoCapture(0)
                                while True:
                                    ret, frame = cap.read()
                                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                    FRAME_WINDOW.image(frame)
                                    if press:
                                        cv2.imwrite(os.path.join(r"C:\Users\ADMIN\OneDrive\Desktop\Face-Recognition-Attendance-System-main\pages\student_images" , register_number+".jpg"), cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                                        break
                                          
                                        
                            cap.release()
                            

                    
                st.success(f"Student {student_name} with Register Number {register_number} added to the register.")

                    # Save the DataFrame to a CSV file
                df.to_csv("attendance_register.csv", index=False)
                break  



        # Display the current attendance register
        st.subheader("Current Attendance Register")

        colb1, colb2 = st.columns([0.5,0.25])
        with colb1:
            if st.button('New Session'):
                df['Status'] = None
                df.to_csv("attendance_register.csv", index=False)
        with colb2:
            if st.button('New Class'):
                df = pd.DataFrame(columns=["Register Number", "Student Name", "Status"])
                df.to_csv("attendance_register.csv", index=False)
            

        st.dataframe(df)



    







if __name__ == "__main__":
    main()