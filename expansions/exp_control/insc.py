# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"\n[Название][состояние][файл кода][языковой файл]", # 0
		"в наличии", # 1
		"отсутствует", # 2
		"загружен", # 3
		"\nКоманды: %s", # 4
		"\nФункции: %s", # 5
		"не загружен", # 6
		"Судя по всему нет такого плагина.", # 7
		"\n[№][Название][файл кода][файл языка]", # 8
		"\n\n## Незагруженные (%d) -»\n\n%s", # 9
		"%s - успешно загружен!", # 10
		"Не могу загрузить - %s!%s", # 11
		"Какой-то гад удалил файл с кодом!", # 12
		"\n\n** Загрузил последнюю рабочую версию плагина.", # 13
		"Этой функции нет в списке зарегистрированных.\n## Список зареганных: %s", # 14
		"В %s нет зарегистрированных функций.", # 15
		"Команда «%s» включена.", # 16
		"Команда «%s» отключена.", # 17
		"Нет отключенных команд." # 18
					)])
else:
	AnsBase_temp = (
		"\n[Name][state][code-file][lang-file]", # 0
		"exists", # 1
		"not exists", # 2
		"loaded", # 3
		"\nCommands: %s", # 4
		"\nHandlers: %s", # 5
		"not loaded", # 6
		"Also, this expansion isn't exist.", # 7
		"\n[#][Name][code-file][lang-file]", # 8
		"\n\n## Not loaded (%d) ->\n\n%s", # 9
		"%s - successfully loaded!", # 10
		"Can't load - %s!%s", # 11
		"Somebody deleted code-file!", # 12
		"\n\n** The last valid version of the expansion was loaded.", # 13
		"This function isn't registered.\n## Functions-list: %s", # 14
		"There is no registered functions in %s", # 15
		"Command '%s' is on.", # 16
		"Command '%s' is off.", # 17
		"No disabled commands." # 18
					)