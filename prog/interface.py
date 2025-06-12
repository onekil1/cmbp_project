import streamlit as st

import auth_func

for key in ["reg_bar", "log_bar"]:
    if key not in st.session_state:
        st.session_state[key] = False
def log_button():
    with st.sidebar.form("Log_form", clear_on_submit=True):
        st.subheader("Форма входа в систему")
def reg_button():
    with st.sidebar.form("reg_form", clear_on_submit=True):
        st.subheader("Форма регистрации")
        work_name = st.text_input("Введите название подразделения", placeholder="ЦМБП")
        full_name = st.text_input("Введите свое ФИО", placeholder="Иванов Иван Иванович")
        login = st.text_input("Введите имя учетной записи", placeholder="cmbp_ivanov")
        password = st.text_input("Введите пароль", type="password")
        password_check = st.text_input("Повторите пароль", type="password")
        submit = st.form_submit_button("Подтвердить регистрацию")
    if submit:
        if not all([work_name, full_name, login, password]):
            return st.error("Все поля должны быть заполнены")
        else:
            auth_inst = auth_func.reg_user(work_name, full_name, login, password, password_check)
            if auth_inst:
                return st.success(auth_inst)
            else:
                return st.error(auth_inst)


col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Регистрация"):
        st.session_state.reg_bar = not st.session_state.reg_bar
        st.session_state.log_bar = False
with col2:
    if st.button("Вход в систему"):
        st.session_state.log_bar = not st.session_state.log_bar
        st.session_state.reg_bar = False

if st.session_state.reg_bar:
    reg_button()
if st.session_state.log_bar:
    log_button()