# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	iq_answers = [x.decode("utf-8") for x in [
		"Понг - %s сек.", # 0
		"Понга нет. Ответ на версию (%s) за %s секунд.", # 1
		"Ни пинга, ни версии...", # 2
		"\nСтатистика пинга (всего %s):\nСамый быстрый пинг - %s\nСамый медленный пинг - %s\nСреднее время пинга - %s", # 3
		"Нет статистики.", # 4
		"«%s» - сейчас нет в чате.", # 5
		"Нет ответа.", # 6
		"Время работы «%s» - %s.", # 7
		"Послеедняя активность «%s» - %s назад." # 8
					]]
else:
	iq_answers = [
		"Pong - %s sec.", # 0
		"No pong. Answer for version (%s) in %s sec.", # 1
		"No pong, no version...", # 2
		"\nPing statistics (total %s):\nFastest - %s\nSlowest - %s\nAverage time - %s", # 3
		"No statistics.", # 4
		"«%s» - isn't here now.", # 5
		"No answer.", # 6
		"%s's uptime is %s.", # 7
		"%s's last activity was %s ago." # 8
					]