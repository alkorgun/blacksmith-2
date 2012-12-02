# coding: utf-8

#  BlackSmith mark.2
# exp_name = "extra_control" # /code.py v.x9
#  Id: 01~7c
#  Code © (2009-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	sep = chr(38)*2

	def command_turbo(self, stype, source, body, disp):
		if body:
			if self.sep in body:
				ls = body.split(self.sep)
				lslen = len(ls) - 1
				if lslen < 4 or enough_access(source[1], source[2], 7):
					for numb, body in enumerate(ls):
						body = body.strip()
						body = body.split(None, 1)
						cmd = (body.pop(0)).lower()
						if Cmds.has_key(cmd):
							if body:
								body = body[0]
							else:
								body = ""
							Cmds[cmd].execute(stype, source, body, disp)
							if numb not in (0, lslen):
								sleep(2)
						else:
							answer = AnsBase[6]
				else:
					answer = AnsBase[10]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_remote(self, stype, source, body, disp):
		confs = sorted(Chats.keys())
		if body:
			body = body.split(None, 3)
			if len(body) >= 3:
				x = (body.pop(0)).lower()
				if x in confs:
					conf = x
				elif isNumber(x):
					Number = (int(x) - 1)
					if Number >= 0 and Number <= len(confs):
						conf = confs[Number]
					else:
						conf = None
				else:
					conf = None
				if conf:
					itype = (body.pop(0)).lower()
					if itype in ("chat", "чат".decode("utf-8")):
						type2 = Types[1]
					elif itype in ("private", "приват".decode("utf-8")):
						type2 = Types[0]
					else:
						type2 = None
					if type2:
						cmd = (body.pop(0)).lower()
						if body:
							body = body[0]
						else:
							body = ""
						if 2048 >= len(body):
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
									answer = AnsBase[19] % (inst.name)
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
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_private(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				body = body.split(None, 1)
				cmd = (body.pop(0)).lower()
				if Cmds.has_key(cmd):
					if body:
						body = body[0]
					else:
						body = ""
					Cmds[cmd].execute(Types[0], source, body, disp)
				else:
					answer = AnsBase[6]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	commands = (
		(command_turbo, "turbo", 1,),
		(command_remote, "remote", 8,),
		(command_private, "private", 1,)
					)
