# coding: utf-8

if DefLANG in ["RU", "UA"]:
	AllwebAnsBase = [x.decode("utf-8") for x in [
		"Не могу получить доступ к странице.", # 0
		"Проблемы с разметкой...", # 1
		"Твоих запросов нет в базе.", # 2
		"Не вижу твоего JID'а, поэтому не могу найти твоих запросов в базе.", # 3
		"\n\n** Ещё %d результатов (командуй «гугл *»).", # 4
		"Ничего не найдено..." # 5
					]]
else:
	AllwebAnsBase = [
		"No access to the page.", # 0
		"Trouble with the marking...", # 1
		"There are no your requests in cache.", # 2
		"I can't find your requests in cache, because I don't know your JID.", # 3
		'\n\n** There are %d another results (type "google *").', # 4
		"No result..." # 5
					]