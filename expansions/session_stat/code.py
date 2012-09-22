# coding: utf-8

#  BlackSmith mark.2
exp_name = "session_stat" # /code.py v.x5
#  Id: 10~3b
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_exc_info(self, ltype, source, body, disp):
		if body:
			if isNumber(body):
				Number = (int(body) - 1)
				if Number in xrange(len(VarCache["errors"])):
					try:
						exc = VarCache["errors"][Number]
						if oSlist[0]:
							exc = exc.decode("cp1251")
						exc = "%s" % (exc)
						if ltype == Types[1]:
							Answer(AnsBase[11], ltype, source, disp)
						Msend(source[0], exc, disp)
					except:
						answer = self.SstatAnsBase[20]
				else:
					answer = self.SstatAnsBase[21] % (body)
			else:
				answer = AnsBase[30]
		else:
			answer = self.SstatAnsBase[22] % len(VarCache["errors"])
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_botup(self, ltype, source, body, disp):
		NowTime = time.time()
		answer = self.SstatAnsBase[15] % (Time2Text(NowTime - Info["up"]))
		if Info["alls"]:
			answer += self.SstatAnsBase[16] % (Time2Text(NowTime - Info["sess"]), str(len(Info["alls"])), ", ".join(sorted(Info["alls"])))
		elif not oSlist[0]:
			answer += self.SstatAnsBase[17]
		Answer(answer, ltype, source, disp)

	def command_session(self, ltype, source, body, disp):
		NowTime = time.time()
		answer = self.SstatAnsBase[0] % (BsPid)
		answer += self.SstatAnsBase[1] % (Time2Text(NowTime - Info["up"]))
		if len(Info["alls"]):
			answer += self.SstatAnsBase[2] % (Time2Text(NowTime - Info["sess"]))
		answer += self.SstatAnsBase[7] % len(Chats.keys())
		answer += self.SstatAnsBase[3] % (Info["msg"]._str())
		answer += self.SstatAnsBase[4] % (Info["cmd"]._str())
		answer += self.SstatAnsBase[5] % (Info["prs"]._str(), Info["iq"]._str())
		answer += self.SstatAnsBase[6] % (Info["omsg"]._str(), Info["outiq"]._str())
		Number = itypes.Number()
		for conf in Chats.keys():
			Number.plus(len(Chats[conf].get_nicks()))
		answer += self.SstatAnsBase[8] % (int(Number))
		answer += self.SstatAnsBase[10] % (len(VarCache["errors"]), Info["errors"]._str())
		answer += self.SstatAnsBase[11] % (Info["cfw"]._str())
		answer += self.SstatAnsBase[12] % (iThr.Counter._str(), len(iThr.enumerate()))
		answer += self.SstatAnsBase[13] % os.times()[0]
		Number = calculate()
		if Number:
			answer += self.SstatAnsBase[14] % str(round(float(Number) / 1024, 3))
		Answer(answer, ltype, source, disp)

	def command_stat(self, ltype, source, body, disp):
		if body:
			x = body.lower()
			if x in Cmds.keys():
				answer = self.SstatAnsBase[18] % (x, Cmds[x].numb._str(), len(Cmds[x].desc))
			else:
				answer = AnsBase[6]
		else:
			list = []
			for x in Cmds.values():
				x_len = x.numb._int()
				if x_len:
					list.append((x_len, len(x.desc), x.name))
			list.sort()
			list.reverse()
			answer, Numb = self.SstatAnsBase[19], itypes.Number()
			for x, y, z in list:
				answer += "\n%s. %s - %d (%d)" % (Numb.plus(), z, x, y)
				if Numb._int() >= 20:
					break
		Answer(answer, ltype, source, disp)

	commands = (
		(command_exc_info, "excinfo", 8,),
		(command_botup, "botup", 1,),
		(command_session, "stat", 1,),
		(command_stat, "comstat", 1,)
					)
