/start  Выводит приветсвенное сообщение и предлагает начать подачу заявки 
	# Добрый день!
	# Вы обратились к автоматизированной системе приема и обработки заявок отдела Цифровой дистрибьюции компании 1С:Северо-Запад.
	# Для составления заявки используйте комманду /order и сделуйте инструкциям!
/order	Начинает собирать информацию для подачи заявки задавая пользователю наводящие вопросы
	partner		- Является ли парнером. (Y/N)
		если Y
			prtner_index	- Запрашиваем инд.идентификатор партнера
	corp_name	- Имя организации








Для создания лида необходимо:
Автоматически:
1. Дата поступления 			- берет системное время
2. Ответсвенный					- назначается по выбранному продукту (необходимо dafault значение)
	Запрос у пользователя
	3. Тип компании 			- выбор по средством "/тип_компании"
		5.* ID Партнера 		- в случии если выбран тип "/партнер"
	4. Компания 				- Блок "Контактные данные": от пользователя требуется ввести данные через ввод с новой строки, в определенном порядке
	6. Фамилия 					- Блок "Контактные данные"
	7. Имя						- Блок "Контактные данные"
	8. e-mail					- Блок "Контактные данные"
	9. Телефон					- Блок "Контактные данные"
	13. Цель запроса			- Запрашивается отдельно.
		Не спрашивать у пользователя. (Необходимы dafault значения)
		10. Тип запроса			- 
		11. Вендор				- 
		12. Продукт 			- 