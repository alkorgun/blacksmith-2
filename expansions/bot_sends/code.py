# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "bot_sends" # /code.py v.x2
#  Id: 18~1a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_clear(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if ltype == Types[1]:
			s1_buckup = Chats[source[1]].state
			s2_buckup = Chats[source[1]].status
			Chats[source[1]].change_status(sList[2], bsends_answers[0])
		zero = xmpp.Message(to = source[1], typ = Types[1])
		for x in range(24):
			Sender(disp, zero); Info["omsg"].plus()
			time.sleep(1.4)
		if ltype == Types[1]:
			Chats[source[1]].change_status(s1_buckup, s2_buckup)
	else:
		Answer(AnsBase[0], ltype, source, disp)

def command_test(ltype, source, body, disp):
	errors = len(VarCache["errors"])
	if not errors:
		answer = bsends_answers[1]
	elif errors < (len(Clients.keys())*3):
		answer = bsends_answers[2] % (get_self_nick(source[1]), errors)
	else:
		answer = bsends_answers[3] % (errors)
	Answer(answer, ltype, source, disp)

def command_sendall(ltype, source, body, disp):
	if body:
		for conf in Chats.keys():
			Msend(conf, bsends_answers[5] % (source[2], body))
		answer = AnsBase[4]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_send(ltype, source, body, disp):
	if body:
		list = body.split()
		if len(list) >= 2:
			sTo = list[0]
			if sTo.count("@") and sTo.count("."):
				conf = sTo.split("/")[0].lower()
				if Chats.has_key(conf) or not conf.count("@conf"):
					Msend(sTo, bsends_answers[5] % (source[2], body[(body.find(" ") + 1):].strip()))
					answer = AnsBase[4]
				else:
					answer = AnsBase[8]
			else:
				answer = bsends_answers[4]
		else:
			answer = AnsBase[2]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_adelivery(ltype, source, body, disp):
	if body:
		if PrivLimit >= len(body):
			instance = get_source(source[1], source[2])
			delivery(bsends_answers[5] % ((source[2] if not instance else "%s (%s)" % (source[2], instance)), body))
			answer = AnsBase[4]
		else:
			answer = AnsBase[5]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_say(ltype, source, body, disp):
	if body:
		if ConfLimit >= len(body):
			Msend(source[1], body, disp)
		else:
			Msend(source[1], body[:ConfLimit], disp)
	else:
		Answer(AnsBase[1], ltype, source, disp)

expansions[exp_name].funcs_add([command_clear, command_test, command_sendall, command_send, command_adelivery, command_say])
expansions[exp_name].ls.extend(["bsends_answers"])

command_handler(command_clear, {"RU": "чисть", "EN": "clear"}, 3, exp_name)
command_handler(command_test, {"RU": "тест", "EN": "test"}, 1, exp_name, False)
command_handler(command_sendall, {"RU": "разослать", "EN": "sendall"}, 8, exp_name)
command_handler(command_send, {"RU": "сообщение", "EN": "send"}, 8, exp_name)
command_handler(command_adelivery, {"RU": "суперадмину", "EN": "toadmin"}, 1, exp_name)
command_handler(command_say, {"RU": "сказать", "EN": "say"}, 7, exp_name)
