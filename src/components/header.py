import base64
import streamlit as st

def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def header_home():
    
    
    img_path = "logo.png"
    img_base64 = get_image_base64(img_path)
    
    st.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center ;margin-top:30px ;margin-bottom:18px;">
            <img src="data:image/png;base64,{img_base64}" style="height: 120px; border-radius:10px" />
            <h1 style="text-align:center ; color:white ">No <br/> Proxy</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
def header_dashboard():
    
    
    img_path = "logo.png"
    img_base64 = get_image_base64(img_path)
    
    st.markdown(
        f"""
        <div style="display:flex;align-items:center; justify-content:center ;gap:10px">
            <img src="data:image/png;base64,{img_base64}" style="height: 95px; border-radius:10px" />
            <h2 style="color:#5865F2 ">No <br/> Proxy</h2>
        </div>
        """,
        unsafe_allow_html=True
    )