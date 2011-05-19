# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	help_answers = [x.decode("utf-8") for x in [
		"Команда «%s» находится в плагине -» %s", # 0
		"Доступ к команде «%s» - %d", # 1
		"\n%s\nСинтаксис:\n»»» %s", # 2
		"\nПримеры:", # 3
		"Файл с описанием этой команды отсутствует...", # 4
		"Пиши «комлист» для получения полного списка команд, пиши «хелп [команда]» чтобы понять как она работает", # 5
		"Полный список команд%s", # 6
		" (Командный префикс - «%s»):", # 7
		"\n\n• Команды для Суперадмина [доступ 8] - %s:\n%s", # 8
		"\n\n• Команды для Глоб.Админов [доступ 7] - %s:\n%s", # 9
		"\n\n• Команды для Владельцев [доступ 6] - %s:\n%s", # 10
		"\n\n• Команды для Админов [доступ 5] - %s:\n%s", # 11
		"\n\n• Команды для Модеров/Мемберов [доступ 4] - %s:\n%s", # 12
		"\n\n• Команды для Модеров [доступ 3] - %s:\n%s", # 13
		"\n\n• Команды для Участников/Мемберов [доступ 2] - %s:\n%s", # 14
		"\n\n• Команды для Участников [доступ 1] - %s:\n%s", # 15
		"\n\nТвой уровень доступа - %s", # 16
		"Файл со справкой повреждён!" # 17
					]]
else:
	help_answers = [
		"Command `%s` located in expansion %s", # 0
		"%s`s access - %d", # 1
		"\n%s\nSyntax:\n*** %s", # 2
		"\nExamples:", # 3
		"Help-file for this command isn`t exists...", # 4
		"Type `commands` for a complete list of commands, type `help [command]` to know how it works", # 5
		"Full command list%s", # 6
		" (Command prefix - `%s`):", # 7
		"\n\n### Superadmin`s commands [access 8] - %s:\n%s", # 8
		"\n\n### Global Admin`s commands [access 7] - %s:\n%s", # 9
		"\n\n### Owner`s commands [access 6] - %s:\n%s", # 10
		"\n\n### Admin`s commands [access 5] - %s:\n%s", # 11
		"\n\n### Moder/Member`s commands [access 4] - %s:\n%s", # 12
		"\n\n### Moder`s commands [access 3] - %s:\n%s", # 13
		"\n\n### User/Member`s commands [access 2] - %s:\n%s", # 14
		"\n\n### User`s commands [access 1] - %s:\n%s", # 15
		"\n\nYour access level - %s", # 16
		"Help file is damaged!" # 17
					]