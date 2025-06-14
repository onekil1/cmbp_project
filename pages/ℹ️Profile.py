import streamlit as st
import sqlite3
import pandas as pd

def _add_task(project, in_plan, control, start, end, user):
    db = sqlite3.connect(r"C:\Users\onekil1\Coding\git_project\db\log=pass.db")
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO plan (project, in_plan, control, start, end, responsible) VALUES (?,?,?,?,?,?)',
                       (project, in_plan, control, start, end, user[2]))
        db.commit()
        return True, "Задача была добавлена в план!"
    except sqlite3.IntegrityError:
        db.rollback()
        return False, "Ошибка базы данных sqllite3"
    finally:
        db.close()

def add_task_button():
    with st.form("add_task_form", clear_on_submit=True):
        project_name = st.text_input("Введите наименование проекта", placeholder="Организация сетевой школы")
        in_plan_info = st.text_input("Введите основание выполнения проекта", placeholder="п.12 ПРПП 2025-2026")
        control_task = st.text_input("Введите контролера", placeholder="ЦЗ-1")
        start_date = st.text_input("Введите дату начала выполнения проекта", placeholder="13.01.2025")
        end_date = st.text_input("Введите дату выполнения проекта", placeholder="31.09.2025")
        submit = st.form_submit_button("Я подтверждаю актуальность введенной информации")
        if submit:
            if all([project_name, in_plan_info, control_task, start_date, end_date]):
                user_info = st.session_state.info_user[1]
                add_task_result = _add_task(project_name, in_plan_info, control_task, start_date, end_date, user_info)
                if add_task_result:
                    st.session_state.update = True
                    return True, add_task_result, st.rerun()
                else:
                    return False, add_task_result
            else:
                return False, "Все поля должны быть заполнены"

def _check_tasks(full_name):
    db = sqlite3.connect(r"C:\Users\onekil1\Coding\git_project\db\log=pass.db")
    cursor = db.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try:
        query = """SELECT COUNT(*) FROM plan WHERE responsible = ?"""
        cursor.execute(query, (full_name,))
        count = cursor.fetchone()[0]
        return True, count
    except sqlite3.IntegrityError:
        db.rollback()
        return False, "Ошибка базы данных sqllite3"
    finally:
        db.close()

def info_interface():
    user_info = st.session_state.info_user[1]
    name = user_info[2].split(" ", 2)
    split_name = name[1] + " " + name[2]
    st.title(f"{split_name}, добро пожаловать!")
    task_info = _check_tasks(user_info[2])
    with st.sidebar.container():
        st.markdown("""
        <style>
            .user-card {
                background: #1c232e   ;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
            }
            .info-row {
                margin-bottom: 5px;
                font-family: Calibri;
            }
        </style>
        <div class="user-card">
            <div class="info-row"> <strong>Учетная запись:</strong></div>
            <div class="info-row">👤 <strong>ФИО:</strong> %s</div>
            <div class="info-row">🏢 <strong>Подразделение:</strong> %s</div>
            <div class="info-row">📊 <strong>Активные проекты:</strong> %s</div>
            <div class="info-row">✅ <strong>Завершенные проекты:</strong> 0</div>
        </div>
        """ % (user_info[2], user_info[1], task_info[1]),
                    unsafe_allow_html=True)

        st.markdown("""
        <style>
            div.stButton > button:first-child {
                background-color: #1c232e;
                color: white;
                padding: 3px 10px;
                margin: 0px;
            }
            div.stButton > button:first-child:hover {
                background-color: #45a049;
            }
        </style>
        """, unsafe_allow_html=True)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Добавить проект", key="unique_btn_add_prjct"):
            st.session_state.active_form = "add_project"
            st.rerun()
    if st.session_state.active_form == "add_project":
        with st.container():
            st.header("Добавление нового проекта")
            add_task_result = add_task_button()
            if add_task_result:
                st.session_state.update = True
                st.write(add_task_result)
    with col2:
        if st.button("Внести корректировки"):
            st.session_state.active_form = "correct_project"
            st.rerun()
    if st.session_state.active_form == "correct_project":
        pass


def navigation():
    if st.session_state.info_user:
        info_interface()
    else:
        st.switch_page("🔑Authorization.py")

st.set_page_config(page_title="Профиль пользователя", layout="wide")
if st.session_state.update is True:
    st.session_state.update = False
    st.rerun()
navigation()
# if __name__ == "__main__":
#     print(about_user())