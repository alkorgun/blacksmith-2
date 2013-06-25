# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Всего %d определений в глобальной базе:\n%s", # 0
		"Всего %d определений в базе %s:\n%s", # 1
		"Базы пусты.", # 2
		"%s - %d соответствий.", # 3
		"Нет соответсвий в базах.", # 4
		"\->\n%s:\n\t%s\n\nDefined by %s (on %s)", # 5
		"Определения «%s» в базе нет.", # 6
		"Всего %d определений в глобальной базе.", # 7
		"Всего %d определений в базе %s.", # 8
		"Определение «%s» уже есть в глобальной базе.", # 9
		"Не существует локальной базы для ростера.", # 10
		"\->\n" # -1
					)])
else:
	AnsBase_temp = (
		"There are %d definitions in global base:\n%s", # 0
		"There are %d definitions in the base of %s:\n%s", # 1
		"The bases are empty.", # 2
		"%s - %d hits.", # 3
		"No hits in the bases.", # 4
		"\->\n%s:\n\t%s\n\nDefined by %s (on %s)", # 5
		"There is no '%s' in the base.", # 6
		"There are %d definitions in the global base.", # 7
		"There are %d definitions in the base of %s.", # 8
		"'%s' is already in the global base.", # 9
		"There is no local base for the roster.", # 10
		"\->\n" # -1
					)