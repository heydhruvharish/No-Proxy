from src.database.config import supabase
import bcrypt

#FUNCTIONS FOR TEACHER LOGIN/REGISTER PAGE

#Functions for registering in teacher page
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()
    
    
    
def check_teacher_exists(username):
    #Check for unique username
    response=supabase.table("teachers").select("username").eq("username",username).execute()
    
    return len(response.data)>0    


def create_teacher(username,password,name):
    data={"username":username,"password":hash_pass(password),"name":name}
    
    response=supabase.table("teachers").insert(data).execute()
    
    return response.data


#functions for logging in ,in teachers page

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())

def teacher_login(username,password):
    response=supabase.table("teachers").select("*").eq("username",username).execute()
    
    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher["password"]):
            return teacher
        
    return None

#Subject creation in tage page
def create_subject(subject_code,name,section,teacher_id):
    data={"subject_code":subject_code,"name":name,"section":section,"teacher_id":teacher_id}
    
    response=supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response=supabase.table("subjects").select("*,subject_student(count),attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    
    
    subjects=response.data #Different subjects with its ID,teacher ID,Number of students,name of sub & attendance logs
    
    for sub in subjects:
        #Before
        # {
        # "subject_id": 1,
        # "name": "DBMS",
        # "subject_students": [{"count": 40}]
        # }
        sub["total_students"]=sub.get("subject_student",[{}])[0].get("count",0) if sub.get("subject_student") else 0
        #AFTER
        # {
        # "subject_id": 1,
        # "name": "DBMS",
        # "subject_students": [{"count": 40}],
        # "total_students": 40
        # }
        #This is done to make the data easier to use in Streamlit.
        
        #Get all attendance records for this subject.
        attendance=sub.get("attendance_logs",[])
        
        #Count the number of unique attendance timestamps/sessions
        unique_sessions = len(set(log["timestamp"] for log in attendance)) #Its assumed atleast 1 student attends the class
        sub["total_classes"]=unique_sessions
        
        sub.pop("subject_student",None)
        sub.pop("attendance_logs",None)
        
    return subjects


#Teacher taking attendance
def create_attendance(logs):
    response=supabase.table("attendance_logs").insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response=supabase.table("attendance_logs").select("*,subjects!inner(*)").eq("subjects.teacher_id",teacher_id).execute()
    
    return response.data
    

#FUNCTIONS FOR STUDENT PAGE
def get_all_students():
    response=supabase.table("students").select("*").execute()
    
    return response.data

def create_student(new_name,face_embedding,voice_embedding=None):
    data={"name":new_name,"face_embedding":face_embedding,"voice_embedding":voice_embedding}
    
    response=supabase.table("students").insert(data).execute()
    
    return response.data
    
def enroll_student_to_subject(student_id,subject_id,):
    data={"student_id":student_id,"subject_id":subject_id}
    
    response=supabase.table("subject_student").insert(data).execute() #Inserted data is returned in dictionary inside list
    
    return response.data 

def unenroll_student_to_subject(student_id,subject_id,):
    data={"student_id":student_id,"subject_id":subject_id}
    
    response=supabase.table("subject_student").delete().eq("student_id",student_id).eq("subject_id",subject_id).execute() #Inserted data is returned in dictionary inside list
    
    return response.data 

def get_student_subjects(student_id):
    response=supabase.table("subject_student").select("*,subjects(*)").eq("student_id",student_id).execute()
    
    return response.data

def get_student_attendance(student_id):
    #Pick the attendance of all the subjects the student was present or absent
    response=supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",student_id).execute()
    
    return response.data