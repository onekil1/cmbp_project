import streamlit as st

import auth_func

for key in ["reg_bar"]:
    if key not in st.session_state:
        st.session_state[key] = False

def reg_button():
    with st.sidebar.form("reg_form"):
        st.subheader("Форма регистрации")
        work_name = st.text_input("Введите название подразделения", placeholder="ЦМБП")
        full_name = st.text_input("Введите свое ФИО", placeholder="Иванов Иван Иванович")
        login = st.text_input("Введите имя четной записи", placeholder="cmbp_ivanov")
        password = st.text_input ("Введите пароль", type="password")
        password_check = st.text_input ("Повторите пароль", type="password")
        submit = st.form_submit_button("Подтвердить регистрацию")
        if submit:
            if password_check != password:
                st.error("Указанные пароли не совпадают")
                return False
            elif len(password) < 8:
                st.error("Длинна пароля должна быть < 8")
                return False
            elif not all([work_name, full_name, login, password]):
                st.error("Все поля должны быть заполнены")
                return False
            try:
                auth_inst = auth_func.reg_user(work_name, full_name, login, password)
                if auth_inst is True:
                    return True
                else:
                    return False
            except Exception as e:
                st.error(f"Ошибка при регистрации {str(e)}")
                return False

col1, col2 = st.columns(2)
with col1:
        if st.sidebar.button("Регистрация"):
            st.session_state.reg_bar = not st.session_state.reg_bar
            if st.session_state.reg_bar:
                result_reg = reg_button()
                st.write = result_reg