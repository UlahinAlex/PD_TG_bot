def get_order(chat_id, text = 'Wait massage...', stage = 0, l_tiket = 0):

	global order
	messege = ' '

	if stage == 1:

		messege = 'Выбирите тип Вашей компании:\n\nПартнер - /Partner\nЗаказчик - /Client\nРегиональный дистрибьютор 1С - /Reg_dist\nДругое - /Other'
		stage = 2
		order = 'Тип компании:\n'

		return messege

	if stage == 2:

		if text == '/Partner':

			messege = 'Укажите Ваш ID партнера'
			order = order + 'Партнер' + ' ID '		#В order происходит запись параметра "Тип компании". В данном случае это определенно "Партнер".
			stage = 3						#Осуществляем переход к записи ID партнера

			return messege

		else:

			messege = 'Укажите ИНН Вашей компании'
			if text == '/Client':						#В order происходит запись параметра "Тип компании".
				order = order + 'Книент'				#В order происходит запись параметра "Тип компании".
			if text == '/Reg_dist':
				order = order + 'Региональный дистрибьютор 1С'
			if text == '/Other':						#В order происходит запись параметра "Тип компании".
				order = order + 'Другое'
			order = order + '\nИНН ' 					#В order происходит запись параметра "Тип компании".
			stage = 3									#Осуществляем переход к записи ИНН компании

			return messege

	if stage == 3:

		if text.isdigit() == True:

			order = order + text + '\n'			#Происходит запись ID партнера или ИНН компании
			messege = 'Введите контактные Ваши данные в строгом порядке:\nКомпания\nФамилия\nИмя\nКонтактный телефон\nE-mail\n\nВводите каждое значения в новой строке, по-умолчаюнию это делается нажатием "Shift + Enther" или "Ctrl + Enther".'
			stage = 5 

		else:
			messege = 'Неверный формат!\nИспользуйте только цифры.'	

		return messege

	if stage == 5:

		order = order + '\nКонтактная информация:\n' + text + '\n'			#Происходит запись контактной информации компании в формате Компания\nФамилия\nИмя\nКонтактный телефон\nE-mail
		messege =  'Изложите Ваш запрос'
		stage = 6

		return messege

	if stage == 6:

		order = order + '\nЗапрос:\n' + text + '\n'			#Происходит запись запроса
		messege = 'Ваша заявка:\n\n' + order + '\n\nВсе данные корректны? (/Yes | /No)'
		stage = 7

		return messege

	if stage == 7:

		if text == '/Yes':

			messege = 'Ваша заявка принята к рассмотрению, в ближайшее время с вами свяжется ответсвенный сотрудник. Номер заявки №' + str(l_tiket)
			# send_messege(88168468, 'Поступила новая заявка!\n' + order + '\n\n Заявка от \n' + str(chat_id) + '\nЗаявка №\n' + str(l_tiket))

			temp = ' От ' + str(chat_id) + ' заявка №' + str(l_tiket) + '.txt'
			order_file = open(temp , 'a')
			order_file.write('\n' + order  + '\nСтатус: Ожидает обработки.')
			order_file.close()

			tiket_file = open('last_tiket.txt', 'w')
			tiket_file.write(str(tiket))
			tiket_file.close()
			stage = 0

			return messege

		if text == '/No':

			messege = 'Восспользуйтесь коммандой /order для повторного составления заявки'
			stage = 0

			return messege

	return messege


def main():




	# chat_id = 
	# stage = 
	# tic = 0
	# file = open('pull.txt', 'r')
	# order_check = file.read()
	# stage = 0
	# file.close()
	# r = order_check.find('Статус:')
	# print('----' + str(r))
	# print(len(order_check))
	# # send_messege(chat_id, order_check[r:len(file)])
	# print(order_check[r:len(order_check)])
	# file.close()
	pass


if __name__ == "__main__":
	main()