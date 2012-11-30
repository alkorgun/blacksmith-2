# coding: utf-8

#  BlackSmith mark.2
# exp_name = "get_iq" # /code.py v.x7
#  Id: 13~6c
#  Code © (2010-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_ping(self, stype, source, instance, disp):
		if instance:
			source_ = instance
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereTS(instance):
					conf_nick = (source[1], instance)
					instance, source_ = "%s/%s" % conf_nick, get_source(*conf_nick)
				else:
					Answer(self.AnsBase[5] % (instance), stype, source, disp)
					raise iThr.ThrKill("exit")
		else:
			instance, source_ = source[0], get_source(source[1], source[2])
		iq = xmpp.Iq(to = instance, typ = Types[10])
		iq.addChild(Types[16], namespace = xmpp.NS_PING)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_ping, {"stype": stype, "source": source, "instance": instance, "source_": source_, "start": time.time()})

	PingStats = {}

	def answer_ping(self, disp, stanza, stype, source, instance, source_, start):
		if xmpp.isResultNode(stanza):
			answer = round(time.time() - start, 3)
			if source_:
				if not self.PingStats.has_key(source_):
					self.PingStats[source_] = []
				self.PingStats[source_].append(answer)
			Answer(self.AnsBase[0] % str(answer), stype, source, disp)
		else:
			iq = xmpp.Iq(to = instance, typ = Types[10])
			iq.addChild(Types[18], namespace = xmpp.NS_VERSION)
			iq.setID("Bs-i%d" % Info["outiq"].plus())
			CallForResponse(disp, iq, self.answer_ping_ver, {"stype": stype, "source": source, "instance": instance, "source_": source_, "start": time.time()})

	def answer_ping_ver(self, disp, stanza, stype, source, instance, source_, start):
		if xmpp.isResultNode(stanza):
			answer = round(time.time() - start, 3)
			if source_:
				if not self.PingStats.has_key(source_):
					self.PingStats[source_] = []
				self.PingStats[source_].append(answer)
			Name = "[None]"
			for node in stanza.getQueryChildren():
				name = node.getName()
				if name == "name":
					Name = node.getData()
					break
			answer = self.AnsBase[1] % (Name, str(answer))
		else:
			answer = self.AnsBase[2]
		Answer(answer, stype, source, disp)

	def command_ping_stats(self, stype, source, source_, disp):
		if source_:
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(source_):
				source_ = get_source(source[1], source_)
			else:
				source_ = source_.lower()
		else:
			source_ = get_source(source[1], source[2])
		if source_ and self.PingStats.has_key(source_):
			Number = float(sum(self.PingStats[source_]))
			len_ = len(self.PingStats[source_])
			max_ = max(self.PingStats[source_])
			min_ = min(self.PingStats[source_])
			if len_:
				answer = self.AnsBase[3] % (str(len_), str(min_), str(max_), str(round(Number / len_, 3)))
			else:
				answer = self.AnsBase[4]
		else:
			answer = self.AnsBase[4]
		Answer(answer, stype, source, disp)

	def command_time(self, stype, source, instance, disp):
		if instance:
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereTS(instance):
					instance = "%s/%s" % (source[1], instance)
				else:
					Answer(self.AnsBase[5] % (instance), stype, source, disp)
					raise iThr.ThrKill("exit")
		else:
			instance = source[0]
		iq = xmpp.Iq(to = instance, typ = Types[10])
		iq.addChild(Types[18], namespace = xmpp.NS_URN_TIME)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_time0202, {"stype": stype, "source": source, "instance": instance})

	def answer_time0202(self, disp, stanza, stype, source, instance):
		if xmpp.isResultNode(stanza):
			hours = None
			for node in stanza.getChildren():
				tzo = node.getTagData("tzo")
				if tzo and tzo.startswith((chr(43), chr(45))):
					try:
						hours, minutes = tzo[1:].split(chr(58))
						symbol = tzo[0]
						hours, minutes = int(symbol + hours), int(symbol + minutes)
					except:
						pass
					else:
						break
			if isinstance(hours, int):
				plus = (symbol == chr(43))
				date = list(time.gmtime())
				days = (31, 31, (28 if (date[0] % 4) else 29), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
				date[4] += minutes
				date[3] += hours
				if date[4] >= 60:
					date[4] -= 60
					date[3] += 1
				if date[3] >= 24:
					date[3] -= 24
					if plus:
						date[2] += 1
						if date[2] > days[date[1]]:
							date[2] = 1
							date[1] += 1
							if date[1] > 12:
								date[1] = 1
								date[0] += 1
					else:
						date[2] -= 1
						if not date[2]:
							date[1] -= 1
							date[2] = days[date[1]]
							if not date[1]:
								date[1] = 12
								date[0] -= 1
				try:
					date = time.struct_time(date)
				except:
					answer = self.AnsBase[6]
				else:
					answer = time.strftime("%a %b %d %H:%M:%S %Y", date)
			else:
				answer = self.AnsBase[6]
			Answer(answer, stype, source, disp)
		else:
			iq = xmpp.Iq(to = instance, typ = Types[10])
			iq.addChild(Types[18], namespace = xmpp.NS_TIME)
			iq.setID("Bs-i%d" % Info["outiq"].plus())
			CallForResponse(disp, iq, self.answer_time0090, {"stype": stype, "source": source})

	def answer_time0090(self, disp, stanza, stype, source):
		if xmpp.isResultNode(stanza):
			Time = None
			for node in stanza.getQueryChildren():
				if "display" == node.getName():
					Time = node.getData()
			answer = Time or self.AnsBase[6]
		else:
			answer = self.AnsBase[6]
		Answer(answer, stype, source, disp)

	def command_version(self, stype, source, instance, disp):
		if instance:
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereTS(instance):
					instance = "%s/%s" % (source[1], instance)
				else:
					Answer(self.AnsBase[5] % (instance), stype, source, disp)
					raise iThr.ThrKill("exit")
		else:
			instance = source[0]
		iq = xmpp.Iq(to = instance, typ = Types[10])
		iq.addChild(Types[18], namespace = xmpp.NS_VERSION)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_version, {"stype": stype, "source": source})

	def answer_version(self, disp, stanza, stype, source):
		if xmpp.isResultNode(stanza):
			Name, Ver, Os = "[None]", "[None]", "[None]"
			for node in stanza.getQueryChildren():
				name = node.getName()
				if name == "name":
					Name = node.getData()
				elif name == "version":
					Ver = node.getData()
				elif name == "os":
					Os = node.getData()
			answer = "\nName: %s\nVer.: %s\nOS: %s" % (Name, Ver, Os)
		else:
			answer = self.AnsBase[6]
		Answer(answer, stype, source, disp)

	XEPs.add(xmpp.NS_VCARD)

	def command_vcard(self, stype, source, instance, disp):
		if instance:
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereTS(instance):
					instance = "%s/%s" % (source[1], instance)
				else:
					Answer(self.AnsBase[5] % (instance), stype, source, disp)
					raise iThr.ThrKill("exit")
		else:
			instance = source[0]
		iq = xmpp.Iq(to = instance, typ = Types[10])
		iq.addChild(Types[18], namespace = xmpp.NS_VCARD)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_vcard, {"stype": stype, "source": source})

	VcardDesc = {
		"NICKNAME": "Nick",
		"GIVEN": "Name",
		"FAMILY": "Surname",
		"FN": "Full Name",
		"BDAY": "Birthday",
		"USERID": "e-Mail",
		"URL": "Web Page",
		"DESC": "Description",
		"NUMBER": "Phone",
		"EXTADR": "Address",
		"PCODE": "Post Code",
		"LOCALITY": "City",
		"CTRY": "Country",
		"ORGNAME": "Organization",
		"ORGUNIT": "Department"
					}

	def parse_vcard(self, node, ls):
		if node.kids:
			for node in node.getChildren():
				name = node.getName()
				if name == "PHOTO":
					continue
				self.parse_vcard(node, ls)
		else:
			data = (node.getData()).strip()
			if data and len(data) <= 512:
				name = node.getName()
				name = self.VcardDesc.get(name, name.capitalize())
				ls.append("%s: %s" % (name, data))

	def answer_vcard(self, disp, stanza, stype, source):
		if xmpp.isResultNode(stanza):
			ls = []
			self.parse_vcard(stanza, ls)
			if ls:
				ls.insert(0, "\->")
				answer = str.join(chr(10), ls)
			else:
				answer = self.AnsBase[10]
		else:
			answer = self.AnsBase[6]
		Answer(answer, stype, source, disp)

	def command_uptime(self, stype, source, server, disp):
		if not server:
			server = disp._owner.Server
		iq = xmpp.Iq(to = server, typ = Types[10])
		iq.addChild(Types[18], namespace = xmpp.NS_LAST)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_idle, {"stype": stype, "source": source, "instance": server, "typ": None})

	def command_idle(self, stype, source, instance, disp):
		if instance:
			nick = instance
			if Chats.has_key(source[1]) and Chats[source[1]].isHere(instance):
				if Chats[source[1]].isHereTS(instance):
					instance = "%s/%s" % (source[1], instance)
				else:
					answer = self.AnsBase[5] % (instance)
			if not locals().has_key(Types[6]):
				iq = xmpp.Iq(to = instance, typ = Types[10])
				iq.addChild(Types[18], namespace = xmpp.NS_LAST)
				iq.setID("Bs-i%d" % Info["outiq"].plus())
				CallForResponse(disp, iq, self.answer_idle, {"stype": stype, "source": source, "instance": nick, "typ": True})
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def answer_idle(self, disp, stanza, stype, source, instance, typ):
		if xmpp.isResultNode(stanza):
			seconds = stanza.getTagAttr(Types[18], "seconds")
			if seconds and seconds != "0" and isNumber(seconds):
				answer = (self.AnsBase[8] if typ else self.AnsBase[7]) % (instance, Time2Text(int(seconds)))
		if not locals().has_key(Types[6]):
			answer = self.AnsBase[6]
		Answer(answer, stype, source, disp)

	affs = ("owner", "admin", "member", "outcast")

	def command_aflist(self, stype, source, body, disp):

		def get_req(body):
			if DefLANG in ("RU", "UA"):
				affsRU = ["овнер", "админ", "мембер", "бан"]
				for name in affsRU:
					if body.count(name.decode("utf-8")):
						return self.affs[affsRU.index(name)]
			return (body if self.affs.count(body) else None)

		if Chats.has_key(source[1]):
			if body:
				ls = body.split()
				body = (ls.pop(0)).lower()
				if body in ("search", "искать".decode("utf-8")):
					if ls:
						data = (ls.pop(0)).lower()
						desc = {}
						for name in self.affs:
							iq = xmpp.Iq(to = source[1], typ = Types[10])
							query = xmpp.Node(Types[18])
							query.setNamespace(xmpp.NS_MUC_ADMIN)
							query.addChild("item", {aRoles[0]: name})
							iq.addChild(node = query)
							iq.setID("Bs-i%d" % Info["outiq"].plus())
							CallForResponse(disp, iq, self.answer_aflist_search, {"desc": desc, "name": name, "data": data})
						for x in xrange(60):
							sleep(0.2)
							if len(desc.keys()) == 4:
								break
						Number = itypes.Number()
						ls = []
						for name, matches in desc.iteritems():
							if matches:
								ls.append(name.capitalize() + "s:")
								for jid in matches:
									ls.append("%d) %s" % (Number.plus(), jid))
						if ls:
							Message(source[0], str.join(chr(10), ls), disp)
							if stype == Types[1]:
								answer = AnsBase[11]
						else:
							answer = self.AnsBase[9]
					else:
						answer = AnsBase[2]
				else:
					body = get_req(body)
					if body:
						Numb = 0
						if ls:
							if isNumber(ls[0]):
								x = int(ls.pop(0))
								if x < 20:
									Numb = 20
								else:
									Numb = x
						iq = xmpp.Iq(to = source[1], typ = Types[10])
						query = xmpp.Node(Types[18])
						query.setNamespace(xmpp.NS_MUC_ADMIN)
						query.addChild("item", {aRoles[0]: body})
						iq.addChild(node = query)
						iq.setID("Bs-i%d" % Info["outiq"].plus())
						CallForResponse(disp, iq, self.answer_aflist, {"stype": stype, "source": source, "Numb": Numb})
					else:
						answer = AnsBase[2]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def answer_aflist_search(self, disp, stanza, desc, name, data):
		if xmpp.isResultNode(stanza):
			count = []
			for node in stanza.getQueryChildren():
				if node and node != "None":
					jid = node.getAttr("jid")
					if jid and jid.count(data):
						signature = node.getTagData("reason")
						if signature:
							jid = "%s (%s)" % (jid, signature)
						count.append(jid)
			desc[name] = count

	def answer_aflist(self, disp, stanza, stype, source, Numb):
		if xmpp.isResultNode(stanza):
			ls, Number = [], itypes.Number()
			for node in stanza.getQueryChildren():
				if node and node != "None":
					jid = node.getAttr("jid")
					if jid:
						if Numb and Numb <= Number._int():
							Number.plus()
						else:
							signature = node.getTagData("reason")
							if signature:
								jid = "%s (%s)" % (jid, signature)
							ls.append("%d) %s" % (Number.plus(), jid))
			if ls:
				if Numb and Numb < Number._int():
					ls.append("...\nTotal: %s items." % (Number._str()))
				Message(source[0], str.join(chr(10), ls), disp)
				if stype == Types[1]:
					answer = AnsBase[11]
			else:
				answer = self.AnsBase[6]
		else:
			answer = self.AnsBase[6]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	XEPs.add(xmpp.NS_STATS)

	def command_server_stats(self, stype, source, server, disp):
		if not server:
			server = disp._owner.Server
		iq = xmpp.Iq(to = server, typ = Types[10])
		iq.addChild(Types[18], namespace = xmpp.NS_STATS)
		iq.setID("Bs-i%d" % Info["outiq"].plus())
		CallForResponse(disp, iq, self.answer_server_stats, {"stype": stype, "source": source})

	def answer_server_stats(self, disp, stanza, stype, source):
		if xmpp.isResultNode(stanza):
			iq = xmpp.Iq(to = stanza.getFrom(), typ = Types[10])
			iq.addChild(Types[18], {}, stanza.getQueryChildren(), xmpp.NS_STATS)
			iq.setID("Bs-i%d" % Info["outiq"].plus())
			CallForResponse(disp, iq, self.answer_server_stats_get, {"stype": stype, "source": source})
		else:
			Answer(self.AnsBase[6], stype, source, disp)

	def answer_server_stats_get(self, disp, stanza, stype, source):
		if xmpp.isResultNode(stanza):
			ls = []
			for node in stanza.getQueryChildren():
				name = node.getAttr("name")
				value = node.getAttr("value")
				if name and value:
					ls.append("%s: %s" % (name, value))
			if ls:
				ls.insert(0, "Stats of %s ->" % stanza.getFrom())
				answer = str.join(chr(10), ls)
			else:
				answer = self.AnsBase[4]
		else:
			answer = self.AnsBase[6]
		Answer(answer, stype, source, disp)

	commands = (
		(command_ping, "ping", 1,),
		(command_ping_stats, "pstat", 1,),
		(command_time, "time", 1,),
		(command_version, "version", 1,),
		(command_vcard, "vcard", 2,),
		(command_uptime, "uptime", 1,),
		(command_idle, "idle", 1,),
		(command_aflist, "list", 4,),
		(command_server_stats, "servstat", 1,)
					)
