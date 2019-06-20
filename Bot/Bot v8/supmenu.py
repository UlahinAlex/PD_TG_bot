import telebot
import config
import dialog
import main
import dbworker # осуществляет работу с однофайловой БД
from datetime import datetime
from telebot import types

bot = telebot.TeleBot(config.token)

# стартовое меню оператора поддержки
def start_menu(message):
	try:

		keyboard = types.InlineKeyboardMarkup()

		callback_button_login = types.InlineKeyboardButton(text="Login", callback_data="login")

		callback_button_toClint = types.InlineKeyboardButton(text="toCliet", callback_data="toClient")

		keyboard.add(callback_button_login,callback_button_toClint)

		bot.send_message(message.chat.id, "Для начала работы с клиентом авторитизируйтесь!", reply_markup=keyboard)

	except:

		print(' === ' + ' ERROR IN start_menu' + ' === ' + str(message.chat.id))

# выводит доп.меню если пароль правильный
def current_pass(message):
	try:

		keyboard = types.InlineKeyboardMarkup()

		callback_button_toClint = types.InlineKeyboardButton(text="toCliet", callback_data="toClient")

		keyboard.add(callback_button_toClint)

		bot.send_message(message.chat.id, "Пароль верный!", reply_markup=keyboard)

		dbworker.set_state(message.chat.id, config.States.F_SUPPORT_ON.value)


	except:

		print(' === ' + ' ERROR IN current_pass' + ' === ' + str(message.chat.id))

# сопоставляет chatID c операторскими и введеный пароль
def login_current(message):
	try:

		if message.chat.id == config.ulahin:

			if message.text == config.u_pass:

				current_pass(message)

			else:

				bot.send_message(message.chat.id, "Пароль не верный!")

		elif message.chat.id == config.dariy:

			if message.text == config.d_pass:

				current_pass(message)

			else:

				bot.send_message(message.chat.id, "Пароль не верный!")

		elif message.chat.id == config.volihina:

			if message.text == config.v_pass:
				
				current_pass(message)

			else:

				bot.send_message(message.chat.id, "Пароль не верный!")

		else:

			bot.send_message(message.chat.id, "Вы не являетесь сотрудником поддержки!\nДля общения с ботом используйте комманду /start")

	except:

		print(' === ' + ' ERROR IN login_current' + ' === ' + str(message.chat.id))

# начинает работу функции переправки всех сообщений клиенту через бота
def sup_to_client(message):
	try:

		main.set_client(message.text)

		dbworker.set_order_state(message.chat.id, 'client_id', message.text)

		bot.send_message(message.chat.id, "ВНИМАНИЕ!\n\nВсе отправленные сообщения будут пересылаться клиенту. Будьте внимательны!\nДля завершения используйте комманду /stop")
		
		dbworker.set_state(message.chat.id, config.States.F_SUPPORT_CLIENT.value)

	except:

		print(' === ' + ' ERROR IN sup_to_client' + ' === ' + str(message.chat.id))

if __name__ == "__main__":
    bot.polling(none_stop=True)