# -*- coding: utf-8 -*-
import dbworker # осуществляет работу с однофайловой БД
from enum import Enum 

token="468817404:AAEC2emjH4f1-wNpgZM-CUKGukjLrEe_hwQ"
# токен бота! самое важное! храним как зенитцу ока!!


channel_id ='-1001256652745'
# id канала поддержки
group_id = '-1001226003947'
# id группы поддержки
db_file = "database.vdb"
# база данных для статусов пользователей

state_pull = "0123456789"
# набор состояний пользователя в процессе составления заявки

# жестко записанные id оператопров и пароли доступа
ulahin = 88168468 
u_pass = "1111"
dariy = 282726944
d_pass = "2222"
volihina = 387253995
v_pass = "3333"

contact_message = "<cm>"
# сообщение с контактныеми данными

command_list = "<cl>"
# список комманд для пользователя

def create_order_bd(chat_id):
	# создает файл для хранения информации о заявки

	try:
		
		a = dbworker.get_order_state(chat_id, 'ChatID')
		# проверяет, есть ли файл с таким именем

	except:
		# если нет, создает

		bd = str(chat_id)
		order_file = open(bd + ".vdb" , 'a')
		order_file.close()

def support_name(chat_id):
	# для возврата имени операторов поодержки

	if chat_id == ulahin:

		return('Уляхин А.')

	elif chat_id == volihina:

		return('Волыхина М.')

	elif chat_id == dariy:

		return('Дарий В.')

	return('None')



class States(Enum):
	"""
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
	ZERO = "00"
	S_START = "0"  # Начало нового диалога

	S_SUPPORT_LINE = "1"
	S_ENTER_COMPANY_SIZE = "2"
	S_ENTER_COMPANY_NAME = "3"
	S_ENTER_CONTACT_NAME = "4"
	S_CHOOSE_CONTACT_CHANAL = "5"
	S_CONTACT_PHONE = "6"
	S_CONTACT_EMAIL = "7"
	S_TICKET= "8"
	S_CURRENT = "9"

	F_SUPPORT = "100"
	F_SUPPORT_LOGIN = "103"
	F_SUPPORT_SET = "102"
	F_SUPPORT_ON = "101"
	F_SUPPORT_CLIENT = "104"

	S_CLIENT_ON_IB = "88168468"
	S_CLIENT_ON_BD = "387253995"
	S_CLIENT_ON_CL = "282726944"
	
	S_CLIENT_ON_O = "-1001256652745"

