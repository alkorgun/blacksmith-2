# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Результаты будут в привате через 80 секунд.", # 0
		"На «%s» нельзя искать.", # 1
		"Проверено %s конференций, найдено %d похожих ников:\n%s", # 2
		"Проверено %s конференций, безрезультатно.", # 3
		"Сейчас обрабатывается другой поисковый запрос. Подожди %s." # 4
	)])
else:
	AnsBase_temp = (
		"I'll send the results after 80 seconds in private.", # 0
		"Search at '%s' is not available.", # 1
		"Checked %s chatrooms, found %d similar nicks:\n%s", # 2
		"Checked %s chatrooms, but no matches.", # 3
		"Now I'm busy with another search query. Wait %s." # 4
	)