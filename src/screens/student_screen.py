import streamlit as st
from src.UI.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance,get_face_embeddings,refresh_trained_model
from src.database.db import get_all_students,create_student
import time
from src.pipelines.voice_pipeline import get_voice_embedding

def student_dashboard():
    st.header("DashBoard here")

def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1 ,c2 =st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()
    
    st.space()
    st.header("Login using faceId",text_alignment="center")
    
    show_registration=False
    photo_source=st.camera_input("Position your face in the center")

    if photo_source:
        img=np.array(Image.open(photo_source))
        
        with st.spinner("AI is scanning..."):
            detected,all_ids,num_faces=predict_attendance(img)
            
            if num_faces==0:
                st.warning("Face not found ! ")
            elif num_faces>1:
                st.warning("Multiple faces found")
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s["student_id"]==student_id),None) #If condition satisfies ,return s
                    
                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role="student"
                        st.session_state.student_data=student
                        st.toast(f"Welcome back {student["name"]}")
                        
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized ,register if you dont have an account")
                    show_registration=True
    
    if show_registration:
        with st.container(border=True):
            st.header("Register new profile")
            new_name=st.text_input("Enter your name",placeholder="Eg Dhruv Harish")
            
            st.subheader("Optional : voice enrollment")
            st.info("Enroll your voice for voice only attendance")
            
            audio_data=None
            
            try:
                audio_data=st.audio_input("Record your voice (Eg.I am present ,my name is Dhruv)")
            except Exception:
                st.error("Audio data failed")
                
            
            if st.button("Create account",type="primary"):
                if new_name:
                    with st.spinner("Creating profile.."):
                        img=np.array(Image.open(photo_source))
                        encodings=get_face_embeddings(img)
                        
                        if encodings:
                            face_emb=encodings[0].tolist()
                            voice_emb=None
                            
                            if audio_data:
                                voice_emb=get_voice_embedding(audio_data.read())
                                
                            response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)
                            
                            if response_data:
                                refresh_trained_model()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role="student"
                                st.session_state.student_data=response_data[0]
                                st.toast(f"Profile create ,Hi {student["name"]}!")            
                                time.sleep(1)
                                st.rerun()
                                
                        else:
                            st.error("Couldnt capture your facial features for recognition")
                else:
                    st.warning("Please enter your name")