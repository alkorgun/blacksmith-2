# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Ты просил выполнить «%s».", # 0
		"Нет задания с ID'ом «%d».", # 1
		"Слишком быстро и часто. (при количестве циклов больше 4х - тайм-аут должен превышать 4 минуты)", # 2
		"\n+ ещё %d раз(а).", # 3
		"Выполню в:\n%s", # 4
		"Тайм-аут не может быть меньше минуты и больше 48 дней.", # 5
		"Выполню в %s.", # 6
		"Нет запланированных заданий.", # 7
		"\n[№][ID][Команда][Deadline]\n%s", # 8
		"Дата/Время введены некорректно." # 9
					)])
else:
	AnsBase_temp = (
		"You asked to execute '%s'.", # 0
		"There is no task with ID '%d'.", # 1
		"Too quickly and often. (when the number of cycles greater than 4 - timeout must exceed 4 minutes)", # 2
		"\n+ %d more times.", # 3
		"It will be executed at:\n%s", # 4
		"The timeout can't be less than 60 seconds and more than 48 days.", # 5
		"It will be executed at %s.", # 6
		"There are no tasks.", # 7
		"\n[#][ID][Command][Deadline]\n%s", # 8
		"Date/Time is incorrect." # 9
					)