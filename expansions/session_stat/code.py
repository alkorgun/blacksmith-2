# coding: utf-8

#  BlackSmith mark.2
exp_name = "session_stat" # /code.py v.x3
#  Id: 10~1a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_exc_info(ltype, source, body, disp):
	if body:
		if isNumber(body):
			number = (int(body) - 1)
			if number in xrange(len(VarCache["errors"])):
				try:
					exc = VarCache["errors"][number]
					if oSlist[0]:
						exc = exc.decode("cp1251")
					exc = "%s" % (exc)
					if ltype == Types[1]:
						Answer(AnsBase[11], ltype, source, disp)
					Msend(source[0], exc, disp)
				except:
					answer = SstatAnsBase[20]
			else:
				answer = SstatAnsBase[21] % (body)
		else:
			answer = AnsBase[30]
	else:
		answer = SstatAnsBase[22] % len(VarCache["errors"])
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_botup(ltype, source, body, disp):
	NowTime = time.time()
	answer = SstatAnsBase[15] % (Time2Text(NowTime - Info["up"]))
	if Info["alls"]:
		answer += SstatAnsBase[16] % (Time2Text(NowTime - Info["sess"]), str(len(Info["alls"])), ", ".join(sorted(Info["alls"])))
	elif not oSlist[0]:
		answer += SstatAnsBase[17]
	Answer(answer, ltype, source, disp)

def command_session(ltype, source, body, disp):
	NowTime = time.time()
	answer = SstatAnsBase[0] % (BsPid)
	answer += SstatAnsBase[1] % (Time2Text(NowTime - Info["up"]))
	if len(Info["alls"]):
		answer += SstatAnsBase[2] % (Time2Text(NowTime - Info["sess"]))
	answer += SstatAnsBase[3] % (Info["msg"]._str())
	answer += SstatAnsBase[4] % (Info["cmd"]._str())
	answer += SstatAnsBase[5] % (Info["prs"]._str(), Info["iq"]._str())
	answer += SstatAnsBase[6] % (Info["omsg"]._str(), Info["outiq"]._str())
	answer += SstatAnsBase[7] % (Info["fcr"]._str())
	answer += SstatAnsBase[8] % (Info["fr"]._str())
	answer += SstatAnsBase[9] % (Info["fw"]._str())
	answer += SstatAnsBase[10] % (len(VarCache["errors"]), Info["errors"]._str())
	answer += SstatAnsBase[11] % (Info["cfw"]._str())
	answer += SstatAnsBase[12] % (iThr.Counter._str(), len(iThr.enumerate()))
	answer += SstatAnsBase[13] % os.times()[0]
	number = calculate()
	if number:
		answer += SstatAnsBase[14] % str(round(float(number) / 1024, 3))
	Answer(answer, ltype, source, disp)

def command_stat(ltype, source, body, disp):
	if body:
		x = body.lower()
		if x in Cmds.keys():
			answer = SstatAnsBase[18] % (x, Cmds[x].numb._str(), len(Cmds[x].users))
		else:
			answer = AnsBase[6]
	else:
		list = []
		for x in Cmds.values():
			x_len = x.numb._int()
			if x_len:
				list.append((x_len, len(x.users), x.name))
		list.sort()
		list.reverse()
		answer, Numb = SstatAnsBase[19], itypes.Number()
		for x, y, z in list:
			answer += "\n%s. %s - %d (%d)" % (Numb.plus(), z, x, y)
			if Numb._int() >= 20:
				break
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_exc_info, command_botup, command_session, command_stat])
expansions[exp_name].ls.extend(["SstatAnsBase"])

command_handler(command_exc_info, {"RU": "ошибка", "EN": "excinfo"}, 8, exp_name)
command_handler(command_botup, {"RU": "ботап", "EN": "botup"}, 1, exp_name)
command_handler(command_session, {"RU": "стат", "EN": "stat"}, 1, exp_name)
command_handler(command_stat, {"RU": "комстат", "EN": "comstat"}, 1, exp_name)
