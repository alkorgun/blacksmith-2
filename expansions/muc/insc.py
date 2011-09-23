# coding: utf-8

if DefLANG in ("RU", "UA"):
	MucAnsBase = tuple([line.decode("utf-8") for line in (
		"Протоколы безопасности конференции запрещают мне выполнить твою команду.", # 0
		"Дай админа/модера, потом поговорим." # 1
					)])
else:
	MucAnsBase = (
		"Security protocols are prohibits this action.", # 0
		"I must to be admin/moder to do this." # 1
					)