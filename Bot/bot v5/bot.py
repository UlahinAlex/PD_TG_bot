# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
# import getOrder

bot = telebot.TeleBot(config.token)
global global_date

@bot.message_handler(commands=["start"])
def start_message(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
	bot.send_message(message.chat.id, '''Welcome!
		Коли хочешь заявку оставить, иди на /getOrder''')
	pass


@bot.message_handler(commands=["getOrder"])
def handle_test(message):
	any_msg(message, 'Оформить заявку', 'Да')
	pass


def any_msg(message, text_m, text_cb):
	keyboard = types.InlineKeyboardMarkup()
	callback_button = types.InlineKeyboardButton(text=text_cb, callback_data="test")
	keyboard.add(callback_button)
	callback_button = types.InlineKeyboardButton(text='No', callback_data="Yest")
	keyboard.add(callback_button)
	global_date = 'Test'
	print(global_date)
	bot.send_message(message.chat.id, text_m, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	chat_id = call.message.chat.id
	if call.message:

		if call.data == 'test':
			bot.send_message(chat_id, 'Test')
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
		elif call.date == 'Yest':
			bot.send_message(chat_id, 'Yest')
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Бдыщь")

@bot.message_handler(content_types=["text"])
def all_msg(message):
	print('Hi!')
	try:
		if global_date == "Test":
			bot.send_message(message.chat.id, 'Test - Test')
	except:
		print('Error')
	pass	

if __name__ == '__main__':
	bot.polling(none_stop=True)