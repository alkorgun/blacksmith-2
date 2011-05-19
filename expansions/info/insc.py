# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	info_answers = [x.decode("utf-8") for x in [
		"Сегодня здесь было %s юзеров:%s\n+ ещё %s досихпор здесь.", # 0
		"Сегодня при мне ещё никто не выходил, все кто был досихпор здесь.", # 1
		"При мне заходило %s юзеров:\n%s", # 2
		"Здесь было %s юзеров:%s\n+ ещё %s досихпор здесь.", # 3
		"При мне ещё никто не выходил, все кто был досихпор здесь.", # 4
		"[№] [Конфа/Ник] [Жид] [Префикc] [Юзеров] [Админ]", # 5
		"В списке конференций - пусто.", # 6
		"[№][Клиент][Коннект][Активен]", # 7
		"Список юзеров в чате:", # 8
		"Нашел %s похожих пользователей:%s", # 9
		"Не знаю." # 10
					]]
else:
	info_answers = [
		"Today there were %s visitors here:%s\n+ %s are still here.", # 0
		"Today when I was still nobody came, everyone who was - are still here.", # 1
		"When I was still there were %s visitors here:\n%s", # 2
		"There were %s visitors here:%s\n+ %s are still here.", # 3
		"При мне ещё никто не выходил, все кто был досихпор здесь.", # 4
		"[#] [Chat/Nick] [Jid] [Prefix] [Users] [Admin]", # 5
		"The list of conferences is empty.", # 6
		"[#][Client][Connected][isActive]", # 7
		"List of users:", # 8
		"Total %s similar users:%s", # 9
		"Don't know." # 10
					]