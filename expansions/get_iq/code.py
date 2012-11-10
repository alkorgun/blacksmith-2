# coding: utf-8

#  BlackSmith mark.2
exp_name = "get_iq" # /code.py v.x4
#  Id: 13~3b
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_ping(self, ltype, source, instance, disp):
		if instance:
			source_ = instance
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereTS(instance):
					conf_nick = (source[1], instance)
					instance, source_ = "%s/%s" % conf_nick, get_source(*conf_nick)
				else:
					Answer(self.AnsBase[5] % (instance), ltype, source, disp)
					raise iThr.ThrKill("exit")
		else:
			instance, source_ = source[0], get_source(source[1], source[2])
		iq = xmpp.Iq(to = instance, typ = Types[10])
		iq.addChild(Types[16], {}, [], xmpp.NS_PING)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_ping, {"ltype": ltype, "source": source, "instance": instance, "source_": source_, "start": time.time()})

	PingStat = {}

	def answer_ping(self, disp, stanza, ltype, source, instance, source_, start):
		if xmpp.isResultNode(stanza):
			answer = round(time.time() - start, 3)
			if source_:
				if not self.PingStat.has_key(source_):
					self.PingStat[source_] = []
				self.PingStat[source_].append(answer)
			Answer(self.AnsBase[0] % str(answer), ltype, source, disp)
		else:
			iq = xmpp.Iq(to = instance, typ = Types[10])
			iq.addChild(Types[18], {}, [], xmpp.NS_VERSION)
			iq.setID("Bs-i%d" % Info["outiq"].plus())
			CallForResponse(disp, iq, self.answer_ping_ver, {"ltype": ltype, "source": source, "instance": instance, "source_": source_, "start": time.time()})

	def answer_ping_ver(self, disp, stanza, ltype, source, instance, source_, start):
		if xmpp.isResultNode(stanza):
			answer = round(time.time() - start, 3)
			if source_:
				if not self.PingStat.has_key(source_):
					self.PingStat[source_] = []
				self.PingStat[source_].append(answer)
			Name = "[None]"
			for x in stanza.getQueryChildren():
				xname = x.getName()
				if xname == "name":
					Name = x.getData()
			answer = self.AnsBase[1] % (Name, str(answer))
		else:
			answer = self.AnsBase[2]
		Answer(answer, ltype, source, disp)

	def command_ping_stat(self, ltype, source, source_, disp):
		if source_:
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(source_):
				source_ = get_source(source[1], source_)
			else:
				source_ = source_.lower()
		else:
			source_ = get_source(source[1], source[2])
		if source_ and self.PingStat.has_key(source_):
			Number = float(sum(self.PingStat[source_]))
			len_ = len(self.PingStat[source_])
			max_ = max(self.PingStat[source_])
			min_ = min(self.PingStat[source_])
			if len_:
				answer = self.AnsBase[3] % (str(len_), str(min_), str(max_), str(round(Number / len_, 3)))
			else:
				answer = self.AnsBase[4]
		else:
			answer = self.AnsBase[4]
		Answer(answer, ltype, source, disp)

	def command_version(self, ltype, source, instance, disp):
		if Chats.has_key(source[1]):
			if instance:
				if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
					if Chats[source[1]].isHereTS(instance):
						instance = "%s/%s" % (source[1], instance)
					else:
						Answer(self.AnsBase[5] % (instance), ltype, source, disp)
						raise iThr.ThrKill("exit")
			else:
				instance = source[0]
			iq = xmpp.Iq(to = instance, typ = Types[10])
			iq.addChild(Types[18], {}, [], xmpp.NS_VERSION)
			iq.setID("Bs-i%d" % Info["outiq"].plus())
			CallForResponse(disp, iq, self.answer_version, {"ltype": ltype, "source": source})
		else:
			Answer(AnsBase[0], ltype, source, disp)

	def answer_version(self, disp, stanza, ltype, source):
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
			answer = self.AnsBase[6]
		Answer(answer, ltype, source, disp)

	def command_uptime(self, ltype, source, server, disp):
		if not server:
			server = InstansesDesc[Gen_disp][0]
		iq = xmpp.Iq(to = server, typ = Types[10])
		iq.addChild(Types[18], {}, [], xmpp.NS_LAST)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_idle, {"ltype": ltype, "source": source, "instance": server, "typ": None})

	def command_idle(self, ltype, source, instance, disp):
		if instance:
			nick = instance
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereTS(instance):
					instance = "%s/%s" % (source[1], instance)
				else:
					answer = self.AnsBase[5] % (instance)
			if not locals().has_key(Types[12]):
				iq = xmpp.Iq(to = instance, typ = Types[10])
				iq.addChild(Types[18], {}, [], xmpp.NS_LAST)
				iq.setID("Bs-i%d" % Info["outiq"].plus())
				CallForResponse(disp, iq, self.answer_idle, {"ltype": ltype, "source": source, "instance": nick, "typ": True})
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def answer_idle(self, disp, stanza, ltype, source, instance, typ):
		if xmpp.isResultNode(stanza):
			seconds = stanza.getTagAttr(Types[18], "seconds")
			if seconds and seconds != "0" and isNumber(seconds):
				answer = (self.AnsBase[8] if typ else self.AnsBase[7]) % (instance, Time2Text(int(seconds)))
		if not locals().has_key(Types[12]):
			answer = self.AnsBase[6]
		Answer(answer, ltype, source, disp)

	def command_afls(self, ltype, source, body, disp):

		def get_req(body):
			afls = ("owner", "admin", "member", "outcast")
			if DefLANG in ("RU", "UA"):
				alsRU = [afl.decode("utf-8") for afl in ("овнер", "админ", "мембер", "бан")]
				for afl in alsRU:
					if body.count(afl):
						return afls[alsRU.index(afl)]
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
					CallForResponse(disp, iq, self.answer_afls, {"ltype": ltype, "source": source, "Numb": Numb})
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def answer_afls(self, disp, stanza, ltype, source, Numb):
		if xmpp.isResultNode(stanza):
			Number, answer = itypes.Number(), str()
			for node in stanza.getChildren():
				for node in node.getChildren():
					if node and node != "None":
						jid = node.getAttr("jid")
						if jid:
							if Numb and Numb <= Number._int():
								Number.plus()
							else:
								answer += "\n%d) %s" % (Number.plus(), jid)
								signature = node.getTagData("reason")
								if signature:
									answer += " [%s]" % (signature)
			if answer:
				if Numb and Numb < Number._int():
					answer += "\n...\nTotal: %s items." % (Number._str())
				Message(source[0], answer, disp)
				if ltype == Types[1]:
					answer = AnsBase[11]
				else:
					del answer
			else:
				answer = self.AnsBase[6]
		else:
			answer = self.AnsBase[6]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	commands = (
		(command_ping, "ping", 1,),
		(command_ping_stat, "pstat", 1,),
		(command_version, "version", 1,),
		(command_uptime, "uptime", 1,),
		(command_idle, "idle", 1,),
		(command_afls, "list", 4,)
					)
