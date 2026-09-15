import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_result import show_attendance_result,attendance_result_dialog



@st.dialog("Voice attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write("Record audio of students saying i am present")
    
    audio_data=None 
    
    audio_data=st.audio_input("Record classroom audio")
    
    if st.button("Analyze audio",type="primary",width="stretch"):
        with st.spinner('Processing Audio data'):
            enrolled_res=supabase.table("subject_student").select("*,students(*)").eq("subject_id",selected_subject_id).execute()
            enrolled_students=enrolled_res.data
                
            if not enrolled_students:
                st.warning("No enrolled students in this course!")
                return 

            #It takes the enrolled_students records and collects only the students whose voice_embedding is available.
            candidates_dict={
                s["students"]["student_id"]:s["students"]["voice_embedding"]    #Example "S101": [0.12, 0.45, 0.78]
                for s in enrolled_students if s["students"].get("voice_embedding")
                   
            }
            
            if not candidates_dict:
                st.error("No enrolled students have voice profiles registered")
                return 

            audio_bytes=audio_data.read()
            
            dectected_scores=process_bulk_audio(audio_bytes,candidates_dict)
            
            results,attendance_to_log=[],[]
                                
            current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            
            for node in enrolled_students:
                student=node["students"]
                score=dectected_scores.get(student["student_id"],0.0)
                is_present=bool(score>0)
                
                results.append({
                    "Name":student["name"],
                    "ID":student["student_id"],
                    "Source":score if is_present else "-",
                    "Status":"✅ Present" if is_present else "❌ Absent"
                    
                })
                
                attendance_to_log.append({
                    "student_id":student["student_id"],
                    "subject_id":selected_subject_id,
                    "timestamp":current_timestamp,
                    "is_present":bool(is_present)
                })
                
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

                
    
    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results,logs=st.session_state.voice_attendance_results
        
        show_attendance_result(df_results,logs)