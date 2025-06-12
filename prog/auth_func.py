import sqlite3

def create_table():
    connection = sqlite3.connect(r"C:\Users\onekil1\Coding\git_project\db\log=pass.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS auth (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    desc TEXT DEFAULT "Отсутствует"
    )
    ''')
    connection.commit()
    return True, "Таблица создана"

def reg_user(full_name, login, password, desc):
    connection = sqlite3.connect(r"C:\Users\onekil1\Coding\git_project\db\log=pass.db")
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO log=pass (full_name, login, password, desc) VALUES (?,?,?,?)', (full_name, login, password, desc))
        connection.commit()
        return True, "Регистрация прошла успешно!"
    except sqlite3.IntegrityError:
        connection.rollback()
        return False, "Такой login уже используется"
    finally:
        connection.close()

if __name__ == "__main__":
    print(create_table())