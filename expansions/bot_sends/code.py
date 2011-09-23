# coding: utf-8

#  BlackSmith mark.2
exp_name = "bot_sends" # /code.py v.x4
#  Id: 18~3a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_clear(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if ltype == Types[1]:
			s1_buckup = Chats[source[1]].state
			s2_buckup = Chats[source[1]].status
			Chats[source[1]].change_status(sList[2], BsendAnsBase[0])
		zero = xmpp.Message(to = source[1], typ = Types[1])
		for x in xrange(24):
			Sender(disp, zero); Info["omsg"].plus()
			time.sleep(1.4)
		if ltype == Types[1]:
			Chats[source[1]].change_status(s1_buckup, s2_buckup)
	else:
		Answer(AnsBase[0], ltype, source, disp)

def command_test(ltype, source, body, disp):
	errors = len(VarCache["errors"])
	if not errors:
		answer = BsendAnsBase[1]
	elif errors < (len(Clients.keys())*3):
		answer = BsendAnsBase[2] % (get_self_nick(source[1]), errors)
	else:
		answer = BsendAnsBase[3] % (errors)
	Answer(answer, ltype, source, disp)

def command_sendall(ltype, source, body, disp):
	if body:
		for conf in Chats.keys():
			Msend(conf, BsendAnsBase[5] % (source[2], body))
		answer = AnsBase[4]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_more(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if Chats[source[1]].more:
			body = "[&&] %s" % (Chats[source[1]].more)
			Chats[source[1]].more = ""
			Msend(source[1], body, disp)
	else:
		Answer(AnsBase[0], ltype, source, disp)

def command_send(ltype, source, body, disp):
	if body:
		list = body.split()
		if len(list) >= 2:
			sTo = list[0]
			if isSource(sTo):
				conf = (sTo.split(chr(47)))[0].lower()
				if Chats.has_key(conf) or not conf.count("@conf"):
					Msend(sTo, BsendAnsBase[5] % (source[2], body[(body.find(sTo) + (len(sTo) + 1)):].strip()))
					answer = AnsBase[4]
				else:
					answer = AnsBase[8]
			else:
				answer = BsendAnsBase[4]
		else:
			answer = AnsBase[2]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_adelivery(ltype, source, body, disp):
	if body:
		if PrivLimit >= len(body):
			instance = get_source(source[1], source[2])
			delivery(BsendAnsBase[5] % ((source[2] if not instance else "%s (%s)" % (source[2], instance)), body))
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

def command_invite(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			timer = (726 if enough_access(source[1], source[2], 7) else (time.time() - ChatsAttrs[source[1]]["intr"]))
			if timer >= 720:
				source_, jid_ = None, (body.split()[0])
				if Chats[source[1]].isHere(body):
					if Chats[source[1]].isHereNow(body):
						Answer(BsendAnsBase[6] % (body), ltype, source, disp)
						raise iThr.ThrKill("exit")
					source_ = get_source(source[1], body)
				elif isSource(jid_):
					source_ = jid_.lower()
				if source_:
					ChatsAttrs[source[1]]["intr"] = time.time()
					invite = xmpp.Message(to = source[1])
					x = xmpp.Node("x")
					x.setNamespace(xmpp.NS_MUC_USER)
					x_child = x.addChild("invite", {"to": source_})
					x_child.setTagData("reason", source[2])
					invite.addChild(node = x)
					Info["omsg"].plus()
					Sender(disp, invite)
					answer = AnsBase[4]
				else:
					answer = BsendAnsBase[7]
			else:
				answer = BsendAnsBase[8] % Time2Text(720 - timer)
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def init_invite_timer(conf):
	if not ChatsAttrs.has_key(conf):
		ChatsAttrs[conf] = {}
	ChatsAttrs[conf]["intr"] = 0

expansions[exp_name].funcs_add([command_clear, command_test, command_sendall, command_more, command_send, command_adelivery, command_say, command_invite, init_invite_timer])
expansions[exp_name].ls.extend(["BsendAnsBase"])

command_handler(command_clear, {"RU": "чисть", "EN": "clear"}, 3, exp_name)
command_handler(command_test, {"RU": "тест", "EN": "test"}, 1, exp_name, False)
command_handler(command_sendall, {"RU": "разослать", "EN": "sendall"}, 8, exp_name)
command_handler(command_more, {"RU": "далее", "EN": "more"}, 1, exp_name)
command_handler(command_send, {"RU": "сообщение", "EN": "send"}, 8, exp_name)
command_handler(command_adelivery, {"RU": "суперадмину", "EN": "toadmin"}, 1, exp_name)
command_handler(command_say, {"RU": "сказать", "EN": "say"}, 7, exp_name)
command_handler(command_invite, {"RU": "пригласить", "EN": "invite"}, 4, exp_name)

handler_register(init_invite_timer, "01si", exp_name)
