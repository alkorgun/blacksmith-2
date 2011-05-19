# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "session_stat" # /code.py v.x3
#  Id: 10~1a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_exc_info(ltype, source, body, disp):
	if body:
		if check_number(body):
			number = (int(body) - 1)
			if number in range(len(VarCache["errors"])):
				try:
					exc = VarCache["errors"][number]
					if oSlist[0]:
						exc = exc.decode("cp1251")
					exc = "%s" % (exc)
					if ltype == Types[1]:
						Answer(AnsBase[11], ltype, source, disp)
					Msend(source[0], exc, disp)
				except:
					answer = sess_answers[20]
			else:
				answer = sess_answers[21] % (body)
		else:
			answer = AnsBase[30]
	else:
		answer = sess_answers[22] % len(VarCache["errors"])
	if locals().has_key(Types[23]):
		Answer(answer, ltype, source, disp)

def command_botup(ltype, source, body, disp):
	Now_time = time.time()
	answer = sess_answers[15] % (timeElapsed(Now_time - Info["up"]))
	if Info["alls"]:
		answer += sess_answers[16] % (timeElapsed(Now_time - Info["sess"]), str(len(Info["alls"])), ", ".join(sorted(Info["alls"])))
	elif not oSlist[0]:
		answer += sess_answers[17]
	Answer(answer, ltype, source, disp)

def command_session(ltype, source, body, disp):
	Now_time = time.time()
	answer = sess_answers[0] % (BsPid)
	answer += sess_answers[1] % (timeElapsed(Now_time - Info["up"]))
	if len(Info["alls"]):
		answer += sess_answers[2] % (timeElapsed(Now_time - Info["sess"]))
	answer += sess_answers[3] % (Info["msg"]._str())
	answer += sess_answers[4] % (Info["cmd"]._str())
	answer += sess_answers[5] % (Info["prs"]._str(), Info["iq"]._str())
	answer += sess_answers[6] % (Info["omsg"]._str(), Info["outiq"]._str())
	answer += sess_answers[7] % (Info["fcr"]._str())
	answer += sess_answers[8] % (Info["fr"]._str())
	answer += sess_answers[9] % (Info["fw"]._str())
	answer += sess_answers[10] % (len(VarCache["errors"]), Info["errors"]._str())
	answer += sess_answers[11] % (Info["cfw"]._str())
	answer += sess_answers[12] % (iThr.Counter._str(), len(iThr.enumerate()))
	answer += sess_answers[13] % os.times()[0]
	number = calculate()
	if number:
		answer += sess_answers[14] % str(round(float(number) / 1024, 3))
	Answer(answer, ltype, source, disp)

def command_stat(ltype, source, body, disp):
	if body:
		x = body.lower()
		if x in Cmds.keys():
			answer = sess_answers[18] % (x, Cmds[x].numb._str(), len(Cmds[x].users))
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
		answer, col = sess_answers[19], itypes.Number()
		for x, y, z in list:
			answer += "\n%s. %s - %d (%d)" % (col.plus(), z, x, y)
			if col._int() >= 20:
				break
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_exc_info, command_botup, command_session, command_stat])
expansions[exp_name].ls.extend(["sess_answers"])

command_handler(command_exc_info, {"RU": "ошибка", "EN": "excinfo"}, 8, exp_name)
command_handler(command_botup, {"RU": "ботап", "EN": "botup"}, 1, exp_name)
command_handler(command_session, {"RU": "стат", "EN": "stat"}, 1, exp_name)
command_handler(command_stat, {"RU": "комстат", "EN": "comstat"}, 1, exp_name)
