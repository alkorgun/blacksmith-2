# coding: utf-8

#  BlackSmith mark.2
# exp_name = "extra_control" # /code.py v.x12
#  Id: 01~10c
#  Code © (2009-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	sep = chr(38)*2

	def command_turbo(self, stype, source, body, disp):
		if body:
			if self.sep in body:
				ls = [body.strip() for body in body.split(self.sep)]
				if all(ls):
					lslen = len(ls) - 1
					if lslen < 4 or enough_access(source[1], source[2], 7):
						for numb, body in enumerate(ls):
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
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		if locals().has_key(sBase[6]):
			Answer(answer, stype, source, disp)

	def command_remote(self, stype, source, body, disp):
		confs = sorted(Chats.keys())
		if body:
			body = body.split(None, 3)
			if len(body) >= 3:
				arg0 = (body.pop(0)).lower()
				if arg0 in confs:
					conf = arg0
				elif isNumber(arg0):
					Number = (int(arg0) - 1)
					if -1 < Number < len(confs):
						conf = confs[Number]
					else:
						conf = None
				else:
					conf = None
				if conf:
					st = (body.pop(0)).lower()
					if st in ("chat", "чат".decode("utf-8")):
						stype_ = sBase[1]
					elif st in ("private", "приват".decode("utf-8")):
						stype_ = sBase[0]
					else:
						stype_ = None
					if stype_:
						cmd = (body.pop(0)).lower()
						if body:
							body = body[0]
						else:
							body = ""
						if 2048 >= len(body):
							if Cmds.has_key(cmd):
								cmd = Cmds[cmd]
								if cmd.isAvalable and cmd.handler:
									if stype_ == sBase[1]:
										disp_ = Chats[conf].disp
									else:
										disp_ = get_disp(disp)
									Info["cmd"].plus()
									sThread("command", cmd.handler, (cmd.exp, stype_, (source[0], conf, source[2]), body, disp_), cmd.name)
									cmd.numb.plus()
									source = get_source(source[1], source[2])
									if source:
										cmd.desc.add(source)
								else:
									answer = AnsBase[19] % (cmd.name)
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
		if locals().has_key(sBase[6]):
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
					Cmds[cmd].execute(sBase[0], source, body, disp)
				else:
					answer = AnsBase[6]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(sBase[6]):
			Answer(answer, stype, source, disp)

	pointer = chr(62)*2

	def command_redirect(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if body.count(self.pointer) == True:
					body = body.split(None, 1)
					cmd = (body.pop(0)).lower()
					if Cmds.has_key(cmd):
						cmd = Cmds[cmd]
						if enough_access(source[1], source[2], cmd.access):
							if cmd.isAvalable and cmd.handler:
								if body:
									body = body[0].rsplit(self.pointer, 1)
									if len(body) == 2:
										body, nick = body
										nick = nick.strip()
										body = body.strip()
									else:
										nick = body[0].strip()
										body = ""
									if Chats[source[1]].isHereTS(nick):
										Info["cmd"].plus()
										sThread("command", cmd.handler, (cmd.exp, sBase[0], ("%s/%s" % (source[1], nick), source[1], nick), body, disp), cmd.name)
										cmd.numb.plus()
										source_ = get_source(source[1], source[2])
										if source_:
											cmd.desc.add(source_)
										answer = AnsBase[4]
									else:
										answer = AnsBase[7]
								else:
									answer = AnsBase[2]
							else:
								answer = AnsBase[19] % (cmd.name)
						else:
							answer = AnsBase[10]
					else:
						answer = AnsBase[6]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	commands = (
		(command_turbo, "turbo", 1,),
		(command_remote, "remote", 8,),
		(command_private, "private", 1,),
		(command_redirect, "redirect", 5,)
	)
