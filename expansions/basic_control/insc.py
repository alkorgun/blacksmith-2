# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	control_answers = [x.decode("utf-8") for x in [
		"Внимание! %s (%s) загнал меня в -» '%s'", # 0
		"\nПричина: %s", # 1
		"Ага я зашел в -» '%s'", # 2
		"Не смог зайти в -» '%s'", # 3
		"АХТУНГ! %s (%s) выгнал меня из -» '%s'", # 4
		"Конференция итак находится в списке.", # 5
		"Судя по всему «%s» - это вообще не конференеция. Не пойду.", # 6
		"I'm %s -» XMPP BOT. Пришел по приказу %s", # 7
		"Реджойн по команде от %s", # 8
		"Ухожу по приказу %s", # 9
		"Ушел из -» '%s'", # 10
		"Перезагрузка по команде от %s", # 11
		"Выключение по команде от %s", # 12
		"\nЗанёс конференцию в список и буду пытаться в неё зайти. Если ты не уверен, что этот сервер существует - скомандуй выход.", # 13
		"Не могу. Прилежащий к этой конфе жид - сейчас оффлайн.", # 14
		"Не могу создать директорию, вероятно «%s» содержит запрещённые символы. Соответственно, я не могу обслуживать эту конференцию.", # 15
		"Система не может выделить ресурсы на ещё один клиент.", # 16
		"«%s» нет в списке клиентов." # 17
					]]
else:
	control_answers = [
		"Attention! %s (%s) sent me in to -> '%s'", # 0
		"\nReason: %s", # 1
		"I have joined -> '%s'", # 2
		"I can't join -> '%s'", # 3
		"Attention! %s (%s) ordered me to leave -> '%s'", # 4
		"Chat is already in list.", # 5
		"Apparently '%s' isn't a conference. I wouldn't join it.", # 6
		"I'm %s -» XMPP BOT. Joined by order from %s", # 7
		"Rejoin by command from %s", # 8
		"Leaved by command from %s", # 9
		"I came out from -> '%s'", # 10
		"Restart by command from %s", # 11
		"Shutdown by command from %s", # 12
		"I added this conference in to chat-list and I'll retry to join it. If you not sure that this server exists - you should to type leave command.", # 13
		"I can't. Client which assigned to this conference - currently offline.", # 14
		"Unable to create directory, probably '%s' contains invalid characters. Accordingly, I can't serve this conference.", # 15
		"The system can not allocate resources to another client.", # 16
		"'%s' not in clients list." # 17
					]