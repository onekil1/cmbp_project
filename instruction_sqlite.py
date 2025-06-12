import sqlite3
# подключение к базе данных(если отсутствует, то будет создана)
connection = sqlite3.connect("mydatabase.db")

# создаем курсор в базе данных для формирования запросов
cursor = connection.cursor()

# создание таблицы Users.
#INTEGER: Целые числа
#TEXT: Текстовые данные
#REAL: Числа с плавающей запятой
#BLOB: Двоичные данные
#NOT NULL: Чтобы не был пустым

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Users (
# id INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# email TEXT NOT NULL,
# age INTEGER
# )
# ''')

# индекс для столбца email
#cursor.execute('CREATE INDEX idx_email ON Users (email)')

# обновление данных
# cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (29, 'newuser'))

# Удаляем пользователя "newuser"
# cursor.execute('DELETE FROM Users WHERE username = ?', ('admin',))

# добавление данных
# cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('clown', '-', 20))

# # Выбираем всех пользователей
# cursor.execute('SELECT * FROM Users')
# users = cursor.fetchall()
# # Выводим результаты
# for user in users:
#   print(user)

# Выбираем имена и возраст пользователей старше 25 лет
# cursor.execute('SELECT username, age FROM Users WHERE age > ?', (25,))
# results = cursor.fetchall()
# for row in results:
#   print(row)




# сохраняем и закрываем соединение
connection.commit()
connection.close()