import requests
import misc											#подключаем файл с токеном
import json
import order
from time import sleep

token = misc.token									#принимаем значение токен для обращения к Telegram API

URL = 'https://api.telegram.org/bot' + token + '/'	#формируем тело ссылки

global last_update_id								#ID последнего сообщения
last_update_id = 0

global pull										#для работы с несколькими пользователями
pull = [0,0,0]									#пользователь|№заявки|стадия

global order										#храниться завка до сохранения
order = ''

global tiket										#номер заявки
tiket = 0

global stage										#номер стадии для создания обращения
stage = 0

global command										#пул комманд
command = ['/start', '/order', '/check', '/help', '/contact']

def get_updates():									#получаем информацию об обновлениях

	url = URL + 'getupdates'
	# offset = 100
	# param = {'offset': offset + 1, 'limit': 0, 'timeout': 10}
	resp = requests.get(url)
	return resp.json()

def get_message():

	data = get_updates()
	
	last_object = data['result'][-1]
	current_update_id = last_object['update_id']

	global last_update_id

	if last_update_id != current_update_id:

		last_update_id = current_update_id

		chat_id = last_object['message']['chat']['id']
		message_text = last_object['message']['text']
		message_id = last_object['message']['message_id']

		message = {'chat_id': chat_id,
					'text': message_text,
					'message_id' : message_id}

		return message

	return None		
	
def send_messege(chat_id, text='Wait a second, please...'):

	url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)

	requests.get(url)

# def get_order(chat_id, text = 'Wait massage...', stage = 0, l_tiket = 0):

# 	global order

# 	if stage == 1:

# 		send_messege(chat_id, 'Выбирите тип Вашей компании:\n\nПартнер - /Partner\nЗаказчик - /Client\nРегиональный дистрибьютор 1С - /Reg_dist\nДругое - /Other')
# 		stage = 2
# 		order = 'Тип компании:\n'

# 		return stage

# 	if stage == 2:

# 		if text == '/Partner':

# 			send_messege(chat_id, 'Укажите Ваш ID партнера')
# 			order = order + 'Партнер' + ' ID '		#В order происходит запись параметра "Тип компании". В данном случае это определенно "Партнер".
# 			stage = 3						#Осуществляем переход к записи ID партнера

# 			return stage

# 		else:

# 			send_messege(chat_id, 'Укажите ИНН Вашей компании')
# 			if text == '/Client':						#В order происходит запись параметра "Тип компании".
# 				order = order + 'Книент'				#В order происходит запись параметра "Тип компании".
# 			if text == '/Reg_dist':
# 				order = order + 'Региональный дистрибьютор 1С'
# 			if text == '/Other':						#В order происходит запись параметра "Тип компании".
# 				order = order + 'Другое'
# 			order = order + '\nИНН ' 					#В order происходит запись параметра "Тип компании".
# 			stage = 3									#Осуществляем переход к записи ИНН компании

# 			return stage

# 	if stage == 3:

# 		if text.isdigit() == True:

# 			order = order + text + '\n'			#Происходит запись ID партнера или ИНН компании
# 			send_messege(chat_id, 'Введите контактные Ваши данные в строгом порядке:\nКомпания\nФамилия\nИмя\nКонтактный телефон\nE-mail\n\nВводите каждое значения в новой строке, по-умолчаюнию это делается нажатием "Shift + Enther" или "Ctrl + Enther".')
# 			stage = 5 

# 		else:
# 			send_messege(chat_id, 'Неверный формат!\nИспользуйте только цифры.')	

# 		return stage

# 	if stage == 5:

# 		order = order + '\nКонтактная информация:\n' + text + '\n'			#Происходит запись контактной информации компании в формате Компания\nФамилия\nИмя\nКонтактный телефон\nE-mail
# 		send_messege(chat_id, 'Изложите Ваш запрос')
# 		print(text)
# 		stage = 6

# 		return stage

# 	if stage == 6:

# 		order = order + '\nЗапрос:\n' + text + '\n'			#Происходит запись запроса
# 		send_messege(chat_id, 'Ваша заявка:\n\n' + order + '\n\nВсе данные корректны? (/Yes | /No)')
# 		stage = 7

# 		return stage

# 	if stage == 7:

# 		if text == '/Yes':

# 			send_messege(chat_id, 'Ваша заявка принята к рассмотрению, в ближайшее время с вами свяжется ответсвенный сотрудник. Номер заявки №' + str(l_tiket))
# 			send_messege(88168468, 'Поступила новая заявка!\n' + order + '\n\n Заявка от \n' + str(chat_id) + '\nЗаявка №\n' + str(l_tiket))

# 			temp = ' От ' + str(chat_id) + ' заявка №' + str(l_tiket) + '.txt'
# 			order_file = open(temp , 'a')
# 			order_file.write('\n' + order  + '\nСтатус: Ожидает обработки.')
# 			order_file.close()

# 			tiket_file = open('last_tiket.txt', 'w')
# 			tiket_file.write(str(tiket))
# 			tiket_file.close()
# 			stage = 0

# 			return stage

# 		if text == '/No':

# 			send_messege(chat_id, 'Восспользуйтесь коммандой /order для повторного составления заявки')
# 			stage = 0

# 			return stage

# 	return stage

def main():

	global stage
	global tiket

	file = open('last_tiket.txt', 'r')
	tiket = int(file.read())
	file.close()

	while True:	

		answer = get_message()

		if answer != None:

			chat_id = answer['chat_id']
			text = answer['text']
			message_id = answer['message_id']

			time_stop = 0

			try:

				if text in command or stage !=0 :

					if text == '/start':

						send_messege(chat_id, 'Добрый день!\nВы обратились к автоматизированной системе приема и обработки заявок отдела Цифровой дистрибьюции компании 1С:Северо-Запад.')
						send_messege(chat_id, 'Для составления заявки используйте комманду /order и сделуйте инструкциям или комманду /help для получения данных о всех доступных коммандах!')
						send_messege(chat_id, '\n\nПРЕДУПРЕЖДЕНИЕ!\n\nПри продолжении работы с ботом, вы соглашаетесь на обработку Ваших персональных данных.\nОзнакомиться с договором - link')
						
						stage = 0
						file = open('chat_ID.txt', 'r+')
						text = file.read()

						if str(chat_id) in text:

							continue

						else:

							file.write('\n' + str(chat_id))

						file.close()
						continue

					if text == '/help':

						send_messege(chat_id, 'Комманда:\n/help - получения данных о всех доступных коммандах\n/contact - данные для обратной связи\n/start - для начала работы с ботом\n/order - для составления заявки\n/check - для проверки существующей заявки')
						stage = 0
						continue

					if text == '/contact':

						send_messege(chat_id, 'Обратная связь.\nСайт: http://1cpd.businesscatalyst.com/\ne-mail: pr-dist@1cnw.ru\nтел.: 8 (812) 385-15-99')
						stage = 0
						continue

					if text == '/order':

						stage = 1
						tiket = tiket + 1

						while True:

							if stage != 8:

								messege = 'Ошибка'

								messege = order.get_order(chat_id, text, stage, tiket)

								send_messege(chat_id, messege)

								stage = stage + 1


						# pull = [chat_id, tiket, stage]

						# stage = get_order(chat_id, text, stage, tiket)

						# time_stop = message_id

						continue

					if text == '/check':

						send_messege(chat_id, 'Введите номер Вашей заявки.')
						stage = 16
						continue


					if stage == 16:

							try:

								if '№' in text:

									file = open(' От ' + str(chat_id) + ' заявка ' + str(text) + '.txt', 'r')

								else:

									file = open(' От ' + str(chat_id) + ' заявка №' + str(text) + '.txt', 'r')
								

							except Exception:

								send_messege(chat_id, 'Введены неверные данные или использовался символ "#".\nВведите номер Вашей заявки.')

							else:

								order_check = file.read()
								stage = 0
								file.close()
								r = order_check.find('Статус:')
								print('----' + str(r))
								print(len(order_check))
								send_messege(chat_id, order_check[r:len(order_check)])
								print(order_check[r:len(order_check)])
								file.close()

							continue

					if message_id != time_stop:

						stage = get_order(chat_id, text, stage, tiket)
						time_stop = message_id
						continue

				else:

					send_messege(chat_id, '\n\nПРЕДУПРЕЖДЕНИЕ!\n\nВоспользуйтесь встроенными коммандами:\n/start - для начала работы с ботом\n/order - для составления заявки\n/check - для проверки существующей заявки')


			except:

				send_messege(chat_id, '\n\nПРЕДУПРЕЖДЕНИЕ!\n\nПрограмная ошибка, перезапустите диалог коммандой /start')
				print(Exception)

		else:

			continue

	sleep(2)

if __name__ == "__main__":
	main()