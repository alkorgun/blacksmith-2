# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Твой доступ - %s.", # 0
		"Доступ «%s» - %s.", # 1
		"На «%s» нет информации.", # 2
		"Нет глобальных доступов.", # 3
		"Нет локальных доступов.", # 4
		"Список доступов:\n", # 5
		"У «%s» итак нет доступа.", # 6
		"Нельзя дать доступ меньше -1 и больше 8.", # 7
		"Нельзя дать локальный доступ меньше 0 и больше 6.", # 8
		"У «%s» глобальный доступ.", # 9
		"Не могу дать доступ «%s»." # 10
	)])
else:
	AnsBase_temp = (
		"Your access - %s.", # 0
		"%s's access - %s.", # 1
		"I have no info about '%s'.", # 2
		"No global accesses.", # 3
		"No local accesses.", # 4
		"Access list:\n", # 5
		"So, '%s' has no access.", # 6
		"You can't give access < -1 & > 8.", # 7
		"You can't give local access < 0 & > 6.", # 8
		"'%s' has global access.", # 9
		"I can't give access to '%s'." # 10
	)