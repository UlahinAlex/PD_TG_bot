# -*- coding: utf-8 -*-

from enum import Enum

token="468817404:AAEC2emjH4f1-wNpgZM-CUKGukjLrEe_hwQ"
db_file = "database.vdb"


class States(Enum):
	"""
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
	F_SUPPORT = "0"  # Начало нового диалога
	F_CLIENT = "1"
	F_SUPPORT_CLIENT = "2"
	F_CLIENT_SUPPORT = "3"
	S_CLIENT_ON_IB = "88168468"
	S_CLIENT_ON_BD = "387253995"
	S_CLIENT_ON_CL = "282726944"
	S_CLIENT_ON_O = "-1001226003947"

	
