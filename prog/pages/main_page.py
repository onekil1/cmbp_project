import streamlit as st

if st.session_state.info_user is False or None:
    st.switch_page("login.py")

main_page = st.Page("pages/main_page.py", title="Авторизация", icon=":material/key:")
plan_page = st.Page("pages/plan_page.py", title="План", icon=":material/key:")
dashboard_page = st.Page("pages/dashboard_page.py", title="Графики", icon=":material/key:")
pg = st.navigation([main_page, plan_page, dashboard_page])

full_name = st.session_state.info_user[2]
st.sidebar.success(f"Вы зашли в систему как {full_name}")