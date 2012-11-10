# -*- coding: utf-8 -*-

if DefLANG in ("RU", "UA"):
	AnsBase = tuple([line.decode("utf-8") for line in (
		"Данная команда доступна исключительно в конференциях.", # 0
		"Данная команда подразумевает использование параметров.", # 1
		"Инвалид синтакс.", # 2
		"«%s» нет в списке конференций.", # 3
		"Сделано.", # 4
		"Слишком длинные параметры.", # 5
		"Нет такой команды.", # 6
		"Не могу.", # 7
		"Меня нет в этой конференции.", # 8
		"Тип указан не корректно.", # 9
		"Недостаточный доступ.", # 10
		"Ответ в привате.", # 11
		"№ %d. - %s", # 12
		"Команды «%s» (%s)", # 13
		"Процесса «%s»", # 14
		"При выполнении %s --» произошла ошибка!", # 15
		"Ошибку смотри по команде --» 'ошибка %d' (Крэшфайл --» %s)", # 16
		"Ошибку смотри по командам --» 'ошибка %d', 'sh cat %s'", # 17
		"%s[...]\n\n** Лимит %d знаков! Продолжение по команде «далее».", # 18
		"Команда '%s' сейчас недоступна!", # 19
		"Ошибка %s (%s) - конфа: «%s».", # 20
		"Ошибка %s (%s), полный выход из «%s».", # 21
		"Ошибка %s (%s), пришлось выйти из «%s».", # 22
		"Отказываюсь работать без прав!", # 23
		"Отключаю все функции до получения прав админа!", # 24
		"Получение прав...", # 25
		"Статускод '%s' в %s (%s). Осуществляю полный выход!", # 26
		"Помощь по команде «ХЕЛП» (последнее действие - %s)", # 27
		"Клиент «%s» упал!", # 28
		"JID «%s» используется в другом клиенте! (отключаю его)", # 29
		"Это не число." # 30
					)])
else:
	AnsBase = (
		"This command is available only in the conferences.", # 0
		"This command implies arguments using.", # 1
		"Invalid syntax.", # 2
		"There is no '%s' in the chats-list.", # 3
		"Done.", # 4
		"Parameters should be shorter.", # 5
		"Such command isn't exist.", # 6
		"I can't.", # 7
		"There is no such conference in my list.", # 8
		"Type is invalid.", # 9
		"You need to access higher.", # 10
		"You should look into private.", # 11
		"# %d. - %s", # 12
		"command '%s' (%s)", # 13
		"prosess '%s'", # 14
		"When execut %s --> error happend!", # 15
		"Type --> 'excinfo %d' to show error (crashfile --> %s)", # 16
		"Type --> 'excinfo %d' or 'sh cat %s' to show error", # 17
		"%s[...]\n\n** %d symbols limit! Type 'more' to show rest of the text.", # 18
		"Command '%s' is unavalable now!", # 19
		"Error %s (%s) - conference: '%s'.", # 20
		"Error %s (%s), full exit from '%s'.", # 21
		"Error %s (%s), I leaved '%s'.", # 22
		"The service without admin's affilation is unavalable!", # 23
		"I disable all functions until I'll become an admin!", # 24
		"Obtaining rights...", # 25
		"sCode '%s' in %s (%s). Full leave!", # 26
		"Type 'HELP' to know more (the last action - %s)", # 27
		"Client '%s' fell!", # 28
		"JID '%s' used in another client! (I have to disconnect it)", # 29
		"This is not a number." # 30
					)