# coding: utf-8

#  BlackSmith mark.2
# exp_name = "help" # /code.py v.x7
#  Id: 03~4c
#  Code © (2010-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_location(self, stype, source, body, disp):
		if body:
			command = body.lower()
			if Cmds.has_key(command):
				answer = self.AnsBase[0] % (command, Cmds[command].exp.name.upper())
			else:
				answer = AnsBase[6]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_comacc(self, stype, source, body, disp):
		if body:
			command = body.lower()
			if Cmds.has_key(command):
				answer = self.AnsBase[1] % (command, Cmds[command].access)
			else:
				answer = AnsBase[6]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	mark = "{command}"

	def command_help(self, stype, source, body, disp):
		if body:
			body = body.split(None, 1)
			command = (body.pop(0)).lower()
			if Cmds.has_key(command):
				if body:
					lang = (body.pop(0)).lower()
					if len(lang) == 2 and all([(char in CharCase[1]) for char in lang]):
						help = os.path.join(ExpsDir, Cmds[command].exp.name, "%s.%s" % (Cmds[command].default, lang))
					else:
						help = None
				else:
					help = Cmds[command].help
				if help and os.path.isfile(help):
					help = get_file(help)
					if self.mark in help:
						help = help.format(command = command)
						help = help.splitlines()
						if len(help) >= 2:
							ls = [self.AnsBase[2] % (help.pop(0), help.pop(0))]
							if help:
								ls.append(self.AnsBase[3])
								for line in help:
									line = line.strip()
									if line.startswith("*/"):
										Char, line = unichr(187)*3, line[2:].lstrip()
									else:
										Char = (chr(9) + chr(42))
									ls.append("%s %s" % (Char, line))
							answer = str.join(chr(10), ls)
						else:
							answer = self.AnsBase[17]
					else:
						answer = self.AnsBase[17]
				else:
					answer = self.AnsBase[4]
			else:
				answer = AnsBase[6]
		else:
			answer = self.AnsBase[5]
		Answer(answer, stype, source, disp)

	def command_commands(self, stype, source, body, disp):
		answer = self.AnsBase[6] % (self.AnsBase[7] % (Chats[source[1]].cPref) if (Chats.has_key(source[1]) and Chats[source[1]].cPref) else ":")
		cmds, lcmds = {}, {}
		for x in xrange(1, 9):
			lcmds[x] = itypes.Number()
		for cmd in Cmds.keys():
			access = Cmds[cmd].access
			cmds.setdefault(access, []).append(cmd)
			for x in lcmds.keys():
				if x >= access:
					lcmds[x].plus()
		for ls in cmds.itervalues():
			ls.sort()
		if cmds.has_key(8):
			answer += self.AnsBase[8] % (lcmds[8], ", ".join(cmds[8]))
		if cmds.has_key(7):
			answer += self.AnsBase[9] % (lcmds[7], ", ".join(cmds[7]))
		if cmds.has_key(6):
			answer += self.AnsBase[10] % (lcmds[6], ", ".join(cmds[6]))
		if cmds.has_key(5):
			answer += self.AnsBase[11] % (lcmds[5], ", ".join(cmds[5]))
		if cmds.has_key(4):
			answer += self.AnsBase[12] % (lcmds[4], ", ".join(cmds[4]))
		if cmds.has_key(3):
			answer += self.AnsBase[13] % (lcmds[3], ", ".join(cmds[3]))
		if cmds.has_key(2):
			answer += self.AnsBase[14] % (lcmds[2], ", ".join(cmds[2]))
		if cmds.has_key(1):
			answer += self.AnsBase[15] % (lcmds[1], ", ".join(cmds[1]))
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
		if stype == sBase[1]:
			Answer(AnsBase[11], stype, source, disp)
		Message(source[0], answer, disp)

	commands = (
		(command_location, "location", 1,),
		(command_comacc, "comacc", 1,),
		(command_help, "help", 1, False),
		(command_commands, "commands", 1, False)
	)
