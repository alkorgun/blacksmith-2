# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Протоколы безопасности конференции запрещают мне выполнить твою команду.", # 0
		"Дай админа/модера, потом поговорим.", # 1
		"Задача выполнена в %(done)d, отклонена в %(fail)d, а также нет ответа из %(none)d конференций.", # 2
		"Задача выполнена в %(done)d, отклонена в %(fail)d конференциях.", # 3
		"Задача выполнена во всех конференциях." # 4
					)])
else:
	AnsBase_temp = (
		"Security protocols are prohibits this action.", # 0
		"I must to be admin/moder, to do this.", # 1
		"The task is executed in %(done)d, rejected in %(fail)d, and no response from %(none)d conferences.", # 2
		"The task is executed in %(done)d, rejected in %(fail)d conferences.", # 3
		"The task is executed in all of the conferences." # 4
					)