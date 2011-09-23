# coding: utf-8

if DefLANG in ("RU", "UA"):
	SstatAnsBase = tuple([line.decode("utf-8") for line in (
		"\n*// Статистика работы (Pid: %d):", # 0
		"\n-//- Время работы %s", # 1
		"\n-//- Последняя сессия %s", # 2
		"\n-//- Получено %s сообщений", # 3
		"\n-//- Выполнено %s команд", # 4
		"\n-//- Обработано %s презенсов и %s iq-запросов", # 5
		"\n-//- Отправлено %s сообщений и %s iq-запросов", # 6
		"\n-//- Создано файлов %s", # 7
		"\n-//- Прочтений файлов %s", # 8
		"\n-//- Записей в файлах %s", # 9
		"\n-//- Произошло %d ошибок и %s Dispatch Errors", # 10
		"\n-//- Записей crash логов %s", # 11
		"\n-//- Создано %s тредов, %d из них активно", # 12
		"\n-//- Потрачено %.2f секунд процессора", # 13
		"\n-//- Потрачено %s мегабайт оперативной памяти", # 14
		"\nВремя работы: %s", # 15
		"\nПоследняя сессия: %s\nВсего %s перезагрузок:\n%s", # 16
		" - Работаю без перезагрузок!", # 17
		"\nСтатистика по команде '%s':\nВсего использовали - %s раз (%d юзеров)", # 18
		"\n[№][Команда][Использований][Юзеров]", # 19
		"Невозможно отправить ошибку, смотри к крешлогах.", # 20
		"Ошибки №%s не существует!", # 21
		"Всего произошло %d ошибок." # 22
					)])
else:
	SstatAnsBase = (
		"\n*// Session statistics (Pid: %d):", # 0
		"\n-//- Bot uptime %s", # 1
		"\n-//- Last working set %s", # 2
		"\n-//- Obtained %s messages", # 3
		"\n-//- Completed %s commands", # 4
		"\n-//- Processed %s presences & %s iq-request", # 5
		"\n-//- Sent %s messages & %s iq-request", # 6
		"\n-//- Created %s files", # 7
		"\n-//- Read %s files", # 8
		"\n-//- Wrote %s files", # 9
		"\n-//- Happened %d exceptions & %s Dispatch Errors", # 10
		"\n-//- Wrote crash logs %s", # 11
		"\n-//- Created %s threads, %d is now active", # 12
		"\n-//- Used %.2f processor seconds", # 13
		"\n-//- Used %s megabyte RAM", # 14
		"\nBot uptime: %s", # 15
		"\nLast working set: %s\nReloads (%s):\n%s", # 16
		" - Work without reboots!", # 17
		"\nCommand '%s' usage statistics:\nTotal used - %s times (%d users)", # 18
		"\n[#][Command][Used][Users used]", # 19
		"Unable to send error, look for crash logs.", # 20
		"Exception #%s isn't exists!", # 21
		"Total %d exceptions happened." # 22
					)