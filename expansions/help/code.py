# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "help" # /code.py v.x4
#  Id: 03~1a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_location(ltype, source, body, disp):
	if body:
		command = body.lower()
		if Cmds.has_key(command):
			answer = help_answers[0] % (command, Cmds[command].exp.upper())
		else:
			answer = AnsBase[6]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_comacc(ltype, source, body, disp):
	if body:
		command = body.lower()
		if Cmds.has_key(command):
			answer = help_answers[1] % (command, Cmds[command].access)
		else:
			answer = AnsBase[6]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_help(ltype, source, body, disp):
	if body:
		command = body.lower()
		if Cmds.has_key(command):
			if os.path.isfile(Cmds[command].help):
				help = get_file(Cmds[command].help).splitlines()
				if len(help) >= 2:
					answer = help_answers[2] % (help.pop(0), help.pop(0))
					if help:
						answer += help_answers[3]
						for line in help:
							if line.count("*/"):
								answer += "\n»»» %s" % line.replace("*/", "")
							else:
								answer += "\n\t* %s" % (line)
				else:
					answer = help_answers[17]
			else:
				answer = help_answers[4]
		else:
			answer = AnsBase[6]
	else:
		answer = help_answers[5]
	Answer(answer, ltype, source, disp)

def command_commands(ltype, source, body, disp):
	answer = help_answers[6] % (help_answers[7] % (Chats[source[1]].cPref) if (Chats.has_key(source[1]) and Chats[source[1]].cPref) else ":")
	cmds, lcmds = {}, {}
	for x in range(1, 9):
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
		answer += help_answers[8] % (lcmds[8]._str(), ", ".join(cmds[8]))
	if cmds.has_key(7):
		answer += help_answers[9] % (lcmds[7]._str(), ", ".join(cmds[7]))
	if cmds.has_key(6):
		answer += help_answers[10] % (lcmds[6]._str(), ", ".join(cmds[6]))
	if cmds.has_key(5):
		answer += help_answers[11] % (lcmds[5]._str(), ", ".join(cmds[5]))
	if cmds.has_key(4):
		answer += help_answers[12] % (lcmds[4]._str(), ", ".join(cmds[4]))
	if cmds.has_key(3):
		answer += help_answers[13] % (lcmds[3]._str(), ", ".join(cmds[3]))
	if cmds.has_key(2):
		answer += help_answers[14] % (lcmds[2]._str(), ", ".join(cmds[2]))
	if cmds.has_key(1):
		answer += help_answers[15] % (lcmds[1]._str(), ", ".join(cmds[1]))
	access = get_access(source[1], source[2])
	if access >= 8:
		access = "%d (BOSS)" % (access)
	elif access == 7:
		access = "7 (Chief)"
	else:
		access = str(access)
	answer += help_answers[16] % (access)
	if ltype == Types[1]:
		Answer(AnsBase[11], ltype, source, disp)
	Msend(source[0], answer, disp)

expansions[exp_name].funcs_add([command_location, command_comacc, command_help, command_commands])
expansions[exp_name].ls.extend(["help_answers"])

command_handler(command_location, {"RU": "дислокация", "EN": "location"}, 1, exp_name)
command_handler(command_comacc, {"RU": "комдоступ", "EN": "comacc"}, 1, exp_name)
command_handler(command_help, {"RU": "хелп", "EN": "help"}, 1, exp_name, False)
command_handler(command_commands, {"RU": "комлист", "EN": "commands"}, 1, exp_name, False)
