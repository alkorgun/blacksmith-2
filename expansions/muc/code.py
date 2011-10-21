# coding: utf-8

#  BlackSmith mark.2
exp_name = "muc" # /code.py v.x7
#  Id: 05~3a
#  Code © (2009-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_subject(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			if Chats[source[1]].isModer:
				Info["omsg"].plus()
				Chats[source[1]].subject(xmpp.XMLescape(body))
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_ban(ltype, source, body, disp):
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
						Chats[source[1]].ban(jid, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_none(ltype, source, body, disp):
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
						Chats[source[1]].none(jid, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_member(ltype, source, body, disp):
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
						Chats[source[1]].member(jid, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_admin(ltype, source, body, disp):
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
						Chats[source[1]].admin(jid, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_owner(ltype, source, body, disp):
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
						Chats[source[1]].owner(jid, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_kick(ltype, source, body, disp):
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
						Chats[source[1]].kick(nick, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_visitor(ltype, source, body, disp):
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
						Chats[source[1]].visitor(nick, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_participant(ltype, source, body, disp):
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
						Chats[source[1]].participant(nick, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_moder(ltype, source, body, disp):
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
						Chats[source[1]].moder(nick, text, (ltype, source))
					else:
						answer = AnsBase[7]
				else:
					answer = MucAnsBase[0]
			else:
				answer = MucAnsBase[1]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_fullban(ltype, source, body, disp):
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
				for conf in Chats.keys():
					Chats[conf].ban(jid, text)
				answer = AnsBase[4]
			else:
				answer = AnsBase[7]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def command_fullunban(ltype, source, body, disp):
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
				for conf in Chats.keys():
					Chats[conf].none(jid)
				answer = AnsBase[4]
			else:
				answer = AnsBase[7]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_ban, command_none, command_member, command_admin, command_owner, command_kick, command_visitor, command_participant, command_moder, command_fullban, command_fullunban])
expansions[exp_name].ls.extend(["MucAnsBase"])

command_handler(command_subject, {"RU": "топик", "EN": "subject"}, 3, exp_name)
command_handler(command_ban, {"RU": "бан", "EN": "ban"}, 5, exp_name)
command_handler(command_none, {"RU": "никто", "EN": "none"}, 5, exp_name)
command_handler(command_member, {"RU": "мембер", "EN": "member"}, 5, exp_name)
command_handler(command_admin, {"RU": "админ", "EN": "admin"}, 6, exp_name)
command_handler(command_owner, {"RU": "овнер", "EN": "owner"}, 6, exp_name)
command_handler(command_kick, {"RU": "кик", "EN": "kick"}, 3, exp_name)
command_handler(command_visitor, {"RU": "визитор", "EN": "visitor"}, 3, exp_name)
command_handler(command_participant, {"RU": "участник", "EN": "participant"}, 3, exp_name)
command_handler(command_moder, {"RU": "модер", "EN": "moder"}, 5, exp_name)
command_handler(command_fullban, {"RU": "фулбан", "EN": "fullban"}, 7, exp_name)
command_handler(command_fullunban, {"RU": "фулунбан", "EN": "fullunban"}, 7, exp_name)
