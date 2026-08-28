import streamlit as st
from src.UI.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard


def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    
    if "teacher_data" in st.session_state:
        teacher_dashboard() 
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type =="register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    
    st.header(f"""Welcome, {teacher_data["name"]}""")
    
#Login page
from src.database.db import teacher_login

def login_teacher(username,password):
    if not username or not password:
        return False
    teacher=teacher_login(username,password)
    
    if teacher:
        st.session_state.user_role="teacher"
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    
    return False
    
def teacher_screen_login():
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
    st.header("Login using password",text_alignment="center")
    st.space()
    
    teacher_username=st.text_input("Enter username",placeholder="dhruv@gmail.com")
    teacher_pass=st.text_input("Enter password",type="password",placeholder="Enter password")
    st.divider()
    
    btn1,btn2=st.columns(2)
    
    with btn1:
        if st.button("Login",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("Login successful",icon="✅")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or/and password")
        
    with btn2:
        if st.button("Register instead",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            st.session_state.teacher_login_type="register"
            
            
            
#Register page
from src.database.db import check_teacher_exists,create_teacher

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
        return False,"All fields are required"
    
    if teacher_pass!=teacher_pass_confirm:
        return False,"Password does not match"
    
    if check_teacher_exists(teacher_username):
        return False,"Username already taken"
    
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"Profile sucessfully created"
        
    except Exception as e:
        return False,"Unexpected error"
        
def teacher_screen_register():
    style_background_dashboard()
    style_base_layout()
    
    c1 ,c2 =st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()
            
    st.header("Register your teacher profile")
    
    teacher_name=st.text_input("Enter name",placeholder="Dhruv Harish")
    teacher_username=st.text_input("Enter username",placeholder="dhruv@gmail.com")
    teacher_pass=st.text_input("Enter password",type="password",placeholder="Enter password")
    teacher_pass_confirm=st.text_input("Confirm your password",type="password",placeholder="Enter password")
    st.divider()
    
    btn1,btn2=st.columns(2)
    
    with btn1:
        if st.button("Register",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
        
    with btn2:
        if st.button("Login instead",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            st.session_state.teacher_login_type="login"