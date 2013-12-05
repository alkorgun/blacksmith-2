# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"\n*// Статистика работы (Pid: %d):", # 0
		"\n# Время работы %s", # 1
		"\n# Последняя сессия %s", # 2
		"\n# Получено %s сообщений", # 3
		"\n# Выполнено %s команд", # 4
		"\n# Обработано %s презенсов и %s iq-запросов", # 5
		"\n# Отправлено %s сообщений и %s iq-запросов", # 6
		"\n# Обслуживаю %d конференций", # 7
		"\n# Зафиксировано %d пользователей", # 8
		"", # 9
		"\n# Произошло %d ошибок и %s Dispatch-Errors", # 10
		"\n# Записей crash-логов %s", # 11
		"\n# Создано %s тредов, %d из них активно", # 12
		"\n# Потрачено %.2f секунд процессора", # 13
		"\n# Потрачено %s мегабайт оперативной памяти", # 14
		"\nВремя работы: %s.", # 15
		"\nПоследняя сессия: %s.\nВсего %s перезагрузок:\n%s.", # 16
		" - Работаю без перезагрузок!", # 17
		"\nСтатистика по команде '%s':\nВсего использовали - %s раз (%d юзеров).", # 18
		"\n[№][Команда][Использований][Юзеров]\n", # 19
		"Невозможно отправить ошибку, смотри к крешлогах.", # 20
		"Ошибки №%s не существует!", # 21
		"Всего произошло %d ошибок." # 22
	)])
else:
	AnsBase_temp = (
		"\n*// Session's statistics (Pid: %d):", # 0
		"\n# Bot's uptime %s", # 1
		"\n# The last working set %s", # 2
		"\n# Obtained %s messages", # 3
		"\n# Completed %s commands", # 4
		"\n# Processed %s presences & %s iq-requests", # 5
		"\n# Sent %s messages & %s iq-requests", # 6
		"\n# Serve %d conferences", # 7
		"\n# Counted %d users", # 8
		"", # 9
		"\n# Happened %d exceptions & %s Dispatch-Errors", # 10
		"\n# Wrote %s crash logs", # 11
		"\n# Created %s threads, %d is now active", # 12
		"\n# Used %.2f processor's seconds", # 13
		"\n# Used %s megabytes RAM", # 14
		"\nBot's uptime: %s.", # 15
		"\nThe last working set: %s.\nReloads (%s):\n%s.", # 16
		" - Working without restarts!", # 17
		"\nCommand '%s' usage statistics:\nTotal used - %s times (%d users).", # 18
		"\n[#][Command][Used][Users]\n", # 19
		"Unable to send error, look for crash logs.", # 20
		"Exception #%s isn't exists!", # 21
		"Total %d exceptions happened." # 22
	)