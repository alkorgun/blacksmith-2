# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"чистка конференции...", # 0
		"Всё круто, я в отличной форме! (0 ошибок)", # 1
		"Бoeц %s тяжело ранен, но я ещё повоюю! (%d ошибок)", # 2
		"Со мной всё кончено, брат, спасайся, я задержу их... (%d ошибок)", # 3
		"На такие адреса я не могу посылать сообщения.", # 4
		"Сообщение от %s:\n%s", # 5
		"«%s» сейчас здесь.", # 6
		"Адресат неопределён.", # 7
		"Не более 1го приглащения за 12 минут! (Осталось: %s)", # 8
		"Чистка итак в процессе!" # 9
	)])
else:
	AnsBase_temp = (
		"cleaning conference...", # 0
		"I am okay! (0 errors)", # 1
		"Private %s is seriously injured, but I have the rotation! (%d errors)", # 2
		"I am a dead man, brother, you should escape, I'll delay them... (%d errors)", # 3
		"At these target, I can't send messages.", # 4
		"Message from %s:\n%s", # 5
		"'%s' is here now.", # 6
		"Unknown target.", # 7
		"Users can send only one invite in 12 minutes! (Remain: %s)", # 8
		"Cleaning already in the process!" # 9
	)