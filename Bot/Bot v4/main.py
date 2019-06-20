import telebot
import botConst

bot = telebot.TeleBot(botConst.token)
global stage


@bot.message_handler(commands=["start"])
def handle_start(message):

	user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
	user_markup.row('Оформить заявку', 'Узнать статус заявки')
	user_markup.row('Контакты', 'Закрыть клавиатуру', 'Список комманд')
	bot.send_message(message.from_user.id, 'Добро пожаловать...', reply_markup=user_markup)

	pass

@bot.message_handler(content_types=["text"])
def handle_test(message):
	print(message.text)

	try:
		if message.text == 'Закрыть клавиатуру':
			hide_kayb(message)

		elif message.text == 'Контакты' or message.text == '\contacts':
			bot.send_message(message.from_user.id, botConst.contacts)

		elif message.text == '\see':
			bot.send_sticker(282726944, 'CAADAgADlgADWQMDAAEPVHFP30qsawI')

		elif message.text == 'Узнать статус заявки':
			bot.send_message(message.from_user.id, 'Введите номер заявки в формате:\n"№-<номер заяки>"')

		elif '№-' in message.text:
			order_status = 'Статус неизвестен'
			bot.send_message(message.from_user.id, 'Стутаус заявки ' + message.text + ':\n~~~~~~~~~~~~~\n\n' + order_status + '\n\n~~~~~~~~~~~~~')

		elif message.text == 'Список комманд' or message.text == '\setting':
			bot.send_message(message.from_user.id, botConst.commands)

		elif message.text == 'Оформить заявку':
			hide_kayb(message)
			stage = 0
			textWait = message.text
			get_order(message)
			pass
				
		elif stage != 5:
			if message.text != textWait:
					print(message.text)
					stage = get_order(message)	
	except:
		print('error  ', stage)


def get_order(message):

	if stage == 0:
		user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
		user_markup.row('Партнер', 'Клиент', 'Другое')
		bot.send_message(message.from_user.id, 'Выбирите тип Вашей компании', reply_markup=user_markup)
		stage = 1
		print('--')
		print(stage)
		return stage

	elif stage == 1:
		bot.send_message(message.from_user.id, 'Введите контактные данные в формате:\n<Название организации\nИНН\nE-mail\nНомер телефона>')
		order = messege.text + '\n'
		stage += 1
		print(stage)
		return stage

	elif stage == 2:
		bot.send_message(message.from_user.id, 'Опишите вашу заявку одним сообщением')
		order = order + messege.text + '\n'
		stage += 1
		print(stage)
		return stage

	elif stage == 3:
		bot.send_message(message.from_user.id, order)
		user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
		user_markup.row('Верно', 'Не верно')
		bot.send_message(message.from_user.id, 'Все верно?', reply_markup=user_markup)
		stage += 1
		print(stage)
		return stage

	elif stage == 4:

		if message.text == 'Верно':
			bot.send_message(message.from_user.id, 'Благодарим за оставленную заявку\nНомер заявки №-' + 0000000)

		elif message.text == 'Не верно':
			bot.send_message(message.from_user.id, 'Пожалуйста, используйте \start для оформления новой заявки')

		stage = 5
		return stage

	return stage


def hide_kayb(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)

bot.polling(none_stop=True)