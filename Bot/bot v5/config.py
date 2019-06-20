# -*- coding: utf-8 -*-

from enum import Enum

token="468817404:AAEC2emjH4f1-wNpgZM-CUKGukjLrEe_hwQ"
db_file = "database.vdb"


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
