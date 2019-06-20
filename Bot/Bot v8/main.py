import postgresql
import subprocess
import telebot
import config
import menu
import supmenu
import dialog
import getOrders
import dbworker # осуществляет работу с однофайловой БД
from telebot import types, apihelper # важные элементы 
from datetime import datetime

# user_data = {'Name Company': '' , 'Contact Name':'', 'Company Size':'', 'Phone':'', 'E-mail':'', 'Ticket':'', 'ChatID':'', 'SupLine':'', 'Choose Edit':'' }

bot = telebot.TeleBot(config.token) # теперь наш бот это bot, GET запрос типа 
									# https://api.telegram.org/bot<TOKEH>/<ЗАПРОС>


# обнуляет статус
@bot.message_handler(commands=["stop"])
def reset_cmd(message):

	dbworker.set_state(message.chat.id, config.States.F_SUPPORT_SET.value)

	bot.send_message(message.chat.id, 'Вы закончили общение с пользователем\n\nДля начала работы используйте комманду /supmenu\n\nИли введите chatID для начала нового диалога.')
		# приветствуем пользователя

# начинает заново формировать зявку
@bot.message_handler(commands=["reset"])
def reset_cmd(message):

	getOrders.Other_Function.cmd_reset(message)

# с этого начинается работа с ботом
@bot.message_handler(commands=["start"])
def start_cmd(message):
	try:

		bot.send_message(message.chat.id, 'Приветствую!\nЯ бот поддержки отдела Проектной дистрибьюции 1С:Северо-запад\n\nДля начала работы используйте комманду /menu')
		# приветствуем пользователя

		dbworker.set_state(message.chat.id, config.States.ZERO.value)
		# даем пользователю пустое значение

		menu.hide_kayb(message)
		# скрываем все клавиатуры

	except:

		print(' === ' + ' ERROR IN start_cmd' + ' === ' + str(message.chat.id))

# вызывает основное меню
@bot.message_handler(commands=["menu"])
def menu_cmd(message):
	try:

		menu.start_menu(message)
		# вызываем основное меню

		dbworker.set_state(message.chat.id, config.States.S_START.value)
		# пользователь получает статус для начала работы

	except:

		print(' === ' + ' ERROR IN menu_cmd' + ' === ' + str(message.chat.id))

# вызыввет меню для оператора поддержки
@bot.message_handler(commands=["supmenu"])
def supmenu_cmd(message):
	try:

		menu.hide_kayb(message)
		# скрываем основное меню, если оно было

		supmenu.start_menu(message)
		# вызывваем inline меню поддержки

		dbworker.set_state(message.chat.id, config.States.F_SUPPORT.value)
		# пользователь получает статус поддержки (пока без прав)

	except:

		print(' === ' + ' ERROR IN supmenu_cmd' + ' === ' + str(message.chat.id))

# вызывает функцию для получения номера телефона от пользователя
@bot.message_handler(content_types=["contact"])
def getorder_tph(message):

	getOrders.take_this_nomber(message)

# обрабатывает кнопки основного меню. когда оно вызвано
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START.value)
def menu_func(message):

	menu.all_msg(message)

# вызывает функцию для определения клиента, которому необходимо написать
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.F_SUPPORT_SET.value)
def supmenu_set(message):

	supmenu.sup_to_client(message)

# проверяет chatID пользователя и запрашивает пароль
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.F_SUPPORT_LOGIN.value)
def supmenu_login(message):

	supmenu.login_current(message)

# вызывает функцию для получения имени компании для заявки
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_COMPANY_NAME.value)
def getorder_cn(message):

	getOrders.user_entering_company_name(message)

# вызывает функцию для получения имени контактного лица для заявки
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CONTACT_NAME.value)
def getorder_cname(message):

	getOrders.user_entering_contact_name(message)

# вызывает функцию для получения контактного телефона для заявки
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CONTACT_PHONE.value)
def getorder_ph(message):

	getOrders.user_entering_contact_phone(message)

# вызывает функцию для получения контактного e-mail для заявки
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CONTACT_EMAIL.value)
def getorder_em(message):

	getOrders.user_entering_contact_email(message)

# вызывает функцию для получения текста заявки
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TICKET.value)
def getorder_tk(message):

	getOrders.user_entering_tiket(message)

# обрабатывает все прочие сообщения
@bot.message_handler(content_types=["text"])
def all_msg(message):

	try:

		stage = dbworker.get_current_state(message.chat.id)
		# определяет на какой стадии пользователь

		print(' : ' + str(message.chat.id) + ' - ' + message.text)
		# потом это будет вести лог

		if stage in config.state_pull and not stage == "0":
			# для игнорирования сообщений при составлении заявки

			print('Client in getOrders')

		elif stage == config.States.S_CLIENT_ON_IB.value or stage == config.States.S_CLIENT_ON_CL.value or stage == config.States.S_CLIENT_ON_BD.value or stage == config.States.F_SUPPORT_CLIENT.value:
			# обрабатывает сообщения для пересылки между пользователем и поддержкой

			cl_sp = dbworker.get_current_state(message.chat.id)
			# получаем статус клиента, зачеем второй раз? А я откуда знаю, лень переписывать

			# в зависимости от стадии клиент он, после составления заявки, он будет сразу писать своему оператору поддержки
			# для понимания кто написал. добавляется приписки '\n\nСообщение перехвачено от клиента '
			if cl_sp == config.States.S_CLIENT_ON_IB.value:

				bot.send_message(str(config.ulahin), message.text + '\n\nСообщение перехвачено от клиента ' + message.chat.id)

			elif cl_sp == config.States.S_CLIENT_ON_CL.value:

				bot.send_message(str(config.volihina), message.text + '\n\nСообщение перехвачено от клиента ' + message.chat.id)

			elif cl_sp == config.States.S_CLIENT_ON_BD.value:

				bot.send_message(str(config.dariy), message.text + '\n\nСообщение перехвачено от клиента ' + message.chat.id)

			elif cl_sp == config.States.F_SUPPORT_CLIENT.value:
				# или если пишет оператор, то добавляет приписку от кого

				bot.send_message(dbworker.get_order_state(message.chat.id, 'client_id'), 'Сообщение отправлено от:'+ config.support_name(message.chat.id) + '\n\n' + message.text)

			else:

				print(' === ' + ' all_msg client-sup ' + ' === ' + str(message.chat.id))
				# на всякий пожарный

		else:

			print('Non state message')
			# сообщение прошло, но пользователь не имеет статуса
			
	except:

		print(' === ' + ' ERROR in all_msg' + ' === ' + str(message.chat.id))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	# По факту реагирует на inline buttons

	if call.message:

		message = call.message
		# чтобы не заебываться и писать как во всем остальном коде

		# для входа оператора поддержки
		if call.data == 'login':

			bot.send_message(message.chat.id, "Введите личный пароль")

			dbworker.set_state(message.chat.id, config.States.F_SUPPORT_LOGIN.value)

		# для выбора кому оператор будет писать
		elif call.data == 'toClient':

			if dbworker.get_current_state(message.chat.id) == config.States.F_SUPPORT_ON.value:
				# проверяем что пишет авторизованный пользователь

				bot.send_message(message.chat.id, "Введите ID клиента")

				dbworker.set_state(message.chat.id, config.States.F_SUPPORT_SET.value)

			else:

				bot.send_message(message.chat.id, "У Вас нет доступа!")

		else:

			if message:
			# Утверждаемся что словили то что надо

				if 'ET_' in dbworker.get_order_state(message.chat.id, 'Choose Edit') and not "CCC_" in call.data:
					# Проверяем редактируется ли сейчас заявка

					getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id)

					if dbworker.get_order_state(message.chat.id, 'Choose Edit') == "ET_SPL":
						# Обрабатываем редактирование линии поддержки

						if call.data == "SPL_IB":

							msg = "Информационная безопасность"

						elif call.data == "SPL_BD":

							msg = "Базы данных"

						elif call.data == "SPL_C":

							msg = "Облачные системы"

						elif call.data == "SPL_O":

							msg = "Другое"

						dbworker.set_order_state(message.chat.id, 'SupLine', msg)
						# Изменяем значение линии поддержки

						getOrders.Other_Function.user_current_reply(message)
						# Спрашиваем пользователя все ли теперь верно

						dbworker.set_order_state(message.chat.id, 'Choose Edit', '')
						# чистим служебное значение

					elif dbworker.get_order_state(message.chat.id, 'Choose Edit') == "ET_CS":

						if call.data == "CS_1":

							msg = "Менее 10"

						elif call.data == "CS_2":

							msg = "От 10 до 100"

						elif call.data == "CS_3":

							msg = "От 100 до 1000"

						elif call.data == "CS_4":

							msg = "Более 1000"

						dbworker.set_order_state(message.chat.id, 'Company Size', msg)
						# Изменяем значение размера компании

						getOrders.Other_Function.user_current_reply(message)
						# Спрашиваем пользователя все ли теперь верно

						dbworker.set_order_state(message.chat.id, 'Choose Edit', '')
						# чистим служебное значение

					elif dbworker.get_order_state(message.chat.id, 'Choose Edit') == "ET_CL":
						# Иключение для изменения линии обратной связи

						pass

				elif "SPL_" in str(call.data):
					# Обрабатываем выбранное значение линии поддержки

					if call.data == "SPL_IB":

						msg = "Информационная безопасность"

					elif call.data == "SPL_BD":

						msg = "Базы данных"

					elif call.data == "SPL_C":

						msg = "Облачные системы"

					elif call.data == "SPL_O":

						msg = "Другое"

					getOrders.Button_Function.user_choose_support_line(message, msg)
					# Переходим к слудующей стадии

				elif "CS_" in call.data:
					# Обрабатываем выбранное значение размера компании

					if call.data == "CS_1":

						msg = "Менее 10"

					elif call.data == "CS_2":

						msg = "От 10 до 100"

					elif call.data == "CS_3":

						msg = "От 100 до 1000"

					elif call.data == "CS_4":

						msg = "Более 1000"

					getOrders.Button_Function.user_choose_company_size(message, msg)
					# Переходим к слудующей стадии

				elif "CCC_" in call.data:
					# Обрабатываем выбранное значение типа обратной связи

					if call.data == "CCC_Em":

						msg = "EMAIL"

					elif call.data == "CCC_Ph":

						msg = "PHONE"

					elif call.data == "CCC_Tg":

						msg = "TG"

					else:

						pass

					getOrders.Button_Function.user_choose_contact_chanal(message, msg)
					# Переходим к слудующей стадии

				elif "UC_" in call.data:
					# Обрабатываем выбранное значение согласия Клиента с составленной заявкий

					if call.data == "UC_Y":

						msg = "YES"

					elif call.data == "UC_N":

						msg = "NO"

					getOrders.Button_Function.user_current(message, msg)
					# Переходим к слудующей стадии

				elif "CE_" in call.data:
					# Обрабатываем выбранное значение выбранного элемента для изменения

					getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id + 1) # удаляет лишнии сообщения бота
					getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id)

					if call.data == "CE_SPL":
						# Действия для изменения линии поддержки

						msg = "ET_SPL"

						keyboard = getOrders.Other_Function.send_message()

						bot.send_message(message.chat.id, "В какой области требуется поддержка?", reply_markup=keyboard)				

					elif call.data == "CE_CS":
						# Действия для изменения размера компании

						msg = "ET_CS"

						keyboard = types.InlineKeyboardMarkup()

						callback_button_1 = types.InlineKeyboardButton(text="Менее 10", callback_data="CS_1")
						# Кнопка для значения размера компании < 10
						callback_button_2 = types.InlineKeyboardButton(text="От 10 до 100", callback_data="CS_2")
						# Кнопка для значения размера компании < 100
						callback_button_3 = types.InlineKeyboardButton(text="От 100 до 1000", callback_data="CS_3")
						# Кнопка для значения размера компании < 1000
						callback_button_4 = types.InlineKeyboardButton(text="Более 1000", callback_data="CS_4")
						# Кнопка для значения размера компании > 1000

						keyboard.add(callback_button_1, callback_button_2, callback_button_3, callback_button_4)

						bot.send_message(message.chat.id, "Укажите размер компании", reply_markup=keyboard)

					elif call.data == "CE_CmN":
						# Действия для изменения названия компании

						msg = "ET_CmN"

						bot.send_message(message.chat.id, "Укажите название компании")

						dbworker.set_state(message.chat.id, config.States.S_ENTER_COMPANY_NAME.value) # Изменяет стадию работы бота с клиентом

					elif call.data == "CE_CoN":
						# Действия для изменения контактного лица

						msg = "ET_CoN"

						bot.send_message(message.chat.id, "Укажите контактное лицо")

						dbworker.set_state(message.chat.id, config.States.S_ENTER_CONTACT_NAME.value) # Изменяет стадию работы бота с клиентом

					elif call.data == "CE_CL":
						# Действия для изменения типа обратной связи

						msg = "ET_CL"

						keyboard = types.InlineKeyboardMarkup()

						callback_button_EM = types.InlineKeyboardButton(text="E-mail", callback_data="CCC_Em")
						# Кнопка обратной связи через электронную почту
						callback_button_PH = types.InlineKeyboardButton(text="Телефон", callback_data="CCC_Ph")
						# Кнопка обратной связи по телефону
						callback_button_TG = types.InlineKeyboardButton(text="Telegram", callback_data="CCC_Tg")
						# Кнопка обратной связи через Telegram

						keyboard.add(callback_button_EM, callback_button_PH, callback_button_TG)

						bot.send_message(message.chat.id, "Как с Вами связаться?", reply_markup=keyboard)

					elif call.data == "CE_TK":
						# Действия для изменения текста заявки

						msg = "ET_TK"

						bot.send_message(message.chat.id, "Опишите вопрос")

						dbworker.set_state(message.chat.id, config.States.S_TICKET.value)

					dbworker.set_order_state(message.chat.id, 'Choose Edit', msg)
						# Вносим служебно значение

				elif "SP_" in call.data:
					# колбеки от кнопок операторов поддержки

					if call.data == 'SP_Y':
						# заявка отправлена оператору по ИБ

						msg = message.text

						getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id)

						bot.send_message(config.ulahin, msg)

						bot.send_message(config.channel_id, msg + '\n\nЗаявка направлена ' + ' Уляхин А.')

					if call.data == 'SP_D':
						# заявка отправлена оператору по Cloud

						msg = message.text

						getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id)

						bot.send_message(config.dariy, msg)

						bot.send_message(config.channel_id, msg + '\n\nЗаявка направлена ' + 'Дарий В.')

					if call.data == 'SP_V':
						# заявка отправлена оператору по БД

						msg = message.text

						getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id)

						bot.send_message(config.volihina, msg)

						bot.send_message(config.channel_id, msg + '\n\nЗаявка направлена ' + 'Волыхина М.')


					if call.data == 'SP_CY':
						# оператор принял заявку

						msg = message.text

						getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id)

						bot.send_message(message.chat.id, msg + '\n________\nПринято!')
						
						bot.send_message(config.channel_id, msg + '\nЗаявка принял(а) ' + config.support_name(message.chat.id))
						# дублируем в общий канал, чтобы все видели и гордились

					if call.data == 'SP_RE':
						# оператор отклонил заявку

						msg = message.text

						getOrders.Other_Function.delete_message(config.token, message.chat.id, message.message_id)

						bot.send_message(message.chat.id, 'Заявка отклонена!')

						keyboard = types.InlineKeyboardMarkup()

						callback_button_SP = types.InlineKeyboardButton(text="Уляхин А.", callback_data="SP_Y") #Support first yes
						keyboard.add(callback_button_SP)
						callback_button_SP = types.InlineKeyboardButton(text="Дарий В.", callback_data="SP_D") #Support first yes
						keyboard.add(callback_button_SP)
						callback_button_SP = types.InlineKeyboardButton(text="Волыхина М.", callback_data="SP_V") #Support first yes
						keyboard.add(callback_button_SP)

						bot.send_message(config.channel_id, msg, reply_markup=keyboard)
						# отклоненные заявки уходят в общий канал
						# к ней прикрепляется кнопка, для каждого оператора поддержки
						# если ее нажать, то будет считаться что оператор принял заявку
						# отказаться он не сможет
			else:
					print(' === ' + ' ERROR IN callback' + ' === ' + str(message.chat.id))

if __name__ == "__main__":
    bot.polling(none_stop=True)