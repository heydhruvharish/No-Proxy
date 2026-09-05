import streamlit as st
from src.UI.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.database.db import check_teacher_exists,create_teacher,get_teacher_subjects
from src.components.subject_card import subject_card

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
    
   
    c1 ,c2 =st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data["name"]}""")
        if st.button("Logout",type="secondary",key="loginbackbtn",shortcut="control+backspace"):
            st.session_state["is_logged_in"]=False
            del st.session_state.teacher_data
            st.rerun()
            
    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab="take_attendance"
        
    tab1,tab2,tab3=st.columns(3)
    
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab =="take_attendance" else "tertiary"
        if st.button("Take attendace",type=type1,width="stretch",icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab="take_attendance"
            st.rerun()
            
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab =="manage_subjects" else "tertiary"
        if st.button("Manage subjects",type=type2,width="stretch",icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab="manage_subjects"
            st.rerun()
            
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab =="attendance_records" else "tertiary"
        if st.button("Attendance records",type=type3,width="stretch",icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab="attendance_records"
            st.rerun()

    st.divider()
    if st.session_state.current_teacher_tab=="take_attendance":
        teacher_tab_take_attendance()
        
    if st.session_state.current_teacher_tab=="manage_subjects":
        teacher_tab_manage_subjects()
        
    if st.session_state.current_teacher_tab=="attendance_records":
        teacher_tab_attendance_records()
    
def teacher_tab_take_attendance():
    st.header("Take attendace")    
    
def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data["teacher_id"]
    
    col1,col2=st.columns(2)
    with col1:
        st.header("Manage subjects")
    with col2:
        if st.button("Create new subject",width="stretch"):
            create_subject_dialog(teacher_id)
            
            
    #List all subjects
    subjects=get_teacher_subjects(teacher_id)
    
    if subjects:
        for sub in subjects:
            stats=[
                ("🧑‍🎓","Students",sub["total_students"]),
                ("⏲️","Classes",sub["total_classes"])
            ]
        def share_btn():
            st.button(f"Share code : {sub["name"]}",key=f"share_{sub["subject_code"]}",icon=":material/share:")
            # share_subject_dialog(sub["name"],sub["subject_code"])
            # st.space()
            
        subject_card(
            name=sub["name"],
            code=sub["subject_code"],
            section=sub["section"],
            stats=stats,
            footer_callback=share_btn
        )
        
    else:
        st.info("No subject found ,create one")
    
def teacher_tab_attendance_records():
    st.header("records")
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