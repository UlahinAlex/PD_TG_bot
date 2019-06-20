# -*- coding: utf-8 -*-

from enum import Enum

token="468817404:AAEC2emjH4f1-wNpgZM-CUKGukjLrEe_hwQ"
channel_id ='-1001256652745'
group_id = '-1001226003947'
db_file = "database.vdb"

ulahin = 88168468
dariy = 282726944
volihina = 387253995


def support_name(chat_id):

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
	S_CLIENT_ON_IB = "88168468"
	S_CLIENT_ON_BD = "387253995"
	S_CLIENT_ON_CL = "282726944"
	S_CLIENT_ON_O = "-1001256652745"

