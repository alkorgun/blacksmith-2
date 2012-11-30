# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Сегодня здесь было %s юзеров:%s\n+ ещё %s до сих пор здесь.", # 0
		"Сегодня при мне ещё никто не выходил, все кто был до сих пор здесь.", # 1
		"При мне заходило %s юзеров:\n%s", # 2
		"Здесь было %s юзеров:%s\n+ ещё %s досихпор здесь.", # 3
		"При мне ещё никто не выходил, все кто был досихпор здесь.", # 4
		"[№] [Конфа/Ник] [Жид] [Префикc] [Юзеров] [Роль]", # 5
		"В списке конференций - пусто.", # 6
		"[№][Клиент][Коннект][Активен]", # 7
		"Список юзеров в чате:", # 8
		"Нашел %s похожих пользователей:\n%s", # 9
		"Не знаю." # 10
					)])
else:
	AnsBase_temp = (
		"Today there were %s visitors here:%s\n+ %s are still here.", # 0
		"Today, when I was still, nobody came, everyone who was - are still here.", # 1
		"When I was still, there were %s visitors here:\n%s", # 2
		"There were %s visitors here:%s\n+ %s are still here.", # 3
		"Nobody leaved, all users are steel here.", # 4
		"[#] [Chat/Nick] [Jid] [Prefix] [Users] [Role]", # 5
		"The list of conferences is empty.", # 6
		"[#][Client][Connected][isActive]", # 7
		"Users-list:", # 8
		"Total %s similar users:\n%s", # 9
		"No result." # 10
					)