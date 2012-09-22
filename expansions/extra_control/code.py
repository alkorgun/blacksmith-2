# coding: utf-8

#  BlackSmith mark.2
exp_name = "extra_control" # /code.py v.x7
#  Id: 01~5b
#  Code © (2009-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_remote(self, ltype, source, body, disp):
		confs = sorted(Chats.keys())
		if body:
			ls = body.split()
			if len(ls) >= 3:
				x = (ls.pop(0)).lower()
				if x in confs:
					conf = x
				elif isNumber(x):
					Number = (int(x) - 1)
					if Number >= 0 and Number <= len(confs):
						conf = confs[Number]
					else:
						conf = False
				else:
					conf = False
				if conf:
					itype = (ls.pop(0)).lower()
					if itype in (Types[14], Types[0]):
						type2 = Types[1]
					elif itype in (Types[15], Types[6]):
						type2 = Types[0]
					else:
						type2 = False
					if type2:
						cmd = (ls.pop(0)).lower()
						if ls:
							body = body[((body.lower()).find(cmd) + (len(cmd) + 1)):].strip()
						else:
							body = ""
						if 1024 >= len(body):
							if Cmds.has_key(cmd):
								inst = Cmds[cmd]
								if inst.isAvalable and inst.handler:
									Info["cmd"].plus()
									if type2 == Types[1]:
										disp_ = Chats[conf].disp
									else:
										disp_ = get_disp(disp)
									sThread("command", inst.handler, (inst.exp, type2, (source[0], conf, source[2]), body, disp_), inst.name)
									inst.numb.plus()
									source = get_source(source[1], source[2])
									if source and source not in inst.desc:
										inst.desc.append(source)
								else:
									Answer(AnsBase[19] % (inst.name), ltype, source, disp)
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_private(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				ls = body.split()
				cmd = (ls.pop(0)).lower()
				if Cmds.has_key(cmd):
					if ls:
						body = body[((body.lower()).find(cmd) + (len(cmd) + 1)):].strip()
					else:
						body = ""
					Cmds[cmd].execute(Types[0], source, body, disp)
				else:
					answer = AnsBase[6]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	commands = (
		(command_remote, "remote", 8,),
		(command_private, "private", 1,)
					)
