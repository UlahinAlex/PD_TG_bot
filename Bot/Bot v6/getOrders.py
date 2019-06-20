# -*- coding: utf-8 -*-

import config # хранит различные константы
import telebot # для работы с API Telegram
import dbworker # осуществляет работу с однофайловой БД
from telebot import types, apihelper # важные элементы 

bot = telebot.TeleBot(config.token) # теперь наш бот это bot, GET запрос типа 
									# https://api.telegram.org/bot<TOKEH>/<ЗАПРОС>
global user_data # глобальный словарь для хранения данных 
# Name Company  - хранит название компании
# Contact Name  - хранит как обращаться к контактному лицу
# Company Size  - хранит условное значение числа работников в компании
# Phone			- хранит числовое значение контактного телефона без +7
# E-mail 		- хранит контактый E-mail адресс
# Ticket 		- хранит зарос от Клиенты
# ChatID 		- хранит номер чата Бота с Клиентом
# SupLine 		- хранит значение направления поддержки
# Choose Edit 	- служебное значение, применяется при редактировании заявки Клиентом
user_data = {'Name Company': '' , 'Contact Name':'', 'Company Size':'', 'Phone':'', 'E-mail':'', 'Ticket':'', 'ChatID':'', 'SupLine':'', 'Choose Edit':'' }

# функции Бота, обратная связь которых приходит от нажатия кнопок
class Button_Function:

	# стадия Бота, в которой он получает и обрабатывает решение Клиента о корректности составленного запроса
	def user_current(message, msg_text):

		Other_Function.delete_message(config.token, message.chat.id, message.message_id) # удаляет лишнии сообщения бота
		keyboard = types.InlineKeyboardMarkup()
		
		# Если ответ утвердительный, то отправляет агентам поддержки составленую заявку
		if msg_text == 'YES':
			
			# формирует заявку в str
			tiket = 'Линия поддержки: ' + user_data.get('SupLine')
			tiket += '\nРазмер компании: ' + user_data.get('Company Size')
			tiket += '\nНазвание компании: ' + user_data.get('Name Company')
			tiket += '\nКонтактное лицо: ' + user_data.get('Contact Name')
			tiket += '\nТелефон: ' + user_data.get('Phone')
			tiket += '\nE-mail: ' + user_data.get('E-mail')
			tiket += '\nВопрос: ' + user_data.get('Ticket')
			tiket += '\n\nChat ID: ' + str(user_data.get('ChatID'))

			print(tiket) # Тут происходит пересылка заявки

			dbworker.set_state(message.chat.id, config.States.S_CLIENT_ON_O.value) # Изменяет стадию работы бота с клиентом
			bot.send_message(message.chat.id, '''Заявка составлена!
			Ожидайте подтверждения от оператора.''')

			# Сообщает Клиенту что составка успешно составлена
			if user_data['Phone'] == '' and user_data['E-mail'] == '':

				if user_data['SupLine'] == "Информационная безопасность":
					dbworker.set_state(message.chat.id, config.States.S_CLIENT_ON_IB.value) # Изменяет стадию работы бота с клиентом
				elif user_data['SupLine'] == "Базы данных":
					dbworker.set_state(message.chat.id, config.States.S_CLIENT_ON_BD.value) # Изменяет стадию работы бота с клиентом
				elif user_data['SupLine'] == "Облачные системы":
					dbworker.set_state(message.chat.id, config.States.S_CLIENT_ON_CL.value) # Изменяет стадию работы бота с клиентом
				if not dbworker.get_current_state(message.chat.id) == config.channel_id:
					callback_button_SPY = types.InlineKeyboardButton(text="Принять", callback_data="SP_CY") #Support CALL Yes
					callback_button_SPN = types.InlineKeyboardButton(text="В общий", callback_data="SP_RE") #Support reject
					keyboard.add(callback_button_SPY, callback_button_SPN)
					bot.send_message(dbworker.get_current_state(message.chat.id), tiket, reply_markup=keyboard)
					return

				pass

			callback_button_SP = types.InlineKeyboardButton(text="Уляхин А.", callback_data="SP_Y") #Support first yes
			keyboard.add(callback_button_SP)
			callback_button_SP = types.InlineKeyboardButton(text="Дарий В.", callback_data="SP_D") #Support first yes
			keyboard.add(callback_button_SP)
			callback_button_SP = types.InlineKeyboardButton(text="Волыхина М.", callback_data="SP_V") #Support first yes
			keyboard.add(callback_button_SP)
			bot.send_message(dbworker.get_current_state(message.chat.id), tiket, reply_markup=keyboard)

			

		# Если ответ отрицательный, то просит Клиента изменить неверную позицию
		elif msg_text == 'NO':
			
			

			callback_button_SPL = types.InlineKeyboardButton(text="Линия поддержки", callback_data="CE_SPL")
			# Кнопка для изменения значения "Линия поддержки"
			callback_button_CS = types.InlineKeyboardButton(text="Размер компании", callback_data="CE_CS")
			# Кнопка для изменения значения "Размер компании"
			callback_button_CmN = types.InlineKeyboardButton(text="Название компании", callback_data="CE_CmN")
			# Кнопка для изменения значения "Название компании"
			callback_button_CoN = types.InlineKeyboardButton(text="Контактное лицо", callback_data="CE_CoN")
			# Кнопка для изменения значения "Контактное лицо"
			callback_button_CL = types.InlineKeyboardButton(text="Тип связи", callback_data="CE_CL")
			# Кнопка для выбора и изменеия типа обратной связи
			callback_button_TK = types.InlineKeyboardButton(text="Вопрос", callback_data="CE_TK")
			# Кнопка для изменения текста заявки
			keyboard.add(callback_button_SPL, callback_button_CS, callback_button_CmN, callback_button_CoN, callback_button_CL, callback_button_TK)
			# Объединяем все кнопки для вывода клавиатуры

			bot.send_message(message.chat.id, "Какие данные необходимо исправить?", reply_markup=keyboard)
			# Выводим вопрос и клавиатуру
			bot.send_message(message.chat.id, "Начать заново /reset")
			# Оставляем возможность начать составление заново

	# стадия Бота, в которой Клиент выбирает способ обратной связи
	# значение msg_text поступает из callback_inline, обрабатывающей инлайн-кнопки
	def user_choose_contact_chanal(message, msg_text):

		Other_Function.delete_message(config.token, message.chat.id, message.message_id) # удаляет лишнии сообщения бота
		
		# Определение необходимого типа контакта
		if msg_text == 'EMAIL':
			
			bot.send_message(message.chat.id, "Укажите контактный E-mail")

			dbworker.set_state(message.chat.id, config.States.S_CONTACT_EMAIL.value) # Изменяет стадию работы бота с клиентом
			

		elif msg_text == 'PHONE':

			keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
			# Создает клавиатуру с одной кнопкой в линии и автоматической настройкой размера кнопок

			button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
			# Кнопка запрашивает телефон Клиента, через который происходит общения в Telegram
			button_no = types.KeyboardButton(text="Использовать другой")
			# Кнопка переводит пользователя к ручному вводу номера телефона

			keyboard.add(button_phone, button_no)

			bot.send_message(message.chat.id, "Использовать текущий номер телефона?", reply_markup=keyboard)
			# Выводим вопрос и клавиатуру

			dbworker.set_state(message.chat.id, config.States.S_CONTACT_PHONE.value) # Изменяет стадию работы бота с клиентом
			

		elif msg_text == 'TG': 
			# TG - обратная связь через Telegram
			# Дополнительных сведений от Клиента не требуется, так что сразу переводим на стадию получения текста заявки

			bot.send_message(message.chat.id, "Опишите вопрос")

			dbworker.set_state(message.chat.id, config.States.S_TICKET.value) # Изменяет стадию работы бота с клиентом
			
	# стадия Бота, в которой обрабатывается выбранная Клиентом линия поддержки и переход к стадии определения размера компании
	# значение msg_text поступает из callback_inline, обрабатывающей инлайн-кнопки
	def user_choose_support_line(message, msg_text):

		Other_Function.delete_message(config.token, message.chat.id, message.message_id) # удаляет лишнии сообщения бота

		user_data['SupLine'] = msg_text
		# вносит занчение выбранной линии поддержки

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
		# Выводим вопрос и клавиатуру
		
		dbworker.set_state(message.chat.id, config.States.S_ENTER_COMPANY_SIZE.value) # Изменяет стадию работы бота с клиентом

	# стадия Бота, в которой обрабатывается выбранный Клиентом размер компании и переход к стадии определения получения названия компании
	# значение msg_text поступает из callback_inline, обрабатывающей инлайн-кнопки
	def user_choose_company_size(message, msg_text):

		Other_Function.delete_message(config.token, message.chat.id, message.message_id) # удаляет лишнии сообщения бота

		user_data['Company Size'] = msg_text
		# Вносит занчение выбранного размера компании

		bot.send_message(message.chat.id, "Укажите название компании")

		dbworker.set_state(message.chat.id, config.States.S_ENTER_COMPANY_NAME.value) # Изменяет стадию работы бота с клиентом

# дополнительные функции, необходимые в процессе работы основных функций составления заявки
class Other_Function:

	# функция выводящая необходимые кнопки, при начале составления заявки
	def start_messege():

		keyboard = types.InlineKeyboardMarkup()

		callback_button_IB = types.InlineKeyboardButton(text="Информационная безопасность", callback_data="SPL_IB")
		# Кнопка для значения линии поддержки по "Информационной безопасности"
		callback_button_BD = types.InlineKeyboardButton(text="Базы данных", callback_data="SPL_BD")
		# Кнопка для значения линии поддержки по "Базам данных"
		callback_button_C = types.InlineKeyboardButton(text="Облачные системы", callback_data="SPL_C")
		# Кнопка для значения линии поддержки по "Облачным системам"
		callback_button_O = types.InlineKeyboardButton(text="Другое", callback_data="SPL_O")
		# Кнопка для значения линии поддержки по другим вопросам

		keyboard.add(callback_button_IB, callback_button_BD, callback_button_C, callback_button_O)

		return keyboard # Возвращает объединенные кнопки

	def user_current_reply(message):

		bot.send_message(message.chat.id, "_____________________________")	
		# Для отделения заявки от пердыдущих сообщений

		# формирует заявку в str
		tiket = 'Линия поддержки: ' + user_data.get('SupLine')
		tiket += '\nРазмер компании: ' + user_data.get('Company Size')
		tiket += '\nНазвание компании: ' + user_data.get('Name Company')
		tiket += '\nКонтактное лицо: ' + user_data.get('Contact Name')

		if not user_data['Phone'] == '':
			# Если пользователь вводил номер телефона, то добавляет его
			
			tiket += '\nТелефон: ' + user_data.get('Phone')

		elif not user_data['E-mail'] == '':
			# Если пользователь вводил адресс электронной почты, то добавляет его

			tiket += '\nE-mail: ' + user_data.get('E-mail')

		else:
			# Если пользователь выбрал в качестве обратной связи Telegram
			tiket += '\nОбрытная связь: Телеграмм'

		tiket += '\nВопрос: ' + user_data.get('Ticket')

		bot.send_message(message.chat.id, tiket)
		# Отправляет Клиенту его заявку для подтверждения

		keyboard = types.InlineKeyboardMarkup()

		callback_button_Y = types.InlineKeyboardButton(text="Да", callback_data="UC_Y")
		# Утверждающая кнопка
		callback_button_N = types.InlineKeyboardButton(text="Нет", callback_data="UC_N")
		# Отрицающая кнопка

		keyboard.add(callback_button_Y, callback_button_N)

		bot.send_message(message.chat.id, "Все верно?", reply_markup=keyboard)

		dbworker.set_state(message.chat.id, config.States.S_CURRENT.value) # Изменяет стадию работы бота с клиентом

	# функция для удаления сообщений
	def delete_message(chat_token, chat_id, message_id):
		return apihelper.delete_message(chat_token, chat_id, message_id)


# Далее идут функции описанные через hedler, перехватыввающий обновление переписки и реагирующий на определенные значения
	
# Срабатывает если в част была внесена комманда /start
@bot.message_handler(commands=["start"]) 
def cmd_start(message):
	# По команде /start будем заново начинаться диалог

	user_data['ChatID'] = message.chat.id
	# Вносит занчение id чата в котором Клиент формирует заявку

	keyboard = Other_Function.start_messege() # Кнопки для клавиатуры получаются из функции start_messege

	bot.send_message(message.chat.id, "Привет! В какой области требуется поддержка?", reply_markup=keyboard)

	dbworker.set_state(message.chat.id, config.States.S_SUPPORT_LINE.value) # Изменяет стадию работы бота с клиентом

# Срабатывает если в част была внесена комманда /reset
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
	# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога

	Other_Function.delete_message(config.token, message.chat.id, message.message_id) # удаляет лишнии сообщения бота

	user_data['ChatID'] = message.chat.id
	# Вносит занчение id чата в котором Клиент формирует заявку

	keyboard = Other_Function.send_message() # Кнопки для клавиатуры получаются из функции start_messege

	bot.send_message(message.chat.id, "Что ж, начнём по-новой. В какой области требуется поддержка?", reply_markup=keyboard)

	dbworker.set_state(message.chat.id, config.States.S_SUPPORT_LINE.value) # Изменяет стадию работы бота с клиентом

# Срабатывает только при наличии в БД необходимой стадии у данного чата
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_COMPANY_NAME.value)
def user_entering_company_name(message):
	# Фукция обработки названия компании и запроса контактного лица

	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1) # удаляет лишнии сообщения бота

	user_data['Name Company'] = message.text
	# Вносит занчение названия компании

	# Если данная функция срабатывает при редактировании элемента, то пеосле переводит на стадию подтверждения корректности заявки
	# Понимание работы в режиме редактирования происходит за счет значения Choose Edit словаря
	if user_data['Choose Edit'] == 'ET_CmN':

		Other_Function.user_current_reply(message) 
		# Переводит на стадию подтверждения корректности заявки с измененным элементом

		user_data['Choose Edit'] = ''
		# Обнуляет служебное значение

		return # Обрывает работу функции

	bot.send_message(message.chat.id, "Укажите контактное лицо")

	dbworker.set_state(message.chat.id, config.States.S_ENTER_CONTACT_NAME.value) # Изменяет стадию работы бота с клиентом

# Срабатывает только при наличии в БД необходимой стадии у данного чата
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CONTACT_NAME.value)
def user_entering_contact_name(message):
	# Функция обработки контактного лица и выбора типа обратной связи

	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1) # удаляет лишнии сообщения бота

	user_data['Contact Name'] = message.text
	# Вносит занчение контактного лица

	# Если данная функция срабатывает при редактировании элемента, то пеосле переводит на стадию подтверждения корректности заявки
	# Понимание работы в режиме редактирования происходит за счет значения Choose Edit словаря
	if user_data['Choose Edit'] == 'ET_CoN':

		Other_Function.user_current_reply(message)
		# Переводит на стадию подтверждения корректности заявки с измененным элементом

		user_data['Choose Edit'] = ''
		# Обнуляет служебное значение

		return

	keyboard = types.InlineKeyboardMarkup()

	callback_button_EM = types.InlineKeyboardButton(text="E-mail", callback_data="CCC_Em")
	# Кнопка обратной связи через электронную почту
	callback_button_PH = types.InlineKeyboardButton(text="Телефон", callback_data="CCC_Ph")
	# Кнопка обратной связи по телефону
	callback_button_TG = types.InlineKeyboardButton(text="Telegram", callback_data="CCC_Tg")
	# Кнопка обратной связи через Telegram

	keyboard.add(callback_button_EM, callback_button_PH, callback_button_TG)

	bot.send_message(message.chat.id, "Как с Вами связаться?", reply_markup=keyboard)

	dbworker.set_state(message.chat.id, config.States.S_CHOOSE_CONTACT_CHANAL.value) # Изменяет стадию работы бота с клиентом

# Срабатывает только при наличии в БД необходимой стадии у данного чата
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CONTACT_EMAIL.value)
def user_entering_contact_email(message):

	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1) # удаляет лишнии сообщения бота

	if '@' in message.text and '.' in message.text:
		# Значение электронной почты подразумевает наличие знаков @ и .

		user_data['E-mail'] = message.text
		# Вносит занчение контактной электронной почты

		bot.send_message(message.chat.id, "Опишите вопрос")

		dbworker.set_state(message.chat.id, config.States.S_TICKET.value) # Изменяет стадию работы бота с клиентом

	else:

		bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте еще раз ввести адресс электронной почты")
		# Посылает сообщение о не соответсвии введенных данных необходимогу типу

		return

	# Если данная функция срабатывает при редактировании элемента, то пеосле переводит на стадию подтверждения корректности заявки
	# Понимание работы в режиме редактирования происходит за счет значения Choose Edit словаря
	if user_data['Choose Edit'] == 'ET_CL':

		Other_Function.user_current_reply(message)
		# Переводит на стадию подтверждения корректности заявки с измененным элементом

		user_data['Choose Edit'] = ''
		# Обнуляет служебное значение

		return

# Срабатывает только если в новом сообщение присутсвует поле contact
@bot.message_handler(content_types=["contact"])
def take_this_nomber(message):
	# Если пользователь нажал согласился предоставить свой телефон

	pn = message.contact.phone_number

	user_data['Phone'] = pn
	# Вносит занчение контактной телефона

	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1) # удаляет лишнии сообщения бота

	# Если данная функция срабатывает при редактировании элемента, то пеосле переводит на стадию подтверждения корректности заявки
	# Понимание работы в режиме редактирования происходит за счет значения Choose Edit словаря
	if user_data['Choose Edit'] == 'ET_CL':

		Other_Function.user_current_reply(message)
		# Переводит на стадию подтверждения корректности заявки с измененным элементом

		user_data['Choose Edit'] = ''
		# Обнуляет служебное значение

		return

	dbworker.set_state(message.chat.id, config.States.S_TICKET.value) # Изменяет стадию работы бота с клиентом

	msg = bot.send_message(message.chat.id, "Опишите вопрос")

	bot.register_next_step_handler(msg, user_entering_tiket)
	# Ожидает появления нового сообщения и переходит на стадию введения текста заявки

# Срабатывает только при наличии в БД необходимой стадии у данного чата	
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CONTACT_PHONE.value)
def user_entering_contact_phone(message):
	# Функция обрабатывает контактный телефон и переводит к получения текста заявки

	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1) # удаляет лишнии сообщения бота

	# Если перешло сюда, после попатки автоматического получения телефона
	if message.text == "Использовать другой":

		bot.send_message(message.chat.id, "Введите номер без '+7'")

		return

	if not message.text.isdigit():
		# Номер телефона должен состоять только из цифр (!)

		bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!\nНомер телефона должен состоять только из цифр.")

		return

	user_data['Phone'] = message.text
	# Вносит занчение контактной телефона

	# Если данная функция срабатывает при редактировании элемента, то пеосле переводит на стадию подтверждения корректности заявки
	# Понимание работы в режиме редактирования происходит за счет значения Choose Edit словаря
	if user_data['Choose Edit'] == 'ET_CL':

		Other_Function.user_current_reply(message)
		# Переводит на стадию подтверждения корректности заявки с измененным элементом

		user_data['Choose Edit'] = ''
		# Обнуляет служебное значение

		return

	bot.send_message(message.chat.id, "Опишите вопрос")

	dbworker.set_state(message.chat.id, config.States.S_TICKET.value) # Изменяет стадию работы бота с клиентом

# Срабатывает только при наличии в БД необходимой стадии у данного чата	
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TICKET.value)
def user_entering_tiket(message):
	# Функция обрабатывет текст заявки и переводит к подтверждению корректности составленной заявки

	Other_Function.delete_message(config.token, message.chat.id, message.message_id - 1) # удаляет лишнии сообщения бота
	
	user_data['Ticket'] = message.text
	# Вносит занчение теста заявки

	# Если значение Choose Edit не пустое, то оно обнуляется
	if not user_data['Choose Edit'] == '':

		user_data['Choose Edit'] = ''

	Other_Function.user_current_reply(message) # Переводит к подтверждению корректности составленной заявки

# Отлавливает новые сообщения, имеющие в себе поле call, 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	# По факту реагирует на inline buttons

	if call.message:
		# Утверждаемся что словили то что надо

		if 'ET_' in user_data['Choose Edit'] and not "CCC_" in call.data:
			# Проверяем редактируется ли сейчас заявка

			Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

			if user_data['Choose Edit'] == "ET_SPL":
				# Обрабатываем редактирование линии поддержки

				if call.data == "SPL_IB":

					msg = "Информационная безопасность"

				elif call.data == "SPL_BD":

					msg = "Базы данных"

				elif call.data == "SPL_C":

					msg = "Облачные системы"

				elif call.data == "SPL_O":

					msg = "Другое"

				user_data['SupLine'] = msg
				# Изменяем значение линии поддержки

				Other_Function.user_current_reply(message)
				# Спрашиваем пользователя все ли теперь верно

				user_data['Choose Edit'] = ''
				# чистим служебное значение

			elif user_data['Choose Edit'] == "ET_CS":

				if call.data == "CS_1":

					msg = "Менее 10"

				elif call.data == "CS_2":

					msg = "От 10 до 100"

				elif call.data == "CS_3":

					msg = "От 100 до 1000"

				elif call.data == "CS_4":

					msg = "Более 1000"

				user_data['Company Size'] = msg
				# Изменяем значение размера компании

				Other_Function.user_current_reply(message)
				# Спрашиваем пользователя все ли теперь верно

				user_data['Choose Edit'] = ''
				# чистим служебное значение

			elif user_data['Choose Edit'] == "ET_CL":
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

			Button_Function.user_choose_support_line(call.message, msg)
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

			Button_Function.user_choose_company_size(call.message, msg)
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

			Button_Function.user_choose_contact_chanal(call.message, msg)
			# Переходим к слудующей стадии

		elif "UC_" in call.data:
			# Обрабатываем выбранное значение согласия Клиента с составленной заявкий

			if call.data == "UC_Y":

				msg = "YES"

			elif call.data == "UC_N":

				msg = "NO"

			Button_Function.user_current(call.message, msg)
			# Переходим к слудующей стадии

		elif "CE_" in call.data:
			# Обрабатываем выбранное значение выбранного элемента для изменения

			Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id + 1) # удаляет лишнии сообщения бота
			Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

			if call.data == "CE_SPL":
				# Действия для изменения линии поддержки

				msg = "ET_SPL"

				keyboard = Other_Function.send_message()

				bot.send_message(call.message.chat.id, "В какой области требуется поддержка?", reply_markup=keyboard)				

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

				bot.send_message(call.message.chat.id, "Укажите размер компании", reply_markup=keyboard)

			elif call.data == "CE_CmN":
				# Действия для изменения названия компании

				msg = "ET_CmN"

				bot.send_message(call.message.chat.id, "Укажите название компании")

				dbworker.set_state(call.message.chat.id, config.States.S_ENTER_COMPANY_NAME.value) # Изменяет стадию работы бота с клиентом

			elif call.data == "CE_CoN":
				# Действия для изменения контактного лица

				msg = "ET_CoN"

				bot.send_message(call.message.chat.id, "Укажите контактное лицо")

				dbworker.set_state(call.message.chat.id, config.States.S_ENTER_CONTACT_NAME.value) # Изменяет стадию работы бота с клиентом

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

				bot.send_message(call.message.chat.id, "Как с Вами связаться?", reply_markup=keyboard)

			elif call.data == "CE_TK":
				# Действия для изменения текста заявки

				msg = "ET_TK"

				bot.send_message(call.message.chat.id, "Опишите вопрос")

				dbworker.set_state(call.message.chat.id, config.States.S_TICKET.value)

			user_data['Choose Edit'] = msg
			# Вносим служебно значение

		elif "SP_" in call.data:

			if call.data == 'SP_Y':

				msg = call.message.text

				Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

				bot.send_message(config.ulahin, msg)

				bot.send_message(config.channel_id, msg + '\n\nЗаявка направлена ' + ' Уляхин А.')

			if call.data == 'SP_D':

				msg = call.message.text

				Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

				bot.send_message(config.dariy, msg)

				bot.send_message(config.channel_id, msg + '\n\nЗаявка направлена ' + 'Дарий В.')

			if call.data == 'SP_V':

				msg = call.message.text

				Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

				bot.send_message(config.volihina, msg)

				bot.send_message(config.channel_id, msg + '\n\nЗаявка направлена ' + 'Волыхина М.')


			if call.data == 'SP_CY':

				msg = call.message.text

				Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

				bot.send_message(call.message.chat.id, msg + '\n________\nПринято!')
				print(call.message.chat.id)
				bot.send_message(config.channel_id, msg + '\nЗаявка принял(а) ' + config.support_name(call.message.chat.id))

			if call.data == 'SP_RE':

				msg = call.message.text

				Other_Function.delete_message(config.token, call.message.chat.id, call.message.message_id)

				bot.send_message(call.message.chat.id, 'Заявка отклонена!')

				keyboard = types.InlineKeyboardMarkup()

				callback_button_SP = types.InlineKeyboardButton(text="Уляхин А.", callback_data="SP_Y") #Support first yes
				keyboard.add(callback_button_SP)
				callback_button_SP = types.InlineKeyboardButton(text="Дарий В.", callback_data="SP_D") #Support first yes
				keyboard.add(callback_button_SP)
				callback_button_SP = types.InlineKeyboardButton(text="Волыхина М.", callback_data="SP_V") #Support first yes
				keyboard.add(callback_button_SP)

				bot.send_message(config.channel_id, msg, reply_markup=keyboard)



if __name__ == "__main__":
    bot.polling(none_stop=True)