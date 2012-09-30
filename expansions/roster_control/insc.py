# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Такого jid'а нет в ростере этого клиента.", # 0
		"Ростер пуст.", # 1
		"У меня нет такого jid'а.", # 2
		"Доступ в ростер свободный.", # 3
		"Доступ в ростер ограничен." # 4
					)])
else:
	AnsBase_temp = (
		"This jid isn't in that client's roster.", # 0
		"The roster is empty.", # 1
		"It isn't my jid.", # 2
		"Access to the roster is free.", # 3
		"Access to the roster is blocked." # 4
					)