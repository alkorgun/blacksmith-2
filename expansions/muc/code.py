# coding: utf-8

#  BlackSmith mark.2
# exp_name = "muc" # /code.py v.x9
#  Id: 05~5c
#  Code © (2009-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_subject(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer or getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (None,)*2)[1] == aRoles[9]:
					Info["omsg"].plus()
					Chats[source[1]].subject(body)
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	sep = chr(47)

	def command_ban(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					if enough_access(source[1], source[2], 6) or getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5],))[0] != aRoles[5]:
						body = body.split(self.sep, 1)
						nick = (body.pop(0)).strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif nick.count(chr(46)):
							jid = nick
						else:
							jid = None
						if jid and not enough_access(jid, None, 7) and jid != get_disp(disp):
							if body:
								body = "%s: %s" % (source[2], body[0].strip())
							else:
								body = "%s/%s" % (get_nick(source[1]), source[2])
							Chats[source[1]].outcast(jid, body, (None, (stype, source)))
						else:
							answer = AnsBase[7]
					else:
						answer = self.AnsBase[0]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_none(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					if enough_access(source[1], source[2], 6) or getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5],))[0] != aRoles[5]:
						body = body.split(self.sep, 1)
						nick = (body.pop(0)).strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif nick.count(chr(46)):
							jid = nick
						else:
							jid = None
						if jid:
							if body:
								body = "%s: %s" % (source[2], body[0].strip())
							else:
								body = "%s/%s" % (get_nick(source[1]), source[2])
							Chats[source[1]].none(jid, body, (None, (stype, source)))
						else:
							answer = AnsBase[7]
					else:
						answer = self.AnsBase[0]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_member(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					if enough_access(source[1], source[2], 6) or getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5],))[0] != aRoles[5]:
						body = body.split(self.sep, 1)
						nick = (body.pop(0)).strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif nick.count(chr(46)):
							jid = nick
						else:
							jid = None
						if jid:
							if body:
								body = "%s: %s" % (source[2], body[0].strip())
							else:
								body = "%s/%s" % (get_nick(source[1]), source[2])
							Chats[source[1]].member(jid, body, (None, (stype, source)))
						else:
							answer = AnsBase[7]
					else:
						answer = self.AnsBase[0]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_admin(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5],))[0] == aRoles[5]:
					body = body.split(self.sep, 1)
					nick = (body.pop(0)).strip()
					if Chats[source[1]].isHere(nick):
						jid = get_source(source[1], nick)
					elif nick.count(chr(46)):
						jid = nick
					else:
						jid = None
					if jid:
						if body:
							body = "%s: %s" % (source[2], body[0].strip())
						else:
							body = "%s/%s" % (get_nick(source[1]), source[2])
						Chats[source[1]].admin(jid, body, (None, (stype, source)))
					else:
						answer = AnsBase[7]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_owner(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5],))[0] == aRoles[5]:
					body = body.split(self.sep, 1)
					nick = (body.pop(0)).strip()
					if Chats[source[1]].isHere(nick):
						jid = get_source(source[1], nick)
					elif nick.count(chr(46)):
						jid = nick
					else:
						jid = None
					if jid:
						if body:
							body = "%s: %s" % (source[2], body[0].strip())
						else:
							body = "%s/%s" % (get_nick(source[1]), source[2])
						Chats[source[1]].owner(jid, body, (None, (stype, source)))
					else:
						answer = AnsBase[7]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_kick(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				aRole = getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5], None))
				if Chats[source[1]].isModer or aRole[1] == aRoles[9]:
					if enough_access(source[1], source[2], 6) or aRole[0] != aRoles[5]:
						body = body.split(self.sep, 1)
						nick = (body.pop(0)).strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						else:
							jid, nick = None, None
						if nick and jid and not enough_access(jid, None, 7) and jid != get_disp(disp):
							if body:
								body = "%s: %s" % (source[2], body[0].strip())
							else:
								body = "%s/%s" % (get_nick(source[1]), source[2])
							Chats[source[1]].kick(nick, body, (None, (stype, source)))
						else:
							answer = AnsBase[7]
					else:
						answer = self.AnsBase[0]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_visitor(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				aRole = getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5], None))
				if Chats[source[1]].isModer or aRole[1] == aRoles[9]:
					if enough_access(source[1], source[2], 6) or aRole[0] != aRoles[5]:
						body = body.split(self.sep, 1)
						nick = (body.pop(0)).strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						else:
							jid, nick = None, None
						if nick and jid and not enough_access(jid, None, 7) and jid != get_disp(disp):
							if body:
								body = "%s: %s" % (source[2], body[0].strip())
							else:
								body = "%s/%s" % (get_nick(source[1]), source[2])
							Chats[source[1]].visitor(nick, body, (None, (stype, source)))
						else:
							answer = AnsBase[7]
					else:
						answer = self.AnsBase[0]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_participant(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				aRole = getattr(Chats[source[1]].get_user(get_nick(source[1])), "role", (aRoles[5], None))
				if Chats[source[1]].isModer or aRole[1] == aRoles[9]:
					if enough_access(source[1], source[2], 6) or aRole[0] != aRoles[5]:
						body = body.split(self.sep, 1)
						nick = (body.pop(0)).strip()
						if Chats[source[1]].isHere(nick):
							if body:
								body = "%s: %s" % (source[2], body[0].strip())
							else:
								body = "%s/%s" % (get_nick(source[1]), source[2])
							Chats[source[1]].participant(nick, body, (None, (stype, source)))
						else:
							answer = AnsBase[7]
					else:
						answer = self.AnsBase[0]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_moder(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					body = body.split(self.sep, 1)
					nick = (body.pop(0)).strip()
					if Chats[source[1]].isHere(nick):
						if body:
							body = "%s: %s" % (source[2], body[0].strip())
						else:
							body = "%s/%s" % (get_nick(source[1]), source[2])
						Chats[source[1]].moder(nick, body, (None, (stype, source)))
					else:
						answer = AnsBase[7]
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	PerfDesc = {"done": 0, "fail": 0}

	def HandleFB(self, disp, stanza, desc):
		if xmpp.isResultNode(stanza):
			desc["done"] += 1
		else:
			desc["fail"] += 1

	def calcPerformance(self, desc):
		cl = len(Chats.keys())
		for x in xrange(60):
			sleep(0.2)
			if cl <= sum(desc.values()):
				break
		sl = sum(desc.values())
		if cl > sl:
			desc["none"] = (cl - sl)
			answer = self.AnsBase[2] %  desc
		elif desc["fail"]:
			answer = self.AnsBase[3] %  desc
		else:
			answer = self.AnsBase[4]
		return answer

	def command_fullban(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				body = body.split(self.sep, 1)
				nick = (body.pop(0)).strip()
				if Chats[source[1]].isHere(nick):
					jid = get_source(source[1], nick)
				elif nick.count(chr(46)):
					jid = nick
				else:
					jid = None
				if nick and jid and not enough_access(jid, None, 7) and jid != get_disp(disp):
					if body:
						body = "%s: %s" % (source[2], body[0].strip())
					else:
						body = "%s/%s" % (get_nick(source[1]), source[2])
					desc = self.PerfDesc.copy()
					for conf in Chats.itervalues():
						conf.outcast(jid, body, (self.HandleFB, {"desc": desc}))
					answer = self.calcPerformance(desc)
				else:
					answer = AnsBase[7]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	def command_fullunban(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				body = body.split(self.sep, 1)
				nick = (body.pop(0)).strip()
				if Chats[source[1]].isHere(nick):
					jid = get_source(source[1], nick)
				elif nick.count(chr(46)):
					jid = nick
				else:
					jid = None
				if jid:
					desc = self.PerfDesc.copy()
					for conf in Chats.itervalues():
						conf.none(jid, handler = (self.HandleFB, {"desc": desc}))
					answer = self.calcPerformance(desc)
				else:
					answer = AnsBase[7]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	commands = (
		(command_subject, "subject", 3,),
		(command_ban, "ban", 5,),
		(command_none, "none", 5,),
		(command_member, "member", 5,),
		(command_admin, "admin", 6,),
		(command_owner, "owner", 6,),
		(command_kick, "kick", 3,),
		(command_visitor, "visitor", 3,),
		(command_participant, "participant", 3,),
		(command_moder, "moder", 5,),
		(command_fullban, "fullban", 7,),
		(command_fullunban, "fullunban", 7,)
					)
