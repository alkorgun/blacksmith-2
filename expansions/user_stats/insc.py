# coding: utf-8

if DefLANG in ("RU", "UA"):
	UstatAnsBase = tuple([line.decode("utf-8") for line in (
		"\nВсего входов - %d\nВремя последнего входа - %s\nПоследняя роль - %s", # 0
		"\nВремя последнего выхода - %s\nПричина выхода - %s", # 1
		"\nНики: %s", # 2
		"нет статистики", # 3
		"«%s» сидит здесь - %s", # 4
		"ты провёл здесь - %s", # 5
		"здесь нет такого юзера" # 6
					)])
else:
	UstatAnsBase = (
		"\nTotal joins - %d\nLast join time - %s\nLast role - %s", # 0
		"\nLast leave time - %s\nExit reason - %s", # 1
		"\nNicks: %s", # 2
		"no statistics", # 3
		"'%s' spent here - %s", # 4
		"You spent here - %s", # 5
		"No sutch user here" # 6
					)