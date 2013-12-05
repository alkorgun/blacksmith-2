# coding: utf-8

#  BlackSmith mark.2
# exp_name = "game" # /code.py v.x2
#  Id: 26~2c
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

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

	GameRules = GameRules

	def command_game(self, stype, source, Char, disp):
		if Char:
			Char = Char.lower()
			if Char in self.GameDesc:
				Char_2 = choice(self.GameDesc.keys())
				Answer(Char_2, stype, source, disp)
				sleep(3.2)
				if Char == Char_2:
					answer = self.AnsBase[0]
				elif self.GameDesc[Char_2].has_key(Char):
					answer = self.AnsBase[1] % (self.GameRules[self.GameDesc[Char_2][Char]])
				else:
					answer = self.AnsBase[2] % (self.GameRules[self.GameDesc[Char][Char_2]])
			else:
				answer = AnsBase[2]
		else:
			answer = str.join(chr(10), self.GameRules)
		Answer(answer, stype, source, disp)

	commands = ((command_game, "game", 2,),)

del GameChrLS, GameRules
