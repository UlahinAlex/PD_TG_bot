# -*- coding: utf-8 -*-
import config
import telebot
import dbworker
from datetime import datetime
from telebot import types, apihelper


bot = telebot.TeleBot(config.token)
global user_data
use_date = {'Name Company': '' , 'Contact Name':'', 'Company Size':'', 'Phone':'', 'E-mail':'', 'Ticket':'', 'ChatID':'', 'SupLine':'', 'Choose Edit':'' }

# Тут лежит первая не до конца рабочая версия
# def getOrder(message):

	# stage = 1
	# user_data['ChatID'] = message.chat.id

	# while i != 99:

	# 	if   stage == 1: #Начат прием заяки, запрашиваем название организации
	# 		bot.send_message(message.chat.id, "Укажите название оранизации")
	# 		stage += 1
	# 		pass

	# 	elif stage == 2: #Запрашиваем контактное лицо или юридическое лицо, к кому будем обращаться
	# 		bot.send_message(message.chat.id, "Укажите контактное лицо")
	# 		user_data['Name Company'] = message.text
	# 		stage += 1
	# 		pass

	# 	elif stage == 3: #Уточняем как будем связываться
	# 		bot.send_message(message.chat.id, "Как с вами связаться?")
	# 		#Тут будет три кнопки "Телефон"+"Почта"+"Телеграмм"
	# 		user_data['Contact Name'] = message.text
	# 		stage += 1
	# 		pass

	# 	elif stage == 4: #Определяем канал связи

	# 		if message.text == :#кнопка телефона
	# 		bot.send_message(message.chat.id, "Использовать этот телефон?")

	# 			if message.text == :#кнопка "Да"
	# 				#А тут просим телефон
	# 				stage = 10
	# 				pass

	# 			elif message.text == :#кнопка "Нет"
	# 				bot.send_message(message.chat.id, "Введите контактный номер телефона")
	# 				stage = 5
	# 				pass

	# 		elif message.text == :#кнопка почты
	# 			satge = 6
	# 			bot.send_message(message.chat.id, "Введите контактный e-mail")
	# 			pass

	# 		elif message.text == :#кнопка телеграмм
	# 			satge = 7
	# 			pass
	# 			#просто помечаем

	# 	elif stage == 5:
	# 		bot.send_message(message.chat.id, "К какой области относиться вопрос?") # "ИБ", "Cloud", "БД", "Other"
	# 		user_data['Phone'] = message.text
	# 		#берем контактную информацию
	# 		satge = 10
	# 		pass

	# 	elif stage == 6:
	# 		bot.send_message(message.chat.id, "К какой области относиться вопрос?") # "ИБ", "Cloud", "БД", "Other"
	# 		user_data['E-mail'] = message.text
	# 		#берем контактную информацию
	# 		satge = 10
	# 		pass

	# 	elif stage == 7:
	# 		bot.send_message(message.chat.id, "К какой области относиться вопрос?") # "ИБ", "Cloud", "БД", "Other"
	# 		user_data['Phone'] = message.chat.id
	# 		#берем контактную информацию
	# 		satge = 10
	# 		pass

	# 	elif stage == 10:
	# 		bot.send_message(message.chat.id, "Укажите рамер компании") # "<10", "10 - 100", "100 - 1000", "1000<"
	# 		user_data['SupLine'] = message.text
	# 		satge += 1
	# 		pass

	# 	elif stage == 11:
	# 		bot.send_message(message.chat.id, "Напишите вопрос")
	# 		user_data['Company Size'] = message.text
	# 		satge += 1
	# 		pass

	# 	elif stage == 12:
	# 		user_data['Ticket'] = message.text
	# 		bot.send_message(message.chat.id, user_data)
	# 		bot.send_message(message.chat.id, "Все верно?") # "Yes", "No"
	# 		satge += 1

	# 	elif stage == 13:

	# 		if message.text == 'Yes':
	# 			bot.send_message(message.chat.id, "Заявка принета, ожидайте ответа от оператора о начале обработки")

	# 		elif message.text == 'No':
	# 			bot.send_message(message.chat.id, "Ваша проблема! Попробуйте заново!")
				
	# 		i = 99

	# 	pass

	# return 1

# Тут лежит вторая, рабочая, версия
class Button_Function:

	def user_current(message, msg_text):
		Other_Function.delete_message(config.token, message.chat.id, message.message_id)
		
		if msg_text == 'YES':
			
			tiket = 'Линия поддержки: ' + use_date.get('SupLine')
			tiket += '\nРазмер компании: ' + use_date.get('Company Size')
			tiket += '\nНазвание компании: ' + use_date.get('Name Company')
			tiket += '\nКонтактное лицо: ' + use_date.get('Contact Name')
			tiket += '\nТелефон: ' + use_date.get('Phone')
			tiket += '\nE-mail: ' + use_date.get('E-mail')
			tiket += '\nВопрос: ' + use_date.get('Ticket')
			tiket += '\n\nChat ID: ' + str(use_date.get('ChatID'))
			print(tiket)
			bot.send_message(message.chat.id, '''Заявка составлена!
			Ожидайте подтверждения от оператора.''')

		elif msg_text == 'NO':
			
			keyboard = types.InlineKeyboardMarkup()

			callback_button = types.InlineKeyboardButton(text="Линия поддержки", callback_data="CE_SPL")
			keyboard.add(callback_button)
			callback_button = types.InlineKeyboardButton(text="Размер компании", callback_data="CE_CS")
			keyboard.add(callback_button)
			callback_button = types.InlineKeyboardButton(text="Название компании", callback_data="CE_CmN")
			keyboard.add(callback_button)
			callback_button = types.InlineKeyboardButton(text="Контактное лицо", callback_data="CE_CoN")
			keyboard.add(callback_button)
			callback_button = types.InlineKeyboardButton(text="Тип связи", callback_data="CE_CL")
			keyboard.add(callback_button)
			# callback_button = types.InlineKeyboardButton(text="Телефон", callback_data="CE_PH")
			# keyboard.add(callback_button)
			# callback_button = types.InlineKeyboardButton(text="E-mail", callback_data="CE_EM")
			# keyboard.add(callback_button)
			callback_button = types.InlineKeyboardButton(text="Вопрос", callback_data="CE_TK")
			keyboard.add(callback_button)

			bot.send_message(message.chat.id, "Какие данные необходимо исправить?", reply_markup=keyboard)
			bot.send_message(message.chat.id, "Начать заново /reset")

			dbworker.set_state(message.chat.id, config.States.S_SUPPORT_LINE.value)

	def user_choose_contact_chanal(message, msg_text):
		Other_Function.delete_message(config.token, message.chat.id, message.message_id)
		
		if msg_text == 'EMAIL':
				
			dbworker.set_state(message.chat.id, config.States.S_CONTACT_EMAIL.value)
			bot.send_message(message.chat.id, "Укажите контактный E-mail")

		elif msg_text == 'PHONE':

			keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
			button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
			button_no = types.KeyboardButton(text="Использовать другой")
			keyboard.add(button_phone, button_no)
			bot.send_message(message.chat.id, "Использовать текущий номер телефона?", reply_markup=keyboard)
			dbworker.set_state(message.chat.id, config.States.S_CONTACT_PHONE.value)
			

		elif msg_text == 'TG':

			dbworker.set_state(message.chat.id, config.States.S_TICKET.value)
			bot.send_message(message.chat.id, "Опишите вопрос")

	def user_choose_support_line(message, msg_text):
		Other_Function.delete_message(config.token, message.chat.id, message.message_id)

		use_date['SupLine'] = msg_text

		keyboard = types.InlineKeyboardMarkup()
		callback_button = types.InlineKeyboardButton(text="Менее 10", callback_data="CS_1")
		keyboard.add(callback_button)
		callback_button = types.InlineKeyboardButton(text="От 10 до 100", callback_data="CS_2")
		keyboard.add(callback_button)
		callback_button = types.InlineKeyboardButton(text="От 100 до 1000", callback_data="CS_3")
		keyboard.add(callback_button)
		callback_button = types.InlineKeyboardButton(text="Более 1000", callback_data="CS_4")
		keyboard.add(callback_button)

		bot.send_message(message.chat.id, "Укажите размер компании", reply_markup=keyboard)
		
		dbworker.set_state(message.chat.id, config.States.S_ENTER_COMPANY_SIZE.value)
		# bot.send_message(message.chat.id, "Укажите размер компании")	

	def user_choose_company_size(message, msg_text):
		Other_Function.delete_message(config.token, message.chat.id, message.message_id)
		use_date['Company Size'] = msg_text
		bot.send_message(message.chat.id, "Укажите название компании")
		dbworker.set_state(message.chat.id, config.States.S_ENTER_COMPANY_NAME.value)

class Other_Function:

	def start_messege():
		keyboard = types.InlineKeyboardMarkup()
		callback_button = types.InlineKeyboardButton(text="Информационная безопасность", callback_data="SPL_IB")
		keyboard.add(callback_button)
		callback_button = types.InlineKeyboardButton(text="Базы данных", callback_data="SPL_BD")
		keyboard.add(callback_button)
		callback_button = types.InlineKeyboardButton(text="Облачные системы", callback_data="SPL_C")
		keyboard.add(callback_button)
		callback_button = types.InlineKeyboardButton(text="Другое", callback_data="SPL_O")
		keyboard.add(callback_button)
		return keyboard

	def user_current_reply(message):

		bot.send_message(message.chat.id, "===================")	
		tiket = 'Линия поддержки: ' + use_date.get('SupLine')
		tiket += '\nРазмер компании: ' + use_date.get('Company Size')
		tiket += '\nНазвание компании: ' + use_date.get('Name Company')
		tiket += '\nКонтактное лицо: ' + use_date.get('Contact Name')
		if not use_date['Phone'] == '':

			tiket += '\nТелефон: ' + use_date.get('Phone')

		elif not use_date['E-mail'] == '':

			tiket += '\nE-mail: ' + use_date.get('E-mail')

		else:

			tiket += '\nОбрытная связь: Телеграмм'

		tiket += '\nВопрос: ' + use_date.get('Ticket')
		bot.send_message(message.chat.id, tiket)
		keyboard = types.InlineKeyboardMarkup()
		callback_button = types.InlineKeyboardButton(text="Да", callback_data="UC_Y")
		keyboard.add(callback_button)
		callback_button = types.InlineKeyboardButton(text="Нет", callback_data="UC_N")
		keyboard.add(callback_button)
		bot.send_message(message.chat.id, "Все верно?", reply_markup=keyboard)
		# bot.send_message(message.chat.id, "Все верно?")
		dbworker.set_state(message.chat.id, config.States.S_CURRENT.value)	

	def delete_message(chat_token, chat_id, message_id):
		return apihelper.delete_message(chat_token, chat_id, message_id)
	

@bot.message_handler(commands=["start"])
def cmd_start(message):
	use_date['ChatID'] = message.chat.id

	keyboard = Other_Function.start_messege()

	bot.send_message(message.chat.id, "Привет! В какой области требуется поддержка?", reply_markup=keyboard)

	dbworker.set_state(message.chat.id, config.States.S_SUPPORT_LINE.value)

# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):

	Other_Function.delete_message(config.token, message.chat.id, message.message_id)
	use_date['ChatID'] = message.chat.id

	keyboard = Other_Function.send_message()

	bot.send_message(message.chat.id, "Что ж, начнём по-новой. В какой области требуется поддержка?", reply_markup=keyboard)

	dbworker.set_state(message.chat.id, config.States.S_SUPPORT_LINE.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_COMPANY_NAME.value)
def user_entering_company_name(message):
	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1)
	use_date['Name Company'] = message.text
	if use_date['Choose Edit'] == 'ET_CmN':
		Other_Function.user_current_reply(message)
		use_date['Choose Edit'] = ''
		return
	bot.send_message(message.chat.id, "Укажите контактное лицо")
	dbworker.set_state(message.chat.id, config.States.S_ENTER_CONTACT_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CONTACT_NAME.value)
def user_entering_contact_name(message):
	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1)
	use_date['Contact Name'] = message.text
	if use_date['Choose Edit'] == 'ET_CoN':
		Other_Function.user_current_reply(message)
		use_date['Choose Edit'] = ''
		return

	keyboard = types.InlineKeyboardMarkup()

	callback_button = types.InlineKeyboardButton(text="E-mail", callback_data="CCC_Em")
	keyboard.add(callback_button)
	callback_button = types.InlineKeyboardButton(text="Телефон", callback_data="CCC_Ph")
	keyboard.add(callback_button)
	callback_button = types.InlineKeyboardButton(text="Telegram", callback_data="CCC_Tg")
	keyboard.add(callback_button)

	bot.send_message(message.chat.id, "Как с Вами связаться?", reply_markup=keyboard)

	dbworker.set_state(message.chat.id, config.States.S_CHOOSE_CONTACT_CHANAL.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CONTACT_EMAIL.value)
def user_entering_contact_email(message):
	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1)
	if '@' in message.text and '.' in message.text:
		use_date['E-mail'] = message.text
		bot.send_message(message.chat.id, "Опишите вопрос")
		dbworker.set_state(message.chat.id, config.States.S_TICKET.value)
	else:
		bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте еще раз")
		return
	if use_date['Choose Edit'] == 'ET_CL':
		Other_Function.user_current_reply(message)
		use_date['Choose Edit'] = ''
		return

@bot.message_handler(content_types=["contact"])
def take_this_nomber(message):
	pn = message.contact.phone_number
	use_date['Phone'] = pn
	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1)
	if use_date['Choose Edit'] == 'ET_CL':
		Other_Function.user_current_reply(message)
		use_date['Choose Edit'] = ''
		return
	dbworker.set_state(message.chat.id, config.States.S_TICKET.value)
	msg = bot.send_message(message.chat.id, "Опишите вопрос")
	bot.register_next_step_handler(msg, user_entering_tiket)
	
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CONTACT_PHONE.value)
def user_entering_contact_phone(message):
	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1)

	if message.text == "Использовать другой":
		bot.send_message(message.chat.id, "Введите номер без '+7'")
		return

	if not message.text.isdigit():
		# Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
		bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
		return

	use_date['Phone'] = message.text
	if use_date['Choose Edit'] == 'ET_CL':
		Other_Function.user_current_reply(message)
		use_date['Choose Edit'] = ''
		return
	bot.send_message(message.chat.id, "Опишите вопрос")
	dbworker.set_state(message.chat.id, config.States.S_TICKET.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TICKET.value)
def user_entering_tiket(message):

	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1)
	
	use_date['Ticket'] = message.text
	if not use_date['Choose Edit'] == '':
		use_date['Choose Edit'] = ''
	Other_Function.user_current_reply(message)
	# tiket = 'Линия поддержки: ' + use_date.get('SupLine')
	# tiket += '\nРазмер компании: ' + use_date.get('Company Size')
	# tiket += '\nНазвание компании: ' + use_date.get('Name Company')
	# tiket += '\nКонтактное лицо: ' + use_date.get('Contact Name')
	# tiket += '\nТелефон: ' + use_date.get('Phone')
	# tiket += '\nE-mail: ' + use_date.get('E-mail')
	# tiket += '\nВопрос: ' + use_date.get('Ticket')
	# bot.send_message(message.chat.id, tiket)
	# keyboard = types.InlineKeyboardMarkup()
	# callback_button = types.InlineKeyboardButton(text="Да", callback_data="UC_Y")
	# keyboard.add(callback_button)
	# callback_button = types.InlineKeyboardButton(text="Нет", callback_data="UC_N")
	# keyboard.add(callback_button)
	# bot.send_message(message.chat.id, "Все верно?", reply_markup=keyboard)
	# # bot.send_message(message.chat.id, "Все верно?")
	# dbworker.set_state(message.chat.id, config.States.S_CURRENT.value)	

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:

		print(call.data)

		if 'ET_' in use_date['Choose Edit'] and not "CCC_" in call.data:
			print(use_date['Choose Edit'])
			Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

			if use_date['Choose Edit'] == "ET_SPL":

				if call.data == "SPL_IB":
					msg = "Информационная безопасность"
				elif call.data == "SPL_BD":
					msg = "Базы данных"
				elif call.data == "SPL_C":
					msg = "Облачные системы"
				elif call.data == "SPL_O":
					msg = "Другое"
				use_date['SupLine'] = msg
				Other_Function.user_current_reply(message)
				use_date['Choose Edit'] = ''

			elif use_date['Choose Edit'] == "ET_CS":

				if call.data == "CS_1":
					msg = "Менее 10"
				elif call.data == "CS_2":
					msg = "От 10 до 100"
				elif call.data == "CS_3":
					msg = "От 100 до 1000"
				elif call.data == "CS_4":
					msg = "Более 1000"
				use_date['Company Size'] = msg
				Other_Function.user_current_reply(message)
				use_date['Choose Edit'] = ''

			elif use_date['Choose Edit'] == "ET_CL":
				pass

			# elif use_date['Choose Edit'] == "ET_CmN":

			# 	if call.data == "CS_1":
			# 		msg = "Менее 10"
			# 	elif call.data == "CS_2":
			# 		msg = "От 10 до 100"
			# 	elif call.data == "CS_3":
			# 		msg = "От 100 до 1000"
			# 	elif call.data == "CS_4":
			# 		msg = "Более 1000"
			# 	use_date['Company Size'] = msg
			# 	user_current_reply(call.message)
			# 	use_date['Choose Edit'] = ''

		elif "SPL_" in str(call.data):

			if call.data == "SPL_IB":
				msg = "Информационная безопасность"
			elif call.data == "SPL_BD":
				msg = "Базы данных"
			elif call.data == "SPL_C":
				msg = "Облачные системы"
			elif call.data == "SPL_O":
				msg = "Другое"

			Button_Function.user_choose_support_line(call.message, msg)

		elif "CS_" in call.data:

			if call.data == "CS_1":
				msg = "Менее 10"
			elif call.data == "CS_2":
				msg = "От 10 до 100"
			elif call.data == "CS_3":
				msg = "От 100 до 1000"
			elif call.data == "CS_4":
				msg = "Более 1000"

			Button_Function.user_choose_company_size(call.message, msg)

		elif "CCC_" in call.data:

			if call.data == "CCC_Em":
				msg = "EMAIL"
			elif call.data == "CCC_Ph":
				msg = "PHONE"
			elif call.data == "CCC_Tg":
				msg = "TG"
			else:
				pass

			Button_Function.user_choose_contact_chanal(call.message, msg)

		elif "UC_" in call.data:

			if call.data == "UC_Y":
				msg = "YES"
			elif call.data == "UC_N":
				msg = "NO"

			Button_Function.user_current(call.message, msg)

		elif "CE_" in call.data:

			Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id + 1)
			Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

			if call.data == "CE_SPL":

				msg = "ET_SPL"
				keyboard = Other_Function.send_message()
				bot.send_message(call.message.chat.id, "В какой области требуется поддержка?", reply_markup=keyboard)
				# dbworker.set_state(call.message.chat.id, config.States.S_SUPPORT_LINE.value)

			elif call.data == "CE_CS":

				keyboard = types.InlineKeyboardMarkup()
				callback_button = types.InlineKeyboardButton(text="Менее 10", callback_data="CS_1")
				keyboard.add(callback_button)
				callback_button = types.InlineKeyboardButton(text="От 10 до 100", callback_data="CS_2")
				keyboard.add(callback_button)
				callback_button = types.InlineKeyboardButton(text="От 100 до 1000", callback_data="CS_3")
				keyboard.add(callback_button)
				callback_button = types.InlineKeyboardButton(text="Более 1000", callback_data="CS_4")
				keyboard.add(callback_button)
				bot.send_message(call.message.chat.id, "Укажите размер компании", reply_markup=keyboard)

				msg = "ET_CS"
				# dbworker.set_state(call.message.chat.id, config.States.S_ENTER_COMPANY_SIZE.value)

			elif call.data == "CE_CmN":

				msg = "ET_CmN"
				bot.send_message(call.message.chat.id, "Укажите название компании")
				dbworker.set_state(call.message.chat.id, config.States.S_ENTER_COMPANY_NAME.value)

			elif call.data == "CE_CoN":

				msg = "ET_CoN"
				bot.send_message(call.message.chat.id, "Укажите контактное лицо")
				dbworker.set_state(call.message.chat.id, config.States.S_ENTER_CONTACT_NAME.value)

			elif call.data == "CE_CL":

				msg = "ET_CL"
				keyboard = types.InlineKeyboardMarkup()

				callback_button = types.InlineKeyboardButton(text="E-mail", callback_data="CCC_Em")
				keyboard.add(callback_button)
				callback_button = types.InlineKeyboardButton(text="Телефон", callback_data="CCC_Ph")
				keyboard.add(callback_button)
				callback_button = types.InlineKeyboardButton(text="Telegram", callback_data="CCC_Tg")
				keyboard.add(callback_button)

				bot.send_message(call.message.chat.id, "Как с Вами связаться?", reply_markup=keyboard)
				# dbworker.set_state(call.message.chat.id, config.States.S_ENTER_CONTACT_NAME.value)

			# elif call.data == "CE_PH":

			# 	msg = "ET_PH"
			# 	# dbworker.set_state(call.message.chat.id, config.States.S_CHOOSE_CONTACT_CHANAL.value)
			# 	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
			# 	button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
			# 	button_no = types.KeyboardButton(text="Использовать другой")
			# 	keyboard.add(button_phone, button_no)
			# 	bot.send_message(call.message.chat.id, "Использовать текущий номер телефона?", reply_markup=keyboard)
			# 	dbworker.set_state(callmessage.chat.id, config.States.S_CONTACT_PHONE.value)

			# elif call.data == "CE_EM":

			# 	msg = "ET_EM"
			# 	dbworker.set_state(call.message.chat.id, config.States.S_CONTACT_EMAIL.value)
			# 	bot.send_message(call.message.chat.id, "Укажите контактный E-mail")

			elif call.data == "CE_TK":

				msg = "ET_TK"
				bot.send_message(call.message.chat.id, "Опишите вопрос")
				dbworker.set_state(call.message.chat.id, config.States.S_TICKET.value)

			use_date['Choose Edit'] = msg




if __name__ == "__main__":
	bot.polling(none_stop=True)