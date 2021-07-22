import sqlite3
import telebot

bot = telebot.TeleBot("Your TOKEN")

def add_goal(id_user, dates, goals):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute("INSERT INTO date_and_goals VALUES (?,?,?)", (id_user, dates, goals))
	conn.commit()
	conn.close()

def delete_old_goals(actual_date):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute("DELETE from date_and_goals WHERE date_time < (?)", (actual_date,))
	conn.commit()
	conn.close()

def show_all(message, id_user):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute("SELECT * FROM date_and_goals WHERE user_id LIKE (?) ORDER BY date_time", (id_user,))
	items = c.fetchall()
	for item in items:
		bot.send_message(message, f'{item[1][8:10] + item[1][4:8] + item[1][0:4] + ": " +item[2]}')
	if len(items) == 0:
		bot.send_message(message, 'Вы еще не успели добавить цели')
	conn.commit()
	conn.close()

def show_today(message, id_user, actual_date):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute("SELECT * FROM date_and_goals WHERE user_id LIKE (?) AND date_time LIKE (?)", (id_user, actual_date))
	items = c.fetchall()
	for item in items:
		bot.send_message(message, f'{item[2]}')
	if len(items) == 0:
		bot.send_message(message, 'На сегодня ничего не запланировано')
	conn.commit()
	conn.close()