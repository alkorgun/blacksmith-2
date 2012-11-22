# coding: utf-8

#  BlackSmith mark.2
exp_name = "help" # /code.py v.x5
#  Id: 03~2a
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_location(self, ltype, source, body, disp):
		if body:
			command = body.lower()
			if Cmds.has_key(command):
				answer = self.AnsBase[0] % (command, Cmds[command].exp.name.upper())
			else:
				answer = AnsBase[6]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_comacc(self, ltype, source, body, disp):
		if body:
			command = body.lower()
			if Cmds.has_key(command):
				answer = self.AnsBase[1] % (command, Cmds[command].access)
			else:
				answer = AnsBase[6]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_help(self, ltype, source, body, disp):
		if body:
			command = body.lower()
			if Cmds.has_key(command):
				if os.path.isfile(Cmds[command].help):
					help = get_file(Cmds[command].help).splitlines()
					if len(help) >= 2:
						answer = self.AnsBase[2] % (help.pop(0), help.pop(0))
						if help:
							answer += self.AnsBase[3]
							for line in help:
								line = line.strip()
								if line.startswith("*/"):
									Char, line = unichr(187)*3, line[2:].lstrip()
								else:
									Char = (chr(9) + chr(42))
								answer += "\n%s %s" % (Char, line)
					else:
						answer = self.AnsBase[17]
				else:
					answer = self.AnsBase[4]
			else:
				answer = AnsBase[6]
		else:
			answer = self.AnsBase[5]
		Answer(answer, ltype, source, disp)

	def command_commands(self, ltype, source, body, disp):
		answer = self.AnsBase[6] % (self.AnsBase[7] % (Chats[source[1]].cPref) if (Chats.has_key(source[1]) and Chats[source[1]].cPref) else ":")
		cmds, lcmds = {}, {}
		for x in xrange(1, 9):
			lcmds[x] = itypes.Number()
		for cmd in Cmds.keys():
			access = Cmds[cmd].access
			if not cmds.has_key(access):
				cmds[access] = []
			cmds[access].append(cmd)
			for x in lcmds.keys():
				if x >= access:
					lcmds[x].plus()
		for x in cmds.keys():
			cmds[x].sort()
		if cmds.has_key(8):
			answer += self.AnsBase[8] % (lcmds[8]._str(), ", ".join(cmds[8]))
		if cmds.has_key(7):
			answer += self.AnsBase[9] % (lcmds[7]._str(), ", ".join(cmds[7]))
		if cmds.has_key(6):
			answer += self.AnsBase[10] % (lcmds[6]._str(), ", ".join(cmds[6]))
		if cmds.has_key(5):
			answer += self.AnsBase[11] % (lcmds[5]._str(), ", ".join(cmds[5]))
		if cmds.has_key(4):
			answer += self.AnsBase[12] % (lcmds[4]._str(), ", ".join(cmds[4]))
		if cmds.has_key(3):
			answer += self.AnsBase[13] % (lcmds[3]._str(), ", ".join(cmds[3]))
		if cmds.has_key(2):
			answer += self.AnsBase[14] % (lcmds[2]._str(), ", ".join(cmds[2]))
		if cmds.has_key(1):
			answer += self.AnsBase[15] % (lcmds[1]._str(), ", ".join(cmds[1]))
		access = get_access(source[1], source[2])
		if access > 8:
			access = "%d (Gandalf)" % (access)
		elif access == 8:
			access = "8 (God)"
		elif access == 7:
			access = "7 (Chief)"
		else:
			access = str(access)
		answer += self.AnsBase[16] % (access)
		if ltype == Types[1]:
			Answer(AnsBase[11], ltype, source, disp)
		Message(source[0], answer, disp)

	commands = (
		(command_location, "location", 1,),
		(command_comacc, "comacc", 1,),
		(command_help, "help", 1, False),
		(command_commands, "commands", 1, False)
					)
