# coding: utf-8

#  BlackSmith mark.2
# exp_name = "cmd_control" # /code.py v.x2
#  Id: 32~2c
#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	TabooFile = "taboo.db"

	def command_taboo(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			oCmds = Chats[source[1]].oCmds
			if body:
				if enough_access(source[1], source[2], 6):
					ls = body.split()
					command = (ls.pop(0)).lower()
					if command in Cmds:
						if enough_access(source[1], source[2], Cmds[command].access):
							if command not in sCmds:
								if command in oCmds:
									oCmds.remove(command)
									answer = self.AnsBase[0] % (command)
								else:
									oCmds.append(command)
									answer = self.AnsBase[1] % (command)
								cat_file(chat_file(source[1], self.TabooFile), str(oCmds))
							else:
								answer = self.AnsBase[2]
						else:
							answer = AnsBase[10]
					elif command in oCmds:
						oCmds.remove(command)
						answer = AnsBase[4]
						cat_file(chat_file(source[1], self.TabooFile), str(oCmds))
					else:
						answer = AnsBase[6]
				else:
					answer = AnsBase[10]
			elif oCmds:
				answer = ", ".join(oCmds)
			else:
				answer = self.AnsBase[3]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	def init_taboo(self, conf):
		filename = chat_file(conf, self.TabooFile)
		if initialize_file(filename, "[]"):
			Chats[conf].oCmds = eval(get_file(filename))

	commands = ((command_taboo, "taboo", 1, False),)

	handlers = ((init_taboo, "01si"),)
