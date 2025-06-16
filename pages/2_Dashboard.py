import streamlit as st
import plotly_express as px
import pandas as pd
import sqlite3

def _check_all_task_in_dashboard():
    db = sqlite3.connect(r"C:\Users\onekil1\Coding\git_project\db\log=pass.db")
    query = """SELECT responsible AS "Ответственный", COUNT(*) AS "Количество проектов" FROM plan
        GROUP BY responsible
        ORDER BY COUNT(*) DESC;
        """
    df = pd.read_sql(query, db)
    db.close()
    fig = px.bar(
        df,
        x='Ответственный',
        y='Количество проектов',
        title='Количество проектов по ответственным',
        labels={'Ответственный': '', 'Количество проектов': 'Количество проектов'},
        color='Количество проектов',
        color_continuous_scale='RdBu',
        text='Количество проектов'
    )
    return df, fig


def show_dashboard():
    st.title("📊 Анализ нагрузки по ответственным (по кол-ву проектов)")
    data, chart = _check_all_task_in_dashboard()
    st.plotly_chart(chart)

def navigation():
    if st.session_state.info_user:
        show_dashboard()
    else:
        st.switch_page("🔑Authorization.py")

navigation()