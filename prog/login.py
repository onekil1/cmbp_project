import streamlit as st
import sqlite3
import hashlib
import os

for key in ["reg_bar", "log_bar", "info_user"]:
    if key not in st.session_state:
        st.session_state[key] = False

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    _key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt,100000)
    return salt + _key

def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return new_key == stored_key

def reg_user(work_name, full_name, login, password, password_check):
    if password_check != password:
        return "Указанные пароли не совпадают"
    if len(password) <= 8:
        return "Длинна пароля должна быть больше 8"
    hashed_password = hash_password(password)
    connection = sqlite3.connect(r"db/log=pass.db")
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO auth (work_name, full_name, login, password) VALUES (?,?,?,?)', (work_name, full_name, login, hashed_password))
        connection.commit()
        return "Регистрация прошла успешно!"
    except sqlite3.IntegrityError:
        connection.rollback()
        return "Учетная запись с таким именем уже существует!"
    finally:
        connection.close()

def auth_user(login, password):
    connection = sqlite3.connect(r"db/log=pass.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM auth WHERE login = ?', (login,))
    result_search = cursor.fetchone()
    if result_search is None:
        return "Учетной записи с таким именем учетной записи не существует"
    stored_password = result_search[4]
    if not verify_password(stored_password, password):
        return "Неверный логин или пароль"
    else:
        return result_search

def log_button():
    with st.sidebar.form("Log_form", clear_on_submit=True):
        st.subheader("Форма входа в систему")
        login = st.text_input("Введите имя учетной записи", placeholder="cmbp_ivanov")
        password = st.text_input("Введите пароль", type="password")
        submit = st.form_submit_button("Войти в систему")
    if submit:
        if not all([login, password]):
            return st.error("Введите свой логин и пароль")
        else:
            log_inst = auth_user(login, password)
        if log_inst:
            st.session_state.info_user = log_inst
            return True
        else:
            st.error("Такого пользователя не существует")
            return False

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
            auth_inst = reg_user(work_name, full_name, login, password, password_check)
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

if st.session_state.info_user is False:
    if st.session_state.reg_bar:
        reg_button()
    if st.session_state.log_bar:
        log_button()

if st.session_state.info_user:
    st.switch_page("main_page.py")