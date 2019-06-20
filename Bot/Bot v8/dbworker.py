# -*- coding: utf-8 -*-

from vedis import Vedis
import config

# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id]
        except KeyError:  # Если такого ключа почему-то не оказалось
            return config.States.S_START.value  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            print('111')
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False

def get_order_state(user_id, stateD):
    with Vedis(str(user_id) + ".vdb") as db:
        try:
            return db[stateD]
        except KeyError:  # Если такого ключа почему-то не оказалось
            return config.States.ZERO.value  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_order_state(user_id, stateD, value):
    with Vedis(str(user_id) + ".vdb") as db:
        try:
            db[stateD] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False