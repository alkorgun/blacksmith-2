# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "user_stats" # /code.py v.x3
#  Id: 17~2a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

StatFile = "jstat.db"

def command_user_stats(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if not body:
			body = get_source(source[1], source[2])
		elif Chats[source[1]].isHere(body):
			body = get_source(source[1], body)
		base = sqlite3.connect(cefile(chat_file(source[1], StatFile)), timeout = 8)
		cu = base.cursor()
		x = cu.execute("select * from stat where jid=?", (body,)).fetchone()
		base.close()
		if x:
			answer = user_stat_answers[0] % (x[3], x[2], x[1])
			if x[3] >= 2 and x[4]:
				answer += user_stat_answers[1] % (x[4], x[5])
			answer += user_stat_answers[2] % (", ".join(sorted(x[6].split("-/-"))))
		else:
			answer = user_stat_answers[3]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def command_here(ltype, source, nick, disp):
	if Chats.has_key(source[1]):
		if not nick:
			nick = source[2]
		if Chats[source[1]].isHereNow(nick):
			jtc = timeElapsed(time.time() - Chats[source[1]].get_user(nick).dates[0])
			if nick != source[2]:
				answer = user_stat_answers[4] % (nick, jtc)
			else:
				answer = user_stat_answers[5] % (jtc)
		else:
			answer = user_stat_answers[6]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def calc_user_stat(stanza, disp):
	(source, conf, stype, nick) = sAttrs(stanza)
	if stype != Types[7] and nick != get_self_nick(conf):
		if not Chats[conf].isHere(nick):
			if stype == Types[4] and sCodes[1] == stanza.getStatusCode():
				nick = stanza.getNick()
				instance = get_source(conf, nick)
				if instance:
					base = sqlite3.connect(cefile(chat_file(conf, StatFile)), timeout = 8)
					cu = base.cursor()
					db_data = cu.execute("select * from stat where jid=?", (instance,)).fetchone()
					nick = nick.strip()
					if db_data and nick not in db_data[6].split("-/-"):
						cu.execute("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_data[6], nick), instance))
						base.commit()
					base.close()
		else:
			sUser = Chats[conf].get_user(nick)
			if sUser.source:
				base = sqlite3.connect(cefile(chat_file(conf, StatFile)), timeout = 8)
				cu = base.cursor()
				db_data = cu.execute("select * from stat where jid=?", (sUser.source,)).fetchone()
				if db_data:
					if stype == Types[4]:
						scode = stanza.getStatusCode()
						if scode == sCodes[1]:
							nick = (stanza.getNick()).strip()
							if nick not in db_data[6].split("-/-"):
								cu.execute("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_data[6], nick), sUser.source))
						else:
							status = (stanza.getReason() or stanza.getStatus() or "None")
							if scode == sCodes[0]:
								status = "ban:(%s)" % (status)
							elif scode == sCodes[2]:
								status = "kick:(%s)" % (status)
							cu.execute("update stat set seen=?, leave=? where jid=?", (strTime(local = False), status, sUser.source))
					elif stype in [Types[3], None]:
						if (time.time() - sUser.dates[0]) <= 0.8:
							cu.execute("update stat set joined=?, joins=? where jid=?", (sUser.dates[2], (db_data[3] + 1), sUser.source))
							nick = nick.strip()
							if nick not in db_data[6].split("-/-"):
								cu.execute("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_data[6], nick), sUser.source))
						arole = "%s/%s" % (sUser.afl, sUser.role)
						if db_data[1] != arole:
							cu.execute("update stat set arole=? where jid=?", (arole, sUser.source))
				else:
					cu.execute("insert into stat values (?,?,?,?,?,?,?)", (sUser.source, "%s/%s" % (sUser.afl, sUser.role), sUser.dates[2], 1, "", "", nick))
				base.commit()
				base.close()

def init_stat_base(conf):
	db_file = cefile(chat_file(conf, StatFile))
	if not os.path.isfile(db_file):
		base = sqlite3.connect(db_file)
		cu = base.cursor()
		cu.execute("create table stat (jid text, arole text, joined text, joins integer, seen text, leave text, nicks text)")
		base.commit()
		base.close()

expansions[exp_name].funcs_add([command_user_stats, command_here, calc_user_stat, init_stat_base])
expansions[exp_name].ls.extend(["user_stat_answers", "StatFile"])

command_handler(command_user_stats, {"RU": "юзерстат", "EN": "userstat"}, 2, exp_name)
command_handler(command_here, {"RU": "пребывание", "EN": "here"}, 1, exp_name)

handler_register(init_stat_base, "01si", exp_name)
handler_register(calc_user_stat, "02eh", exp_name)
