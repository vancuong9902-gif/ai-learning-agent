import streamlit as st
from api import check_health, upload_document

st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Chọn trang",
    ["Login (Demo)", "Upload Tài liệu", "Health Check"]
)

if page == "Health Check":
    st.title("Backend Health Check")

    if st.button("Check Backend"):
        result = check_health()
        st.json(result)

elif page == "Upload Tài liệu":
    st.title("Upload tài liệu")

    file = st.file_uploader("Chọn file")

    if file and st.button("Upload"):
        result = upload_document(file)
        st.json(result)

elif page == "Login (Demo)":
    st.title("Login giả lập")
    user = st.selectbox("Chọn user", ["Student", "Teacher"])
    st.success(f"Đăng nhập với vai trò: {user}")
