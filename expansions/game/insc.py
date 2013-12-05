# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Ничья.", # 0
		"%s\n\t»» Я победил!", # 2
		"%s\n\t»» Ты победил." # 3
	)])

	GameRules = tuple([Rule.decode("utf-8") for Rule in (
		"Ножницы режут бумагу.", # 0
		"Бумага обхватывает камень.", # 1
		"Камень давит ящерицу.", # 2
		"Ящерица отравляет Спока.", # 3
		"Спок ломает ножницы.", # 4
		"Ножницы обезглавливают ящерицу.", # 5
		"Ящерица ест бумагу.", # 6
		"Бумага компрометирует Спока.", # 7
		"Спок испаряет камень.", # 8
		"Камень ломает ножницы." # 9
	)])

	GameChrLS = tuple([Char.decode("utf-8") for Char in (
		"камень", # 0
		"ножницы", # 1
		"бумага", # 2
		"ящерица", # 3
		"спок" # 4
	)])
	
	del Char, Rule
else:
	AnsBase_temp = (
		"Draw.", # 1
		"%s\n\t>> I won!", # 2
		"%s\n\t>> You won." # 3
	)

	GameRules = (
		"Scissors cut paper.", # 0
		"Paper covers rock.", # 1
		"Rock crushes lizard.", # 2
		"Lizard poisons Spock.", # 3
		"Spock smashes scissors.", # 4
		"Scissors decapitate lizard.", # 5
		"Lizard eats paper.", # 6
		"Paper disproves Spock.", # 7
		"Spock vaporizes rock.", # 8
		"Rock crushes scissors." # 9
	)

	GameChrLS = (
		"rock", # 0
		"scissors", # 1
		"paper", # 2
		"lizard", # 3
		"spock" # 4
	)