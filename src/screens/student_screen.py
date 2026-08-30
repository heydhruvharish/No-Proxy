import streamlit as st
from src.UI.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from PIL import Image
import numpy as np

def student_screen():
    style_background_dashboard()
    style_base_layout()
    c1 ,c2 =st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()
    
    st.space()
    st.header("Login using faceId",text_alignment="center")
    
    photo_source=st.camera_input("Position your face in the center")

    if photo_source:
        np.array(Image.open(photo_source))

    