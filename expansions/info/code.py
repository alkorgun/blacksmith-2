# coding: utf-8

#  BlackSmith mark.2
exp_name = "info" # /code.py v.x5
#  Id: 11~4a
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_online(self, ltype, source, body, disp):
		list, Numb, ThrIds = self.AnsBase[7], itypes.Number(), iThr.ThrNames()
		for disp_ in sorted(InstansesDesc.keys()):
			connect, alive = online(disp_), str("%s%s" % (Types[13], disp_) in ThrIds)
			if not connect:
				connect = False
			list += "\n%d) %s - %s - %s" % (Numb.plus(), disp_, str(connect), alive)
		if ltype == Types[1]:
			Answer(AnsBase[11], ltype, source, disp)
		Message(source[0], list, disp)

	def command_inchat(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			list, Numb, acc = self.AnsBase[8], itypes.Number(), enough_access(source[1], source[2], 4)
			owners, admins, members, none = [], [], [], []
			for nick in Chats[source[1]].sorted_users():
				if nick.ishere:
					text = nick.nick
					if acc and nick.source:
						text += " (%s)" % (nick.source)
					if nick.role[0] == aRoles[5]:
						owners.append(text)
					elif nick.role[0] == aRoles[4]:
						admins.append(text)
					elif nick.role[0] == aRoles[3]:
						members.append(text)
					else:
						none.append(text)
			if owners:
				list += "\n\nOwners:"
				for x in owners:
					list += "\n%d) %s" % (Numb.plus(), x)
			if admins:
				list += "\n\nAdmins:"
				for x in admins:
					list += "\n%d) %s" % (Numb.plus(), x)
			if members:
				list += "\n\nMembers:"
				for x in members:
					list += "\n%d) %s" % (Numb.plus(), x)
			if none:
				list += "\n\nOthers:"
				for x in none:
					list += "\n%d) %s" % (Numb.plus(), x)
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			Message(source[0], list, disp)
		else:
			Answer(AnsBase[0], ltype, source, disp)

	def command_conflist(self, ltype, source, body, disp):
		answer, Numb, admin = self.AnsBase[5], itypes.Number(), enough_access(source[1], source[2], 7)
		for conf in sorted(Chats.keys()):
			BsNick = get_self_nick(conf)
			isModer = str(Chats[conf].isModer)
			ConfName = conf.split("@")[0]
			disp_ = (Chats[conf].disp if admin else "***")
			cPref = str(Chats[conf].cPref)
			online = itypes.Number()
			for nick in Chats[conf].get_users():
				if nick.ishere:
					online.plus()
			answer += '\n%d) %s/%s [%s] "%s" (%s) - %s' % (Numb.plus(), ConfName, BsNick, disp_, cPref, online._str(), isModer)
		if Numb._int():
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			Message(source[0], answer, disp)
		else:
			Answer(self.AnsBase[6], ltype, source, disp)

	def command_visitors(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				Var = body.lower()
			else:
				Var = "default"
			if Var in ("today", "сегодня".decode("utf-8")):
				list = str()
				date = Yday()
				Numb = itypes.Number()
				Numb2 = itypes.Number()
				for nick in Chats[source[1]].sorted_users():
					if not nick.ishere:
						if nick.date[1] == date:
							if nick.source:
								list += "\n%d. %s (%s)" % (Numb.plus(), nick.nick, nick.source)
							else:
								list += "\n%d. %s" % (Numb.plus(), nick.nick)
					else:
						Numb2.plus()
				if Numb._int():
					if ltype == Types[1]:
						Answer(AnsBase[11], ltype, source, disp)
					Message(source[0], self.AnsBase[0] % (Numb._str(), list, Numb2._str()), disp)
				else:
					Answer(self.AnsBase[1], ltype, source, disp)
			elif Var in ("dates", "даты".decode("utf-8")):
				list = str()
				Numb = itypes.Number()
				for nick in Chats[source[1]].sorted_users():
					list += "\n%d. %s\t\t%s" % (Numb.plus(), nick.nick, nick.date[2])
				if ltype == Types[1]:
					Answer(AnsBase[11], ltype, source, disp)
				Message(source[0], self.AnsBase[2] % (Numb._str(), list), disp)
			elif Var in ("list", "лист".decode("utf-8")):
				ls = sorted(Chats[source[1]].get_nicks())
				if ltype == Types[1]:
					Answer(AnsBase[11], ltype, source, disp)
				Message(source[0], self.AnsBase[2] % (str(len(ls)), ", ".join(ls)), disp)
			else:
				list = str()
				Numb = itypes.Number()
				Numb2 = itypes.Number()
				for nick in Chats[source[1]].sorted_users():
					if not nick.ishere:
						if nick.source:
							list += "\n%d. %s (%s)" % (Numb.plus(), nick.nick, nick.source)
						else:
							list += "\n%d. %s" % (Numb.plus(), nick.nick)
					else:
						Numb2.plus()
				if Numb._int():
					if ltype == Types[1]:
						Answer(AnsBase[11], ltype, source, disp)
					Message(source[0], self.AnsBase[3] % (Numb._str(), list, Numb2._str()), disp)
				else:
					Answer(self.AnsBase[4], ltype, source, disp)
		else:
			Answer(AnsBase[0], ltype, source, disp)

	def command_search(self, ltype, source, body, disp):
		if body:
			list, Numb, acc = str(), itypes.Number(), enough_access(source[1], source[2], 7)
			for conf in sorted(Chats.keys()):
				for nick in sorted(Chats[conf].get_nicks()):
					if Chats[conf].isHereTS(nick):
						jid = get_source(conf, nick)
						if nick.count(body) or (jid and jid.count(body)):
							list += "\n%d) %s (%s)" % (Numb.plus(), nick, conf)
							if jid and acc:
								list += " [%s]" % (jid)
							if Numb._int() >= 20:
								break
			if Numb._int():
				if ltype == Types[1]:
					Answer(AnsBase[11], ltype, source, disp)
				Message(source[0], self.AnsBase[9] % (Numb._str(), list), disp)
			else:
				answer = self.AnsBase[10]
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	commands = (
		(command_online, "online", 7,),
		(command_inchat, "inmuc", 2,),
		(command_conflist, "chatslist", 5,),
		(command_visitors, "visitors", 4,),
		(command_search, "search", 2,)
					)
