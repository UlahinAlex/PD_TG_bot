# import config # хранит различные константы
# import telebot # для работы с API Telegram
# import main
# import dbworker # осуществляет работу с однофайловой БД
# from telebot import types, apihelper # важные элементы 

# bot = telebot.TeleBot(config.token) # теперь наш бот это bot, GET запрос типа 
# 									# https://api.telegram.org/bot<TOKEH>/<ЗАПРОС>

# def all_msg(message):

# 	try:

# 		cl_sp = dbworker.get_current_state(message.chat.id)


# 		if cl_sp == config.States.S_CLIENT_ON_IB.value:

# 			bot.send_message(str(config.ulahin), message.text + '\n\nСообщение перехвачено от клиента ' + message.chat.id)

# 		elif cl_sp == config.States.S_CLIENT_ON_CL.value:

# 			bot.send_message(str(config.volihina), message.text + '\n\nСообщение перехвачено от клиента ' + message.chat.id)

# 		elif cl_sp == config.States.S_CLIENT_ON_BD.value:

# 			bot.send_message(str(config.dariy), message.text + '\n\nСообщение перехвачено от клиента ' + message.chat.id)

# 		elif cl_sp == config.States.F_SUPPORT_CLIENT.value:
# 			print(str(main.get_client()))
# 			# msg = 'Сообщение отправлено от:'+ config.support_name(message.chat_id) + '\n\n' + message.text
# 			# print(msg)
# 			# print(main.set_client())
# 			bot.send_message(str(main.get_client()), 'Сообщение отправлено от:'+ config.support_name(message.chat.id) + '\n\n' + message.text)
# 			print('!!!')

# 		else:

# 			print(' === ' + 'dialog' + ' === ' + str(message.chat.id))

# 	except:

# 		print(' === ' + ' ERROR IN dialog' + ' === ' + str(message.chat.id))

# if __name__ == "__main__":
#     bot.polling(none_stop=True)