import streamlit as st
from src.database.db import create_subject

@st.dialog("Create new subject")
def create_subject_dialog(teacher_id):
    st.write("Enter details of new subject")
    
    sub_id=st.text_input("Subject code",placeholder="CS021")
    sub_name=st.text_input("Subject name",placeholder="Physics")
    sub_section=st.text_input("Section",placeholder="C14")
    
    if st.button("Create subject now",type="primary",width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subject created succesfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error : {str(e)}")
    
        else:
            st.error("Please fill all the fields !")