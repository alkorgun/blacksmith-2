# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Сдаётся мне '%s' сейчас оффлайн.", # 0
		"Сдаётся мне '%s' итак закреплён за этой конфой.", # 1
		"'%s' нет среди доступных клиентов!", # 2
		"Смена jid'а...", # 3
		"Переименовался в «%s».", # 4
		"В моём нике не должно быть больше 16ти символов.", # 5
		"Префикс удалён.", # 6
		"Префикс и без того отсутствует.", # 7
		"Отныне знак '%s' является префиксом здесь.", # 8
		"Знак '%s' итак префикс здесь.", # 9
		"Недоступный знак для префикса! Доступные: '%s'.", # 10
		"'%s' является здесь префиксом.", # 11
		"Префикс не установлен.", # 12
		"Статус '%s' мне неизвестен." # 13
					)])
else:
	AnsBase_temp = (
		"I can't, because '%s' is offline.", # 0
		"'%s' is already owned by this conference.", # 1
		"'%s' not in available clients.", # 2
		"Jabber ID changing...", # 3
		"My new nick is '%s'.", # 4
		"My nick can't be longer than 16 symbols.", # 5
		"The prefix was deleted.", # 6
		"So there is no prefix.", # 7
		"'%s' is prefix here now.", # 8
		"So symbol '%s' is prefix here.", # 9
		"Unavailable symbol for prefix! Available: '%s'.", # 10
		"'%s' is current prefix here.", # 11
		"The prefix wasn't set.", # 12
		"'%s' isn't a status." # 13
					)