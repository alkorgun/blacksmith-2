# coding: utf-8

#  BlackSmith mark.2
# exp_name = "info" # /code.py v.x6
#  Id: 11~5c
#  Code © (2010-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_online(self, stype, source, body, disp):
		ls, ThrIds = self.AnsBase[7], iThr.ThrNames()
		for numb, disp_ in enumerate(sorted(InstansesDesc.keys()), 1):
			connect, alive = online(disp_), str("%s-%s" % (Types[13], disp_) in ThrIds)
			if not connect:
				connect = None
			ls += "\n%d) %s - %s - %s" % (numb, disp_, str(connect), alive)
		if stype == Types[1]:
			Answer(AnsBase[11], stype, source, disp)
		Message(source[0], ls, disp)

	def command_inchat(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			ls, Numb, access = self.AnsBase[8], itypes.Number(), enough_access(source[1], source[2], 4)
			owners, admins, members, none = [], [], [], []
			for nick in Chats[source[1]].sorted_users():
				if nick.ishere:
					data = nick.nick
					if access and nick.source:
						data += " (%s)" % (nick.source)
					if nick.role[0] == aRoles[5]:
						owners.append(data)
					elif nick.role[0] == aRoles[4]:
						admins.append(data)
					elif nick.role[0] == aRoles[3]:
						members.append(data)
					else:
						none.append(data)
			if owners:
				ls += "\n\nOwners:"
				for x in owners:
					ls += "\n%d) %s" % (Numb.plus(), x)
			if admins:
				ls += "\n\nAdmins:"
				for x in admins:
					ls += "\n%d) %s" % (Numb.plus(), x)
			if members:
				ls += "\n\nMembers:"
				for x in members:
					ls += "\n%d) %s" % (Numb.plus(), x)
			if none:
				ls += "\n\nOthers:"
				for x in none:
					ls += "\n%d) %s" % (Numb.plus(), x)
			if stype == Types[1]:
				Answer(AnsBase[11], stype, source, disp)
			Message(source[0], ls, disp)
		else:
			Answer(AnsBase[0], stype, source, disp)

	def command_conflist(self, stype, source, body, disp):
		ls, Numb, access = [], itypes.Number(), enough_access(source[1], source[2], 7)
		for conf_str, conf in sorted(Chats.items()):
			isModer = str(conf.isModer)
			cName = conf_str.split("@")[0]
			disp_ = (conf.disp if access else "***")
			cPref = str(conf.cPref)
			online = itypes.Number()
			for nick in conf.get_users():
				if nick.ishere:
					online.plus()
			ls.append("%d) %s/%s [%s] \"%s\" (%s) - %s" % (Numb.plus(), cName, conf.nick, disp_, cPref, online._str(), isModer))
		if ls:
			if stype == Types[1]:
				Answer(AnsBase[11], stype, source, disp)
			ls.insert(0, self.AnsBase[5])
			Message(source[0], str.join(chr(10), ls), disp)
		else:
			Answer(self.AnsBase[6], stype, source, disp)

	def command_visitors(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				body = body.lower()
			else:
				body = "default"
			if body in ("today", "сегодня".decode("utf-8")):
				Number = itypes.Number()
				Numb = itypes.Number()
				ls = []
				date = Yday()
				for nick in Chats[source[1]].sorted_users():
					if not nick.ishere:
						if nick.date[1] == date:
							if nick.source:
								ls.append("%d. %s (%s)" % (Number.plus(), nick.nick, nick.source))
							else:
								ls.append("%d. %s" % (Number.plus(), nick.nick))
					else:
						Numb.plus()
				if Number._int():
					if stype == Types[1]:
						Answer(AnsBase[11], stype, source, disp)
					Message(source[0], self.AnsBase[0] % (Number._str(), str.join(chr(10), ls), Numb._str()), disp)
				else:
					Answer(self.AnsBase[1], stype, source, disp)
			elif body in ("dates", "даты".decode("utf-8")):
				Number = itypes.Number()
				ls = []
				for nick in Chats[source[1]].sorted_users():
					ls.append("%d. %s\t\t%s" % (Number.plus(), nick.nick, nick.date[2]))
				if stype == Types[1]:
					Answer(AnsBase[11], stype, source, disp)
				Message(source[0], self.AnsBase[2] % (Number._str(), str.join(chr(10))), disp)
			elif body in ("list", "лист".decode("utf-8")):
				ls = sorted(Chats[source[1]].get_nicks())
				if stype == Types[1]:
					Answer(AnsBase[11], stype, source, disp)
				Message(source[0], self.AnsBase[2] % (str(len(ls)), ", ".join(ls)), disp)
			else:
				Number = itypes.Number()
				Numb = itypes.Number()
				ls = []
				for nick in Chats[source[1]].sorted_users():
					if not nick.ishere:
						if nick.source:
							ls.append("%d. %s (%s)" % (Number.plus(), nick.nick, nick.source))
						else:
							ls.append("%d. %s" % (Number.plus(), nick.nick))
					else:
						Numb.plus()
				if Number._int():
					if stype == Types[1]:
						Answer(AnsBase[11], stype, source, disp)
					Message(source[0], self.AnsBase[3] % (Number._str(), str.join(chr(10), ls), Numb._str()), disp)
				else:
					Answer(self.AnsBase[4], stype, source, disp)
		else:
			Answer(AnsBase[0], stype, source, disp)

	def command_search(self, stype, source, body, disp):
		if body:
			ls, Numb, access = "", itypes.Number(), enough_access(source[1], source[2], 7)
			for conf_str, conf in sorted(Chats.items()):
				for nick in sorted(conf.get_nicks()):
					if conf.isHereTS(nick):
						jid = get_source(conf_str, nick)
						if nick.count(body) or (jid and jid.count(body)):
							ls += "\n%d) %s (%s)" % (Numb.plus(), nick, conf_str)
							if jid and access:
								ls += " [%s]" % (jid)
							if Numb._int() >= 20:
								break
			if Numb._int():
				if stype == Types[1]:
					Answer(AnsBase[11], stype, source, disp)
				Message(source[0], self.AnsBase[9] % (Numb._str(), ls), disp)
			else:
				answer = self.AnsBase[10]
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	commands = (
		(command_online, "online", 7,),
		(command_inchat, "inmuc", 2,),
		(command_conflist, "chatslist", 5,),
		(command_visitors, "visitors", 4,),
		(command_search, "search", 2,)
					)
