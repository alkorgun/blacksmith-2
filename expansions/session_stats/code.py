# coding: utf-8

#  BlackSmith mark.2
# exp_name = "session_stats" # /code.py v.x6
#  Id: 10~4c
#  Code © (2010-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_exc_info(self, stype, source, body, disp):
		if body:
			if isNumber(body):
				Number = (int(body) - 1)
				if Number in xrange(len(VarCache["errors"])):
					try:
						exc = VarCache["errors"][Number]
						if oSlist[0]:
							exc = exc.decode("cp1251")
						exc = str(exc)
						if stype == Types[1]:
							Answer(AnsBase[11], stype, source, disp)
						Message(source[0], exc, disp)
					except:
						answer = self.AnsBase[20]
				else:
					answer = self.AnsBase[21] % (body)
			else:
				answer = AnsBase[30]
		else:
			answer = self.AnsBase[22] % len(VarCache["errors"])
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_botup(self, stype, source, body, disp):
		NowTime = time.time()
		answer = self.AnsBase[15] % (Time2Text(NowTime - Info["up"]))
		if Info["alls"]:
			answer += self.AnsBase[16] % (Time2Text(NowTime - Info["sess"]), str(len(Info["alls"])), ", ".join(sorted(Info["alls"])))
		elif not oSlist[0]:
			answer += self.AnsBase[17]
		Answer(answer, stype, source, disp)

	def command_session(self, stype, source, body, disp):
		NowTime = time.time()
		answer = self.AnsBase[0] % (BsPid)
		answer += self.AnsBase[1] % (Time2Text(NowTime - Info["up"]))
		if len(Info["alls"]):
			answer += self.AnsBase[2] % (Time2Text(NowTime - Info["sess"]))
		answer += self.AnsBase[7] % len(Chats.keys())
		answer += self.AnsBase[3] % (Info["msg"]._str())
		answer += self.AnsBase[4] % (Info["cmd"]._str())
		answer += self.AnsBase[5] % (Info["prs"]._str(), Info["iq"]._str())
		answer += self.AnsBase[6] % (Info["omsg"]._str(), Info["outiq"]._str())
		Number = itypes.Number()
		for conf in Chats.itervalues():
			Number.plus(len(conf.get_nicks()))
		answer += self.AnsBase[8] % (int(Number))
		answer += self.AnsBase[10] % (len(VarCache["errors"]), Info["errors"]._str())
		answer += self.AnsBase[11] % (Info["cfw"]._str())
		answer += self.AnsBase[12] % (iThr.Counter._str(), len(iThr.enumerate()))
		answer += self.AnsBase[13] % os.times()[0]
		Number = calculate()
		if Number:
			answer += self.AnsBase[14] % str(round(float(Number) / 1024, 3))
		Answer(answer, stype, source, disp)

	def command_stats(self, stype, source, body, disp):
		if body:
			cmd = body.lower()
			if Cmds.has_key(cmd):
				answer = self.AnsBase[18] % (cmd, Cmds[cmd].numb._str(), len(Cmds[cmd].desc))
			else:
				answer = AnsBase[6]
		else:
			ls = []
			for cmd in Cmds.values():
				used = cmd.numb._int()
				if used:
					ls.append((used, len(cmd.desc), cmd.name))
			answer = self.AnsBase[19] + str.join(chr(10), ["%s. %s - %d (%d)" % (numb, name, used, desc) for numb, (used, desc, name) in enumerate(sorted(ls, reverse = True), 1)])
		Answer(answer, stype, source, disp)

	commands = (
		(command_exc_info, "excinfo", 8,),
		(command_botup, "botup", 1,),
		(command_session, "stat", 1,),
		(command_stats, "comstat", 1,)
					)
