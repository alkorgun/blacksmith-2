# coding: utf-8

if DefLANG in ("RU", "UA"):
	RosterAnsBase = tuple([line.decode("utf-8") for line in (
		"Такого jid'а нет в ростере этого клиента.", # 0
		"Ростер пуст.", # 1
		"У меня нет такого jid'а." # 2
					)])
else:
	RosterAnsBase = (
		"This jid isn't in that client's roster.", # 0
		"Roster is empty.", # 1
		"It isn't my jid." # 2
					)