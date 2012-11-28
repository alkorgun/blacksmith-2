# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Изменённые пункты: %s", # 0
		"Очевидно параметры неверны.", # 1
		"Настройки:\n", # 2
		"Конфиг пуст.", # 3
		"Вниание! Текущий jid сейчас удаляется, сейчас я зайду с нового.", # 4
		"смена jid'а", # 5
		"Теперь '%s' - мой основной JID.", # 6
		"Нельзя! Итак подключен всего один клиент.", # 7
		"Система не может выделить ресурсы на ещё один клиент.", # 8
		"Не коннектится.", # 9
		"Этот jid уже есть в списках.", # 10
		"«%s» нет в списке клиентов.", # 11
		"«%s» сейчас оффлайн." # 12
					)])
else:
	AnsBase_temp = (
		"Changed options: %s", # 0
		"Parameters are incorrect.", # 1
		"Config:\n", # 2
		"Config is empty.", # 3
		"Attention! Current jid deleting now. I'll rejoin with new.", # 4
		"jid change", # 5
		"'%s' - my main JID now.", # 6
		"Forbidden!", # 7
		"The system can not allocate resources to another client.", # 8
		"No connection.", # 9
		"This jid is already in list.", # 10
		"'%s' not in clients-list.", # 11
		"'%s' is offline." # 12
					)