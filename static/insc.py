# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	AnsBase = [x.decode("utf-8") for x in [
		"данная команда доступна исключительно в конференциях", # 0
		"данная команда подразумевает использование параметров", # 1
		"инвалид синтакс", # 2
		"почитай-ка помощь по команде", # 3
		"сделано", # 4
		"слишком длинные параметры", # 5
		"нет такой команды", # 6
		"немогу", # 7
		"меня нет в этой конференции", # 8
		"тип указан не корректно", # 9
		"недостаточный доступ", # 10
		"ответ в привате", # 11
		"\n№ %d. - %s", # 12
		"команды «%s» (%s)", # 13
		"процесса «%s»", # 14
		"При выполнении %s --» произошла ошибка!", # 15
		"Ошибку смотри по команде --» `ошибка %d` (Крэшфайл --» %s)", # 16
		"Ошибку смотри по командам --» `ошибка %d`, `sh cat %s`", # 17
		"%s[...]\n\n** Лимит %d знаков! Продолжение по команде «далее».", # 18
		"Команда `%s` сейчас недоступна!", # 19
		"Ошибка %s (%s) - конфа: «%s»", # 20
		"Ошибка %s (%s), полный выход из «%s»", # 21
		"Ошибка %s (%s), пришлось выйти из «%s»", # 22
		"Отказываюсь работать без прав!", # 23
		"Отключаю все функции до получения прав админа!", # 24
		"Получение прав...", # 25
		"Статускод `%s` в %s (%s). Осуществляю полный выход!", # 26
		"Помощь по команде «ХЕЛП» (последнее действие - %s)", # 27
		"Клиент «%s» упал!", # 28
		"JID «%s» используется в другом клиенте! (отключаю его)", # 29
		"это не число" # 30
				]]
else:
	AnsBase = [
		"This command is available only in conferences", # 0
		"This command implies arguments using", # 1
		"Invalid syntax", # 2
		"You should to read commnad`s help", # 3
		"Done", # 4
		"Parameters should be shorter", # 5
		"Such command isn`t exists", # 6
		"I can`t", # 7
		"There is not such conference in my list", # 8
		"Type specified is incorrect", # 9
		"You need to access higher", # 10
		"You should to look in to your private", # 11
		"\n# %d. - %s", # 12
		"command `%s` (%s)", # 13
		"prosess `%s`", # 14
		"When execut %s --> error was happend!", # 15
		"Type --> `exception %d` to show error (crashfile --> %s)", # 16
		"Type --> `exception %d` or `sh %s` to show error", # 17
		"%s[...]\n\n** %d symbols limit! Type `more` to show rest of the text.", # 18
		"Command `%s` is unavalable now!" # 19
		"Error %s (%s) - conference: `%s`", # 20
		"Error %s (%s), full exit from `%s`", # 21
		"Error %s (%s), I leaved `%s`", # 22
		"Service without admin affilation is unavalable!", # 23
		"I Disable all functions until I`ll become an admin!", # 24
		"Obtaining rights...", # 25
		"sCode `%s` in %s (%s). Full leave!", # 26
		"Type HELP to know more (last action - %s)", # 27
		"Client `%s` falled!", # 28
		"JID `%s` used in another client! (I have to disconnect it)", # 29
		"This is not a number" # 30
				]