import sqlite3
connection = sqlite3.connect('schedule.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('INSERT INTO lesson(teacher, theme, time, home_work, replace)'+
               'VALUES ("Учитель17", "Обществознание", "", "дом. работа.", "") ')
connection.commit()
