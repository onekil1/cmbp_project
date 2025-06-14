import streamlit as st
import sqlite3
import hashlib
import os
import time

def _hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    _key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt,100000)
    return salt + _key

def _verify_password(stored_password, input_password):
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    new_key = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), salt, 100000)
    return new_key == stored_key

def _auth_user(login, password):
    with sqlite3.connect("db/log=pass.db") as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM auth WHERE login = ?', (login,))
        result_search = cursor.fetchone()
        if result_search is None:
            return False, "Ошибка: Такой учетной записи не существует"
        if not _verify_password(result_search[4], password):
            return False, "Ошибка: Неверный пароль"
        return True, result_search

def _reg_user(work_name, full_name, login, password, password_check):
    if password_check != password:
        return False, "Ошибка: Указанные пароли не совпадают"
    if len(password) < 8:
        return False, "Ошибка: Длинна пароля должна быть больше 8"
    hashed_password = _hash_password(password)
    connection = sqlite3.connect(r"db/log=pass.db")
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO auth (work_name, full_name, login, password) VALUES (?,?,?,?)', (work_name, full_name, login, hashed_password))
        connection.commit()
        return True, "Регистрация прошла успешно!"
    except sqlite3.IntegrityError:
        connection.rollback()
        return False, "Ошибка базы данных sqllite3"
    finally:
        connection.close()

def reg_button():
    with st.sidebar.form("win", clear_on_submit=True):
        st.subheader("Форма регистрации")
        work_name = st.text_input("Введите название подразделения", placeholder="ЦМБП")
        full_name = st.text_input("Введите свое ФИО", placeholder="Иванов Иван Иванович")
        login = st.text_input("Введите имя учетной записи", placeholder="cmbp_ivanov")
        password = st.text_input("Введите пароль", type="password")
        password_check = st.text_input("Повторите пароль", type="password")
        submit = st.form_submit_button("Подтвердить регистрацию")
        if submit:
            if all([work_name, full_name, login, password, password_check]):
                auth_inst = _reg_user(work_name, full_name, login, password, password_check)
                if auth_inst is True:
                    st.session_state.active_form = None
                    return True, "Регистрация прошла успешно!"
                else:
                    return auth_inst[1]
            else:
                return False,"Ошибка: Все поля должны быть заполнены"

def log_button():
    with st.sidebar.form("Log_form", clear_on_submit=True):
        st.subheader("Форма входа в систему")
        login = st.text_input("Введите имя учетной записи")
        password = st.text_input("Введите пароль", type="password")
        submit = st.form_submit_button("Войти в систему")
    if submit:
        if not all([login, password]):
            return False, "Ошибка входа: Введите логин и пароль"
        else:
            st.session_state.info_user = _auth_user(login, password)
        if st.session_state.info_user[0] is True:
            return True, " "
        else:
            st.session_state.info_user = None
            return False, "Ошибка входа в систему"

def reg_log_interface():
    col1, col2 = st.sidebar.columns(2)
    reg_clicked = col1.button("Регистрация", key="unique_btn_register")
    if reg_clicked:
        st.session_state.active_form = 'register'
        st.rerun()
    if st.session_state.active_form == 'register':
        reg_result = reg_button()
        if reg_result is True:
            st.sidebar.success(reg_result[1])
        elif reg_result is not None:
            st.sidebar.error(reg_result)

    log_clicked = col2.button("Вход в систему", key="unique_btn_login")
    if log_clicked:
        st.session_state.active_form = "login"
        st.rerun()
    if st.session_state.active_form == "login":
        log_result = log_button()
        if log_result is True:
            st.sidebar.success(log_result[1])
            return True
        elif log_result is not None:
            st.sidebar.error(log_result)
            return False

def navigation():
    reg_log_interface()
    if st.session_state.info_user:
        st.switch_page("pages/ℹ️Information.py")
    else:
        return False

if __name__ == "__main__":
    for key in ["info_user","active_form"]:
        if key not in st.session_state:
            st.session_state[key] = None

    st.set_page_config(page_title="Авторизация", layout="wide")
    navigation()