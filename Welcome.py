import streamlit as st
import pandas as pd
import cv2 
import tempfile
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

def main():

    
    st.set_page_config(
        page_title="Welcome",
        page_icon="👋",
    )

    

    st.sidebar.success("Select the service above.")

    st.markdown('''
                # Welcome to Smart Attendance Management App

    Hi! 

    - To add new students to your class, click **Attendance Management System** in the sidebar
    - To take attendance, click **Take Attendance** in the sidebar
    
    ''')





    

if __name__ == "__main__":
    main()