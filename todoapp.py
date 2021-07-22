import telebot
from telebot import types
from datetime import datetime
from datetime import date
from datetime import time
import sql_master as s_m

bot = telebot.TeleBot("Your TOKEN")

class DatesGoals:
	dates = (' ',)
	goals = (' ',)
	
dates_goals = DatesGoals()

@bot.message_handler(commands=['check'])
def check_goals(message):
	keyboard = types.InlineKeyboardMarkup() 
	key_all_goals = types.InlineKeyboardButton(text='Все цели', callback_data='all_goals')
	keyboard.add(key_all_goals)
	key_today_goals = types.InlineKeyboardButton(text='Цели на сегодня', callback_data='today_goals')
	keyboard.add(key_today_goals)
	bot.send_message(message.from_user.id, text='Что именно нужно посмотреть?', reply_markup=keyboard)
	
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	day = str(date.today())
	s_m.delete_old_goals(day)
	if call.data == 'all_goals':
		user_id = call.from_user.id
		s_m.show_all(call.message.chat.id, user_id)
	if call.data == 'today_goals':
		user_id = call.from_user.id
		s_m.show_today(call.message.chat.id, user_id, day)

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.from_user.id, 'Привет, {0.first_name}!\nЯ бот помогающий составить список дел.\nДля того, чтобы узнать как пользоваться ботом напиши /help '.format(message.from_user, bot.get_me()))

@bot.message_handler(commands=['help'])
def welcome(message):
	bot.send_message(message.from_user.id, 'Сначала напиши дату в формате: "день.месяц.год", а после добавь цель.\nДля проверки целей напиши /check')

@bot.message_handler(content_types = ['text'])
def get_date(message):
	try:
		dates_goals.dates = str(datetime.strptime(message.text, '%d.%m.%Y'))[0:10]
		bot.send_message(message.from_user.id, 'А теперь введите заметку')
		bot.register_next_step_handler(message, get_goal)
	except:
		bot.send_message(message.from_user.id, 'Введите дату в формате "день.месяц.год"')

def get_goal(message):
	dates_goals.goals = message.text
	user_id = message.from_user.id
	s_m.add_goal(user_id, dates_goals.dates, dates_goals.goals)
	bot.send_message(message.from_user.id, 'Добавлено')

bot.polling(none_stop=True)

