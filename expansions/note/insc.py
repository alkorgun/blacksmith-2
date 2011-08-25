# -*- coding: utf-8 -*-

if DefLANG in ["RU", "UA"]:
	note_answers = [x.decode("utf-8") for x in [
		"У тебя нет записей в блокноте.", # 0
		"Длинна одной записи не должна превышать 512 символов.", # 1
		"Не получится. Твой jid мне не известен.", # 2
		"Все 16 строк уже заполнены.", # 3
		"В блокноте 16 строк.", # 4
		"Эта строка - пуста.", # 5
		"Твои записи:%s", # 6
		"Запись добавлена под номером - %s.", # 7
		"Эта строка итак пуста." # 8
					]]
else:
	note_answers = [
		"Your note is empty.", # 0
		"Length of one line can't be more than 512 symbols.", # 1
		"No chance. I don't know your jid.", # 2
		"All of 16 lines are filled.", # 3
		"There are 16 lines in note.", # 4
		"This line is empty.", # 5
		"Your notes:%s", # 6
		"Recorded in line - %s.", # 7
		"This line is alredy empty." # 8
					]