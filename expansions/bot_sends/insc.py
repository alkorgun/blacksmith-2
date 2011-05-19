# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	bsends_answers = [x.decode("utf-8") for x in [
		"чистка конференции...", # 0
		"Всё круто, я в отличной форме! (0 ошибок)", # 1
		"Бoeц %s тяжело ранен, но я ещё повоюю! (%d ошибок)", # 2
		"Со мной всё кончено, брат, спасайся, я задержу их... (%d ошибок)", # 3
		"На такие адреса я не могу посылать сообщения.", # 4
		"Сообщение от %s:\n%s" # 5
					]]
else:
	bsends_answers = [
		"cleaning conference...", # 0
		"I am okay! (0 errors)", # 1
		"Private %s is seriously injured, but I have the rotation! (%d errors)", # 2
		"I am dead man, brother, escape, I will delay them... (%d errors)", # 3
		"At these addresses, I can not send messages.", # 4
		"Message from %s:\n%s" # 5
					]