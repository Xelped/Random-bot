'''Импорты'''
import datetime
from model import schedule
import telebot
import datetime
import time


'''Переменные'''
token = "ВВЕДИТЕ СВОЙ ТОКЕН"
bot = telebot.TeleBot(token)
schedule1 = schedule()

delete_flag = False
keyboard = telebot.types.InlineKeyboardMarkup()
params_new_day_count = 0
new_day = ['', '', '', '']

time_bot = time.localtime()


'''Сообщение о работе бота, выводится в терминал'''
print(f'Бот был включен {time_bot[0]}/{time_bot[1]}/{time_bot[2]} в {time_bot[3]}:{time_bot[4]}:{time_bot[5]}')


'''Список кнопок для редактирования расписания'''
button_list = [
    telebot.types.InlineKeyboardButton(text='Расписание недели', callback_data='show_all_days'),
    telebot.types.InlineKeyboardButton(text='Удалить день', callback_data='delete_by_date'),
    telebot.types.InlineKeyboardButton(text='Добавить день', callback_data='add_new_day'),
]


'''Добавление кнопок'''
for i in button_list:
    keyboard.add(i)


'''Сообщения которые будут отправляться при создании дня'''
params_new_day_desc = [
    'Введите кол-во уроков: ',
    'Введите место: ',
    'Введите уроки: ',
]


'''Стартовое сообщение'''
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='Действие', reply_markup=keyboard)


'''Создание дня'''
def add_new_day(message):
    global params_new_day_count


    '''Проверяет ввели ли вы правильное количество информации'''
    if params_new_day_count == 3:
        new_day[params_new_day_count] = message.text
        schedule1.create_day(new_day[0], new_day[1], new_day[2], new_day[3])
        bot.send_message(message.chat.id, text='Действие', reply_markup=keyboard)


    #Цикл получения информации
    else:
        new_day[params_new_day_count] = message.text
        params_new_day_count += 1
        bot.send_message(message.chat.id, text=params_new_day_desc[params_new_day_count-1])
        bot.register_next_step_handler(message, add_new_day)
        print(params_new_day_count, new_day)


'''Проверка того что мы выбрали из списка'''
@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    '''Показ расписания недели'''
    if call.data == 'show_all_days':


        '''Внутренние переменные'''
        now_date = datetime.datetime.now()
        wd = now_date.weekday()
        date1 = now_date - datetime.timedelta(days=wd)
        date2 = date1 + datetime.timedelta(days=5)
        select_days = schedule1.select_all_days(date1.date(), date2.date())


        '''Проверка количества символов в сообщении, если их больше 0, то функция вызывается'''
        if len(select_days) > 0:
            for day in select_days:
                '''Сбор данных, записывание в переменную, вывод в сообщении'''
                s = 'Дата: '+str(day[1]) + '\n'
                s += 'Кол-во уроков: '+str(day[2])+ '\n'
                s += 'Место проведения: '+str(day[3])+ '\n'
                s += 'Уроки: '+str(day[4])
                bot.send_message(call.message.chat.id, s)


                '''Кнопка для вывода уроков'''
                lessons_button = telebot.types.InlineKeyboardButton(text='Уроки', callback_data=str(day[4]))
                lessons_keyboard = telebot.types.InlineKeyboardMarkup()
                lessons_keyboard.add(lessons_button)
                print(lessons_button)
                print(lessons_keyboard)
                bot.send_message(call.message.chat.id, text='Уроки', reply_markup=lessons_keyboard)


        #Если записей нет
        else:
            bot.send_message(call.message.chat.id, 'Нет записей')


    #Добавление дня
    elif call.data == 'add_new_day':
        bot.send_message(call.message.chat.id, 'Введите дату в формате YYYY-MM-DD:')
        bot.register_next_step_handler(call.message, add_new_day)


    #Удаление дня по дате
    elif call.data == 'delete_by_date':
        global delete_flag
        delete_flag = True
        '''Запрос даты'''
        bot.send_message(call.message.chat.id, 'Введите дату')


    #Нажата кнопка Уроки
    else:
        lessons = schedule1.select_lessons(call.data)
        if len(lessons) > 0:
            for i in lessons:
                s = 'Учитель: '+str(i[1]) + '\n'
                s += 'предмет: '+str(i[2])+ '\n'
                s += 'Дом. работа: '+str(i[3])+ '\n'
                bot.send_message(call.message.chat.id, s)




'''Удаление дня'''
@bot.message_handler(content_types=['text'])
def delete_day(message):
    if delete_flag == True:
        date = message.text
        schedule1.delete_by_date(date)

bot.polling(none_stop=True)
