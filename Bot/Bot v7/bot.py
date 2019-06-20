import config
import telebot
import dbworker
from telebot import types, apihelper

bot = telebot.TeleBot(config.token)
CHANAL_NAME = '-1001256652745'

global data

@bot.message_handler(commands=["help"])
def start_bot(message):
	bot.send_message(message.chat.id, 'Общие комманды: /start ' + ' /help')
	bot.send_message(message.chat.id, 'Клиентские комманды: /order ' + ' /stopsendtosupport')
	bot.send_message(message.chat.id, 'Саппортские комманды: /sendtoclient ' + ' /stopsendtoclient')

@bot.channel_post_handler(commands=["help"])
def start_bot(message):
	bot.send_message(message.chat.id, 'Общие комманды: /start ' + ' /help')
	bot.send_message(message.chat.id, 'Клиентские комманды: /order ' + ' /stopsendtosupport')
	bot.send_message(message.chat.id, 'Саппортские комманды: /sendtoclient ' + ' /stopsendtoclient')

# @bot.message_handler(content_types=['channel_post'])
# def handle_docs_photo(channel_post):
# 	print(channel_post)

@bot.message_handler(commands=["start"])
def start_bot(message):

	bot.send_message(message.chat.id, 'Лучший в мире бот!')

@bot.channel_post_handler(commands=["start"])
def start_bot(message):
	
	bot.send_message(message.chat.id, 'Лучшая в мире работа! /help')

@bot.message_handler(commands=["order"])
def start_bot(message):

	keyboard = types.InlineKeyboardMarkup()
	callback_button = types.InlineKeyboardButton(text="Yes", callback_data="order_yes")
	keyboard.add(callback_button)
	bot.send_message(message.chat.id, 'Оформить заявку?',  reply_markup=keyboard)

# @bot.inline_handler(lambda query: len(query.query) > 0)
# def query_text(query):
#     kb = types.InlineKeyboardMarkup()
#     # Добавляем колбэк-кнопку с содержимым "test"
#     kb.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="order_yes"))
#     results = []
#     single_msg = types.InlineQueryResultArticle(
#         id="1", title="Press me",
#         input_message_content=types.InputTextMessageContent(message_text="Я – сообщение из инлайн-режима"),
#         reply_markup=kb
#     )
#     results.append(single_msg)
#     bot.answer_inline_query(query.id, results)

# @bot.message_handler(commands=["send"])
# def start_bot(message):
# 	bot.send_message(CHANAL_NAME, 'Test - Test')

# @bot.channel_post_handler(commands=["sendtosupport"])
# def change_stage(message):

# 	keyboard = types.InlineKeyboardMarkup()

# 	callback_button = types.InlineKeyboardButton(text="Начать пересылку", callback_data="send_to_support")
# 	keyboard.add(callback_button)
# 	bot.send_message(message.chat.id, "Нажми кнопку!", reply_markup=keyboard)

@bot.message_handler(commands=["stopsendtosupport"])
def change_stage(message):
	bot.send_message(message.chat.id, "Автоматическая пересылка остановлена!")
	dbworker.set_state(message.chat.id, config.States.F_CLIENT.value)

@bot.message_handler(commands=["sendtoclient"])
def change_stage(message):

	keyboard = types.InlineKeyboardMarkup()

	callback_button = types.InlineKeyboardButton(text="Начать пересылку", callback_data="send_to_client")
	keyboard.add(callback_button)
	bot.send_message(message.chat.id, "Введите кому писать", reply_markup=keyboard)

@bot.message_handler(commands=["stopsendtoclient"])
def change_stage(message):
	print(dbworker.get_current_state(message.chat.id))

	bot.send_message(message.chat.id, "Автоматическая пересылка остановлена!")
	dbworker.set_state(message.chat.id, config.States.F_SUPPORT.value)
	

@bot.channel_post_handler(commands=["start"])
def channel_start(message):
	bot.send_message(message.chat.id, 'Я обработал твою комманду start')



@bot.channel_post_handler(content_types=["text"])
def any_msg_channel(message):
	if dbworker.get_current_state(message.chat.id) == config.States.F_CLIENT_SUPPORT.value:
			bot.send_message(88168468, message.text + '\nСообщение перехвачено от клиента')
	else:
		print('Non state message')


@bot.message_handler(content_types=["text"])
def all_msg(message):
	try:

		if dbworker.get_current_state(message.chat.id) == config.States.F_SUPPORT_CLIENT.value:
			bot.send_message(CHANAL_NAME, message.text + '\nСообщение перехвачено от support')
		else:
			# bot.send_message(message.chat.id, 'Test - Test')
			print('Non state message')

	except:
		print('Error')

	pass	

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

	if call.message:
		if 'send_to_client' in call.data:

			dbworker.set_state(call.message.chat.id, config.States.F_SUPPORT_CLIENT.value)
		if 'order_yes' in call.data:
			print(call.message)
			dbworker.set_state(call.message.chat.id, config.States.F_CLIENT_SUPPORT.value)
	elif call.inline_message_id:
		if call.data == "order_yes":
			print(call.message)
			dbworker.set_state(call.message.chat.id, config.States.F_CLIENT_SUPPORT.value)



if __name__ == "__main__":
	bot.polling(none_stop=True)