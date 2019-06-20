import telebot
import botID

bot = telebot.TeleBot(botID.token)
global global_client
global_client = []
global client_stage
client_stage = []
global global_orders
global_orders = [global_client,client_stage]


# bot.send_message(botID.me, 'Добро пожаловать...')
@bot.message_handler(commands=["start"])
def handle_start(message):
	user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
	user_markup.row('Оформить заявку', 'Узнать статус заявки')
	user_markup.row('Контакты', 'Закрыть клавиатуру', 'Список комманд')
	bot.send_message(message.from_user.id, 'Добро пожаловать...', reply_markup=user_markup)
	pass
# @bot.message_handler(commands=["stop"])
# def handle_start(message):
# 	hide_markup = telebot.types.ReplyKeyboardRemove()
# 	bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)

@bot.message_handler(content_types=["text"])
def handle_test(message):
	stage = 0
	try:
		client_index = global_client.index(message.from_user.id)
		stage = client_stage.pop(client_index)
		client_stage.insert(client_index, 0)
	except:
		print('Error!')
	if message.text == 'Закрыть клавиатуру':
		hide_kayb(message)
	elif message.text == 'Контакты':
		bot.send_message(message.from_user.id, botID.contacts)
	elif message.text == 'Узнать статус заявки':
		bot.send_message(message.from_user.id, 'Введите номер заявки в формате:\n"№-<номер заяки>"')
	elif message.text == 'Оформить заявку':
		global_client.append(message.from_user.id)
		client_stage.append(0)
		hide_kayb(message)
		get_order(message)
	elif '№-' in message.text:
		order_status = 'Статус неизвестен'
		bot.send_message(message.from_user.id, 'Стутаус заявки ' + message.text + ':\n~~~~~~~~~~~~~\n\n' + order_status + '\n\n~~~~~~~~~~~~~')
	elif stage > 0:
		get_order(message)

def hide_kayb(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)

def get_order(message):
	client_index = global_client.index(message.from_user.id)
	stage = client_stage.pop(client_index)
	print('=' + str(stage))
	if stage == 0:
		user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
		user_markup.row('Партнер', 'Клиент', 'Другое')
		bot.send_message(message.from_user.id, 'Выбирите тип Вашей компании', reply_markup=user_markup)
		client_stage.insert(client_index, 1)
		print('+' + str(stage))
	elif stage == 1:
		bot.send_message(message.from_user.id, 'Введите контактные данные в формате:\n<Название организации\nИНН\nE-mail\nНомер телефона>')
		client_stage.insert(client_index, 2)
	elif stage == 2:
		bot.send_message(message.from_user.id, 'Опишите вашу заявку одним сообщением')
		client_stage.insert(client_index, 3)

	print(stage)
	pass




bot.polling(none_stop=True)