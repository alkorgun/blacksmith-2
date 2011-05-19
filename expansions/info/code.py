# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "info" # /code.py v.x2
#  Id: 11~1a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_online(ltype, source, body, disp):
	list, col, ThrIds = info_answers[7], itypes.Number(), iThr.ThrNames()
	for disp_ in sorted(InstansesDesc.keys()):
		connect, alive = online(disp_), str("%s%s" % (Types[13], disp_) in ThrIds)
		if not connect:
			connect = False
		list += "\n%d) %s - %s - %s" % (col.plus(), disp_, str(connect), alive)
	if ltype == Types[1]:
		Answer(AnsBase[11], ltype, source, disp)
	Msend(source[0], list, disp)

def command_inchat(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		list, col, acc = info_answers[8], itypes.Number(), enough_access(source[1], source[2], 4)
		owners, admins, members, none = [], [], [], []
		for nick in Chats[source[1]].sorted_users():
			if nick.ishere:
				text = nick.nick
				if acc and nick.source:
					text += " (%s)" % (nick.source)
				if nick.afl == AflRoles[5]:
					owners.append(text)
				elif nick.afl == AflRoles[4]:
					admins.append(text)
				elif nick.afl == AflRoles[3]:
					members.append(text)
				else:
					none.append(text)
		if owners:
			list += "\n\nOwners:"
			for x in owners:
				list += "\n%d) %s" % (col.plus(), x)
		if admins:
			list += "\n\nAdmins:"
			for x in admins:
				list += "\n%d) %s" % (col.plus(), x)
		if members:
			list += "\n\nMembers:"
			for x in members:
				list += "\n%d) %s" % (col.plus(), x)
		if none:
			list += "\n\nOthers:"
			for x in none:
				list += "\n%d) %s" % (col.plus(), x)
		if ltype == Types[1]:
			Answer(AnsBase[11], ltype, source, disp)
		Msend(source[0], list, disp)
	else:
		Answer(AnsBase[0], ltype, source, disp)

def command_conflist(ltype, source, body, disp):
	answer, col, admin = info_answers[5], itypes.Number(), enough_access(source[1], source[2], 7)
	for conf in sorted(Chats.keys()):
		BsNick = get_self_nick(conf)
		ismoder = str(Chats[conf].ismoder)
		ConfName = conf.split("@")[0]
		disp_ = (Chats[conf].disp if admin else "***")
		cPref = str(Chats[conf].cPref)
		online = itypes.Number()
		for nick in Chats[conf].get_users():
			if nick.ishere:
				online.plus()
		answer += '\n%d) %s/%s [%s] "%s" (%s) - %s' % (col.plus(), ConfName, BsNick, disp_, cPref, online._str(), ismoder)
	if col._int():
		if ltype == Types[1]:
			Answer(AnsBase[11], ltype, source, disp)
		Msend(source[0], answer, disp)
	else:
		Answer(info_answers[6], ltype, source, disp)

def command_visitors(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			action = body.lower()
		else:
			action = "default"
		if action in ["today", "сегодня".decode("utf-8")]:
			date = today()[1]
			list = ""
			col = itypes.Number()
			col2 = itypes.Number()
			for nick in Chats[source[1]].sorted_users():
				if not nick.ishere:
					if nick.dates[1] == date:
						if nick.source:
							list += "\n%d. %s (%s)" % (col.plus(), nick.nick, nick.source)
						else:
							list += "\n%d. %s" % (col.plus(), nick.nick)
				else:
					col2.plus()
			if col._int():
				if ltype == Types[1]:
					Answer(AnsBase[11], ltype, source, disp)
				Msend(source[0], info_answers[0] % (col._str(), list, col2._str()), disp)
			else:
				Answer(info_answers[1], ltype, source, disp)
		elif action in ["dates", "даты".decode("utf-8")]:
			list = ""
			col = itypes.Number()
			for nick in Chats[source[1]].sorted_users():
				list += "\n%d. %s\t\t%s" % (col.plus(), nick.nick, nick.dates[2])
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			Msend(source[0], info_answers[2] % (col._str(), list), disp)
		elif action in ["list", "лист".decode("utf-8")]:
			list = Chats[source[1]].get_nicks()
			text = ", ".join(sorted(list))
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			Msend(source[0], info_answers[2] % (str(len(list)), text), disp)
		else:
			list = ""
			col = itypes.Number()
			col2 = itypes.Number()
			for nick in Chats[source[1]].sorted_users():
				if not nick.ishere:
					if nick.source:
						list += "\n%d. %s (%s)" % (col.plus(), nick.nick, nick.source)
					else:
						list += "\n%d. %s" % (col.plus(), nick.nick)
				else:
					col2.plus()
			if col._int():
				if ltype == Types[1]:
					Answer(AnsBase[11], ltype, source, disp)
				Msend(source[0], info_answers[3] % (col._str(), list, col2._str()), disp)
			else:
				Answer(info_answers[4], ltype, source, disp)
	else:
		Answer(AnsBase[0], ltype, source, disp)

def command_where(ltype, source, body, disp):
	if body:
		acc = enough_access(source[1], source[2], 7)
		list, col = "", itypes.Number()
		for conf in sorted(Chats.keys()):
			for nick in sorted(Chats[conf].get_nicks()):
				if Chats[conf].isHereNow(nick):
					jid = get_source(conf, nick)
					if nick.count(body) or (jid and jid.count(body)):
						list += "\n%d) %s (%s)" % (col.plus(), nick, conf)
						if jid and acc:
							list += " [%s]" % (jid)
						if col._int() >= 20:
							break
		if col._int():
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			Msend(source[0], info_answers[9] % (col._str(), list), disp)
		else:
			answer = info_answers[10]
	else:
		answer = AnsBase[1]
	if locals().has_key(Types[23]):
		Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_online, command_inchat, command_conflist, command_visitors, command_where])
expansions[exp_name].ls.extend(["info_answers"])

command_handler(command_online, {"RU": "онлайн", "EN": "online"}, 7, exp_name)
command_handler(command_inchat, {"RU": "инмук", "EN": "inmuc"}, 2, exp_name)
command_handler(command_conflist, {"RU": "чатлист", "EN": "chatslist"}, 5, exp_name)
command_handler(command_visitors, {"RU": "ктобыл", "EN": "visitors"}, 4, exp_name)
command_handler(command_where, {"RU": "где", "EN": "where"}, 2, exp_name)
