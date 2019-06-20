import telebot
import config
import getOrders

from telebot import types

bot = telebot.TeleBot(config.token)

# старовое меню
def start_menu(message):

	try:

		user_markup = telebot.types.ReplyKeyboardMarkup(True, True)

		user_markup.row('Оформить заявку', 'Узнать статус заявки')
		user_markup.row('Контакты', 'Закрыть клавиатуру', 'Список комманд')

		bot.send_message(message.from_user.id, 'Добро пожаловать...', reply_markup=user_markup)

	except:

		print(' === ' + ' ERROR IN start_menu' + ' === ' + str(message.chat.id))

	pass

# функция для скрытия клавиатуры
def hide_kayb(message):

	try:

		hide_markup = telebot.types.ReplyKeyboardRemove()

		bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)

	except:

		print(' === ' + ' ERROR IN hide_kayb' + ' === ' + str(message.chat.id))

# функция обработки всех "сообщений"" меню
def all_msg(message):

	try:
		
		if message.text == 'Закрыть клавиатуру':

			hide_kayb(message)

		elif message.text == 'Контакты':

			bot.send_message(message.from_user.id, config.contact_message)

		elif message.text == 'Список комманд':

			bot.send_message(message.from_user.id, config.command_list)

		elif message.text == 'Оформить заявку':

			getOrders.Other_Function.order_start(message)

		elif message.text == 'Узнать статус заявки':

			client_suport = dbworker.get_current_state(message.chat.id)
			
			try:

				support_name = support_name(client_suport)

			except:

				print(' === ' + ' ERROR IN support_name' + ' === ' + str(message.chat.id))

			if client_suport == config.States.S_CLIENT_ON_IB.value:

				bot.send_message(message.from_user.id, 'По вашей заявке работает специалист ' + support_name)

			elif client_suport == config.States.S_CLIENT_ON_CL.value:

				bot.send_message(message.from_user.id, 'По вашей заявке работает специалист ' + support_name)

			elif client_suport == config.States.S_CLIENT_ON_BD.value:

				bot.send_message(message.from_user.id, 'По вашей заявке работает специалист ' + support_name)

			elif client_suport == config.States.S_CLIENT_ON_O.value:

				bot.send_message(message.from_user.id, 'В данный момент Ваша заявка ожидает подтверждения')

			else:

				bot.send_message(message.from_user.id, 'Вами не была составлена заявка!\nДля составления заявки исползуйте /menu')

	except:

		print(' === ' + ' ERROR in all_msg' + ' === ' + str(message.chat.id))

	pass

if __name__ == "__main__":
    bot.polling(none_stop=True)