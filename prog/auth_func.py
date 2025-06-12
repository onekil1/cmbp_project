import sqlite3

def create_table():
    connection = sqlite3.connect(r"C:\Users\onekil1\Coding\git_project\db\log=pass.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS auth (
    id INTEGER PRIMARY KEY,
    work_name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    desc TEXT DEFAULT "Отсутствует"
    )
    ''')
    connection.commit()
    return True, "Таблица создана"

def reg_user(work_name, full_name, login, password):
    connection = sqlite3.connect(r"C:\Users\onekil1\Coding\git_project\db\log=pass.db")
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO auth (work_name, full_name, login, password) VALUES (?,?,?,?)', (work_name, full_name, login, password))
        connection.commit()
        return True, "Регистрация прошла успешно!"
    except sqlite3.IntegrityError:
        connection.rollback()
        return False, "Такой login уже используется"
    finally:
        connection.close()

if __name__ == "__main__":
    print(reg_user("ЦМБП", "Басов Р.С.", "admin", "adminadmin"))