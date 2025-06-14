import streamlit as st

st.set_page_config(page_title="Информация", layout="wide")
if st.session_state.info_user:
    user_info = st.session_state.info_user[1]
    st.sidebar.success(f"{user_info[2]}, Добро пожаловать!")
else:
    st.sidebar.error(f"Необходимо авторизироваться")