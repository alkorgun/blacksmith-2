# coding: utf-8

#  BlackSmith mark.2
exp_name = "game" # /code.py v.x1
#  Id: 26~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

GameDesc = {
	GameChrLS[0]: {
			GameChrLS[1]: 9,
			GameChrLS[3]: 2
					},
	GameChrLS[1]: {
			GameChrLS[2]: 0,
			GameChrLS[3]: 5
					},
	GameChrLS[2]: {
			GameChrLS[0]: 1,
			GameChrLS[4]: 7
					},
	GameChrLS[3]: {
			GameChrLS[2]: 6,
			GameChrLS[4]: 3
					},
	GameChrLS[4]: {
			GameChrLS[0]: 8,
			GameChrLS[1]: 4
					}
			}

del GameChrLS

def command_game(ltype, source, Char, disp):
	if Char:
		Char = Char.lower()
		if GameDesc.has_key(Char):
			Char_2 = choice(GameDesc.keys())
			Answer(Char_2, ltype, source, disp)
			time.sleep(3.2)
			if Char == Char_2:
				answer = GameAnsBase[0]
			elif GameDesc[Char_2].has_key(Char):
				answer = GameAnsBase[1] % (GameRules[GameDesc[Char_2][Char]])
			else:
				answer = GameAnsBase[2] % (GameRules[GameDesc[Char][Char_2]])
		else:
			answer = AnsBase[2]
	else:
		answer = str.join(chr(10), GameRules)
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_game])
expansions[exp_name].ls.extend(["GameAnsBase", "GameRules", "GameDesc"])

command_handler(command_game, {"RU": "игра", "EN": "game"}, 2, exp_name)
