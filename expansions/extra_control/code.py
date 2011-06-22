# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "extra_control" # /code.py v.x5
#  Id: 01~3a
#  Code © (2009-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_remote(ltype, source, body, disp):
	confs = sorted(Chats.keys())
	if body:
		list = body.split()
		if len(list) >= 3:
			x = list[0].lower()
			if x in confs:
				conf = x
			elif check_number(x):
				number = (int(x) - 1)
				if number >= 0 and number <= len(confs):
					conf = confs[number]
				else:
					conf = False
			else:
				conf = False
			if conf:
				itype = list[1].lower()
				if itype in [Types[14], Types[0]]:
					type2 = Types[1]
				elif itype in [Types[15], Types[6]]:
					type2 = Types[0]
				else:
					type2 = False
				if type2:
					command = list[2].lower()
					if len(list) >= 4:
						Parameters = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
					else:
						Parameters = ""
					if len(Parameters) <= 1024:
						if Cmds.has_key(command):
							self = Cmds[command]
							if self.isAvalable and self.handler:
								Info["cmd"].plus()
								if type2 == Types[1]:
									disp_ = Chats[conf].disp
								else:
									disp_ = get_disp(disp)
								sThread("command", self.handler, (type2, (source[0], conf, source[2]), Parameters, disp_), self.name)
								self.numb.plus()
								source = get_source(source[1], source[2])
								if source and source not in self.users:
									self.users.append(source)
							else:
								Answer(AnsBase[19] % (self.name), ltype, source, disp)
						else:
							answer = AnsBase[6]
					else:
						answer = AnsBase[5]
				else:
					answer = AnsBase[9]
			else:
				answer = AnsBase[8]
		else:
			answer = AnsBase[2]
	else:
		answer = enumerated_list(confs)
	if locals().has_key(Types[23]):
		Answer(answer, ltype, source, disp)

def command_private(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			list = body.split()
			command = (list.pop(0)).lower()
			if Cmds.has_key(command):
				if list:
					Parameters = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
				else:
					Parameters = ""
				Cmds[command].execute(Types[0], source, Parameters, disp)
			else:
				answer = AnsBase[6]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[23]):
		Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_remote, command_private])

command_handler(command_remote, {"RU": "ремоут", "EN": "remote"}, 8, exp_name)
command_handler(command_private, {"RU": "приват", "EN": "private"}, 1, exp_name)
