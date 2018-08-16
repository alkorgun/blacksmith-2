# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Резервная копия темы не создана.", # 0
		"Резервная копия темы успешно создана.", # 1
		"Резервная копия списка '%ss' не создана.", # 2
		"Резервная копия списка '%ss' успешно создана.", # 3
		"Резервная копия опций не создана (вероятно у меня недостаточно прав).", # 4
		"Резервная копия опций успешно создана.", # 5
		"Сервер не принял сохраненную форму с опциями.", # 6
		"Сохранённое состояние настроек успешно восстановлено. Бекап от %s.", # 7
		"Список '%ss' успешно восстановлен. Бекап от %s.", # 8
		"Тема успешно восстановлена. Бекап от %s.", # 9
		"\nПоследние бекапы ->", # 10
		"Файл с бекапом опций - испорчен.", # 11
		"Чтобы создать/восстановить бекап, у меня должны быть права админа (как минимум).", # 12
		"Список овнеров не может быть восстановлен, для этого я сам должен иметь права владельца.", # 13
		"Нельзя создавать бекапы чаще одного раза в час! (Осталось: %s)", # 14
		"Сейчас обрабатывается другой запрос на восстановление, попробуйте позже.", # 15
		"Нельзя восстанавливать опции чаще одного раза в час! (Осталось: %s)", # 16
		"Нельзя восстанавливать список '%ss' чаще одного раза в час! (Осталось: %s)", # 17
		"Настройки не восстановлены, ибо мне небходимы права владельца.", # 18
		"Тебя нет в списке владельцев '%s', тебе нельзя копировать её настройки.", # 19
		"Не могу проверить твои полномочия по списку владельцев '%s'.", # 20
		"Конференцию можно копировать не чаще раза в сутки! (Осталось: %s)" # 21
	)])
else:
	AnsBase_temp = (
		"Backup of the subject is not created.", # 0
		"Backup of the subject is successfully created.", # 1
		"Backup of %ss list is not created.", # 2
		"Backup of %ss list is successfully created.", # 3
		"Backup of chat's options is not created (maybe I don't have enough rights).", # 4
		"Backup of chat's options is successfully created.", # 5
		"Server denied saved form of chat's optins.", # 6
		"Saved options successfully restored. Backup of %s.", # 7
		"The list of %ss successfully restored. Backup of %s.", # 8
		"The subject successfully restored. Backup of %s.", # 9
		"\nThe last backups ->", # 10
		"The file with saved options is corrupted.", # 11
		"I must be an admin (at least) to create/restore backups.", # 12
		"Owners list cant's be restored while I'm not an owner.", # 13
		"Backups can's be created often than the one time in hour! (Remain: %s)", # 14
		"Another request processed now, retry later.", # 15
		"An options can's be restored often than the one time in hour! (Remain: %s)", # 16
		"The list of %ss can's be restored often than the one time in hour! (Remain: %s).", # 17
		"An options can's be restored, because I'm not an owner.", # 18
		"Your JID not in owners list of '%s', you can't copy it's options.", # 19
		"I can't check your access by owners list of '%s'.", # 20
		"A conference can't be copied often than the one time in a day! (Remain: %s)" # 21
	)