'''Импорт'''
import sqlite3


'''Создание класса расписания'''
class schedule():
	'''Переменные'''
	connection = 0
	cursor = ''


	'''Создание таблицы расписания'''
	def __init__(self):
		self.connection = sqlite3.connect('schedule.db', check_same_thread=False)
		self.cursor = self.connection.cursor()


		self.cursor.execute('CREATE TABLE IF NOT EXISTS'+
                       '`day` ('+
	                   '`id` INTEGER PRIMARY KEY AUTOINCREMENT,'+
	                   '`date` DATE NOT NULL,'+
	                   '`lessons_count` int NOT NULL,'+
	                   '`place` varchar NOT NULL,'+
	                   '`lessons` varchar NOT NULL'+
                       ');')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS' +
						'`lesson` (' +
						'`id` INTEGER PRIMARY KEY AUTOINCREMENT,' +
						'`teacher` varchar NOT NULL,' +
						'`theme` varchar NOT NULL,' +
						'`time` varchar NOT NULL,' +
						'`home_work` varchar NOT NULL,' +
						'`replace` varchar NOT NULL' +
						');')


	'''Создание дня'''
	def create_day(self, date, lessons_count, place, lessons):
		print('INSERT INTO day(date,lessons_count,place,lessons)'+
							f' VALUES("{date}",{lessons_count},"{place}","{lessons}")')
		self.cursor.execute('INSERT INTO day(date,lessons_count,place,lessons)'+
							f' VALUES("{date}",{lessons_count},"{place}","{lessons}")')
		self.connection.commit()


	'''Вывод расписания'''
	def select_all_days(self, date1, date2):
		print(f'SELECT * from day WHERE date BETWEEN "{date1}" AND "{date2}"')
		self.cursor.execute(f'SELECT * from day WHERE date BETWEEN "{date1}" AND "{date2}"')
		return self.cursor.fetchall()


	'''Вывод расписаня определенной даты'''
	def select_day_by_date(self, date):
		self.cursor.execute(f'SELECT * from day WHERE date="{date}"')
		return self.cursor.fetchall()


	'''Удаление дня'''
	def delete_by_date(self, date):
		self.cursor.execute(f'DELETE FROM day WHERE date="{date}"')
		self.connection.commit()


	'''Вывод уроков'''
	def select_lessons(self, lessons):
		self.cursor.execute(f'SELECT * from lesson WHERE id in ({lessons})')
		return self.cursor.fetchall()
