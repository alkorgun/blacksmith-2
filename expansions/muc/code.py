# coding: utf-8

#  BlackSmith mark.2
exp_name = "muc" # /code.py v.x7
#  Id: 05~3a
#  Code © (2009-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_subject(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Info["omsg"].plus()
					Chats[source[1]].subject(xmpp.XMLescape(body))
				else:
					answer = self.AnsBase[1]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_ban(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif Chats[source[1]].isHere(Nick):
							jid = get_source(source[1], Nick)
						elif nick.count(chr(46)) and not Nick.count(chr(32)):
							jid = Nick
						else:
							jid = None
						if jid and Galist.get(jid, 0) < 7 and not Clients.has_key(jid):
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].outcast(jid, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_none(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif Chats[source[1]].isHere(Nick):
							jid = get_source(source[1], Nick)
						elif nick.count(chr(46)) and not Nick.count(chr(32)):
							jid = Nick
						else:
							jid = None
						if jid:
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].none(jid, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_member(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif Chats[source[1]].isHere(Nick):
							jid = get_source(source[1], Nick)
						elif nick.count(chr(46)) and not Nick.count(chr(32)):
							jid = Nick
						else:
							jid = None
						if jid:
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].member(jid, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_admin(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif Chats[source[1]].isHere(Nick):
							jid = get_source(source[1], Nick)
						elif nick.count(chr(46)) and not Nick.count(chr(32)):
							jid = Nick
						else:
							jid = None
						if jid:
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].admin(jid, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_owner(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							jid = get_source(source[1], nick)
						elif Chats[source[1]].isHere(Nick):
							jid = get_source(source[1], Nick)
						elif nick.count(chr(46)) and not Nick.count(chr(32)):
							jid = Nick
						else:
							jid = None
						if jid:
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].owner(jid, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_kick(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							pass
						elif Chats[source[1]].isHere(Nick):
							nick = Nick
						else:
							nick = None
						jid = get_source(source[1], nick)
						if nick and jid and Galist.get(jid, 0) < 7 and jid != get_disp(disp):
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].kick(nick, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_visitor(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							pass
						elif Chats[source[1]].isHere(Nick):
							nick = Nick
						else:
							nick = None
						jid = get_source(source[1], nick)
						if nick and jid and Galist.get(jid, 0) < 7:
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].visitor(nick, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_participant(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							pass
						elif Chats[source[1]].isHere(Nick):
							nick = Nick
						else:
							nick = None
						if nick:
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].participant(nick, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_moder(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if Chats[source[1]].isModer:
					Lock, BsNick = False, get_self_nick(source[1])
					if getattr(Chats[source[1]].get_user(BsNick), "role", (AflRoles[5],))[0] == AflRoles[5]:
						if not enough_access(source[1], source[2], 6):
							Lock = True
					if not Lock:
						body = body.split(chr(47), 1)
						nick = body.pop(0)
						Nick = nick.strip()
						if Chats[source[1]].isHere(nick):
							pass
						elif Chats[source[1]].isHere(Nick):
							nick = Nick
						else:
							nick = None
						if nick:
							if body and body[0]:
								text = "%s: %s" % (source[2], (body.pop(0)).strip())
							else:
								text = "%s/%s" % (get_self_nick(source[1]), source[2])
							Chats[source[1]].moder(nick, text, (None, (ltype, source)))
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
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	PerfDesc = {"done": 0, "fail": 0}

	def HandleFB(self, disp, stanza, desc):
		if xmpp.isResultNode(stanza):
			desc["done"] += 1
		else:
			desc["fail"] += 1

	def calcPerformance(self, desc):
		cl = len(Chats.keys())
		for x in xrange(60):
			time.sleep(0.2)
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

	def command_fullban(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				body = body.split(chr(47), 1)
				nick = body.pop(0)
				Nick = nick.strip()
				if Chats[source[1]].isHere(nick):
					jid = get_source(source[1], nick)
				elif Chats[source[1]].isHere(Nick):
					jid = get_source(source[1], Nick)
				elif nick.count(chr(46)) and not Nick.count(chr(32)):
					jid = Nick
				else:
					jid = None
				if jid and Galist.get(jid, 0) < 7 and not Clients.has_key(jid):
					if body and body[0]:
						text = "%s: %s" % (source[2], (body.pop(0)).strip())
					else:
						text = "%s/%s" % (get_self_nick(source[1]), source[2])
					desc = self.PerfDesc.copy()
					for conf in Chats.keys():
						Chats[conf].outcast(jid, text, (self.HandleFB, {"desc": desc}))
					answer = self.calcPerformance(desc)
				else:
					answer = AnsBase[7]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	def command_fullunban(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				body = body.split(chr(47), 1)
				nick = body.pop(0)
				Nick = nick.strip()
				if Chats[source[1]].isHere(nick):
					jid = get_source(source[1], nick)
				elif Chats[source[1]].isHere(Nick):
					jid = get_source(source[1], Nick)
				elif nick.count(chr(46)) and not Nick.count(chr(32)):
					jid = Nick
				else:
					jid = None
				if jid:
					desc = self.PerfDesc.copy()
					for conf in Chats.keys():
						Chats[conf].none(jid, handler = (self.HandleFB, {"desc": desc}))
					answer = self.calcPerformance(desc)
				else:
					answer = AnsBase[7]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

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
