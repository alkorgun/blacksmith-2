# coding: utf-8

#  BlackSmith mark.2
exp_name = "get_iq" # /code.py v.x3
#  Id: 13~2a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_ping(ltype, source, instance, disp):
	if instance:
		source_ = instance
		if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
			if Chats[source[1]].isHereNow(instance):
				conf_nick = (source[1], instance)
				instance, source_ = "%s/%s" % conf_nick, get_source(*conf_nick)
			else:
				Answer(IqAnsBase[5] % (instance), ltype, source, disp)
				raise iThr.ThrKill("exit")
	else:
		instance, source_ = source[0], get_source(source[1], source[2])
	iq = xmpp.Iq(to = instance, typ = Types[10])
	iq.addChild(Types[16], {}, [], xmpp.NS_PING)
	iq.setID("Bs-i%d" % Info["outiq"].plus())
	CallForResponse(disp, iq, answer_ping, {"ltype": ltype, "source": source, "instance": instance, "source_": source_, "start": time.time()})

PingStat = {}

def answer_ping(disp, stanza, ltype, source, instance, source_, start):
	if xmpp.isResultNode(stanza):
		answer = round(time.time() - start, 3)
		if source_:
			if not PingStat.has_key(source_):
				PingStat[source_] = []
			PingStat[source_].append(answer)
		Answer(IqAnsBase[0] % str(answer), ltype, source, disp)
	else:
		iq = xmpp.Iq(to = instance, typ = Types[10])
		iq.addChild(Types[18], {}, [], xmpp.NS_VERSION)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, answer_ping_ver, {"ltype": ltype, "source": source, "instance": instance, "source_": source_, "start": time.time()})

def answer_ping_ver(disp, stanza, ltype, source, instance, source_, start):
	if xmpp.isResultNode(stanza):
		answer = round(time.time() - start, 3)
		if source_:
			if not PingStat.has_key(source_):
				PingStat[source_] = []
			PingStat[source_].append(answer)
		Name = "[None]"
		for x in stanza.getQueryChildren():
			xname = x.getName()
			if xname == "name":
				Name = x.getData()
		answer = IqAnsBase[1] % (Name, str(answer))
	else:
		answer = IqAnsBase[2]
	Answer(answer, ltype, source, disp)

def command_ping_stat(ltype, source, source_, disp):
	if source_:
		if Chats.has_key(source[1]) and Chats[source[1]].isHere(source_):
			source_ = get_source(source[1], source_)
		else:
			source_ = source_.lower()
	else:
		source_ = get_source(source[1], source[2])
	if source_ and PingStat.has_key(source_):
		number = 0
		for x in PingStat[source_]:
			number += x
		len_ = len(PingStat[source_])
		max_ = max(PingStat[source_])
		min_ = min(PingStat[source_])
		if len_:
			answer = IqAnsBase[3] % (str(len_), str(min_), str(max_), str(round(number / len_, 3)))
		else:
			answer = IqAnsBase[4]
	else:
		answer = IqAnsBase[4]
	Answer(answer, ltype, source, disp)

def command_version(ltype, source, instance, disp):
	if Chats.has_key(source[1]):
		if instance:
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereNow(instance):
					instance = "%s/%s" % (source[1], instance)
				else:
					Answer(IqAnsBase[5] % (instance), ltype, source, disp)
					raise iThr.ThrKill("exit")
		else:
			instance = source[0]
		iq = xmpp.Iq(to = instance, typ = Types[10])
		iq.addChild(Types[18], {}, [], xmpp.NS_VERSION)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, answer_version, {"ltype": ltype, "source": source})
	else:
		Answer(AnsBase[0], ltype, source, disp)

def answer_version(disp, stanza, ltype, source):
	if xmpp.isResultNode(stanza):
		Name, Ver, Os = "[None]", "[None]", "[None]"
		for x in stanza.getQueryChildren():
			xname = x.getName()
			if xname == "name":
				Name = x.getData()
			elif xname == "version":
				Ver = x.getData()
			elif xname == "os":
				Os = x.getData()
		answer = "\nName: %s\nVer.: %s\nOS: %s" % (Name, Ver, Os)
	else:
		answer = IqAnsBase[6]
	Answer(answer, ltype, source, disp)

def command_uptime(ltype, source, server, disp):
	if not server:
		server = InstansesDesc[Gen_disp][0]
	iq = xmpp.Iq(to = server, typ = Types[10])
	iq.addChild(Types[18], {}, [], xmpp.NS_LAST)
	iq.setID("Bs-i%d" % Info["outiq"].plus())
	CallForResponse(disp, iq, answer_idle, {"ltype": ltype, "source": source, "instance": server, "typ": 0})

def command_idle(ltype, source, instance, disp):
	if instance:
		nick = instance
		if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
			if Chats[source[1]].isHereNow(instance):
				instance = "%s/%s" % (source[1], instance)
			else:
				Answer(IqAnsBase[5] % (instance), ltype, source, disp)
				raise iThr.ThrKill("exit")
	else:
		instance, nick = source[0], source[2]
	iq = xmpp.Iq(to = instance, typ = Types[10])
	iq.addChild(Types[18], {}, [], xmpp.NS_LAST)
	iq.setID("Bs-i%d" % Info["outiq"].plus())
	CallForResponse(disp, iq, answer_idle, {"ltype": ltype, "source": source, "instance": nick, "typ": 1})

def answer_idle(disp, stanza, ltype, source, instance, typ):
	if xmpp.isResultNode(stanza):
		seconds = stanza.getTagAttr(Types[18], "seconds")
		if seconds and seconds != "0" and isNumber(seconds):
			answer = (IqAnsBase[8] if typ else IqAnsBase[7]) % (instance, Time2Text(int(seconds)))
	if not locals().has_key(Types[12]):
		answer = IqAnsBase[6]
	Answer(answer, ltype, source, disp)

def command_afls(ltype, source, body, disp):

	def get_req(body):
		afls = ["owner", "admin", "member", "outcast"]
		if DefLANG in ["RU", "UA"]:
			alsRU = [x.decode("utf-8") for x in ["овнер", "админ", "мембер", "бан"]]
			for x in alsRU:
				if body.count(x):
					return afls[alsRU.index(x)]
		return (body if afls.count(body) else None)

	if Chats.has_key(source[1]):
		if body:
			list = body.split()
			body = get_req((list.pop(0)).lower())
			if body:
				Numb = 0
				if list:
					if isNumber(list[0]):
						x = int(list.pop(0))
						if x < 20:
							Numb = 20
						else:
							Numb = x
				iq = xmpp.Iq(to = source[1], typ = Types[10])
				query = xmpp.Node(Types[18])
				query.setNamespace(xmpp.NS_MUC_ADMIN)
				query.addChild("item", {AflRoles[0]: body})
				iq.addChild(node = query)
				iq.setID("Bs-i%d" % Info["outiq"].plus())
				CallForResponse(disp, iq, answer_afls, {"ltype": ltype, "source": source, "Numb": Numb})
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def answer_afls(disp, stanza, ltype, source, Numb):
	if xmpp.isResultNode(stanza):
		list = stanza.getChildren()
		if list:
			answer, Number = "", itypes.Number()
			for child in list[0].getChildren():
				if child and child != "None":
					jid = child.getAttr("jid")
					if jid:
						if Numb and Numb <= Number._int():
							Number.plus()
						else:
							answer += "\n%d) %s" % (Number.plus(), jid)
							signature = child.getTagData("reason")
							if signature:
								answer += " [%s]" % (signature)
			if answer:
				if Numb and Numb < Number._int():
					answer += "\n...\nTotal: %s items." % (Number._str())
				Msend(source[0], answer, disp)
				if ltype == Types[1]:
					answer = AnsBase[11]
				else:
					del answer
			else:
				answer = IqAnsBase[6]
		else:
			answer = IqAnsBase[6]
	else:
		answer = IqAnsBase[6]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_ping, answer_ping, answer_ping_ver, command_ping_stat, command_version, answer_version, command_uptime, command_idle, answer_idle, command_afls, answer_afls])
expansions[exp_name].ls.extend(["IqAnsBase, PingStat"])

command_handler(command_ping, {"RU": "пинг", "EN": "ping"}, 1, exp_name)
command_handler(command_ping_stat, {"RU": "пингстат", "EN": "pingstat"}, 1, exp_name)
command_handler(command_version, {"RU": "версия", "EN": "version"}, 1, exp_name)
command_handler(command_uptime, {"RU": "аптайм", "EN": "uptime"}, 1, exp_name)
command_handler(command_idle, {"RU": "жив", "EN": "idle"}, 1, exp_name)
command_handler(command_afls, {"RU": "список", "EN": "list"}, 4, exp_name)
