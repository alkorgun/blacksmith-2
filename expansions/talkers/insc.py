# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	talkers_answers = [x.decode("utf-8") for x in [
		"\n[№][Юзер][Фраз][Слов][Коэф.]", # 0
		"нет статистики", # 1
		"\n[Фраз][Слов][Коэф.]\n%d\t%d\t%s", # 2
		"\n*! Поиск в базе произведён по ключу." # 3
					]]
else:
	talkers_answers = [
		"\n[#][User][Messages][Words][Coef.]", # 0
		"no statistics", # 1
		"\n[Messages][Words][Coef.]\n%d\t%d\t%s", # 2
		"\n*! Search the database produced by the key." # 3
					]