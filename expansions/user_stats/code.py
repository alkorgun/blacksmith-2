# coding: utf-8

#  BlackSmith mark.2
exp_name = "user_stats" # /code.py v.x3
#  Id: 17~2a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

UstatFile = "jstat.db"

UstatDesc = {}

def command_user_stats(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if not body:
			body = get_source(source[1], source[2])
		elif Chats[source[1]].isHere(body):
			body = get_source(source[1], body)
		filename = cefile(chat_file(source[1], UstatFile))
		with UstatDesc[source[1]]:
			with database(filename) as db:
				db("select * from stat where jid=?", (body,))
				x = db.fetchone()
		if x:
			answer = UstatAnsBase[0] % (x[3], x[2], x[1])
			if x[3] >= 2 and x[4]:
				answer += UstatAnsBase[1] % (x[4], x[5])
			answer += UstatAnsBase[2] % (", ".join(sorted(x[6].split("-/-"))))
		else:
			answer = UstatAnsBase[3]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def command_here(ltype, source, nick, disp):
	if Chats.has_key(source[1]):
		if not nick:
			nick = source[2]
		if Chats[source[1]].isHereNow(nick):
			jtc = Time2Text(time.time() - Chats[source[1]].get_user(nick).date[0])
			if nick != source[2]:
				answer = UstatAnsBase[4] % (nick, jtc)
			else:
				answer = UstatAnsBase[5] % (jtc)
		else:
			answer = UstatAnsBase[6]
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
					nick = UnicodeType(nick).strip()
					filename = cefile(chat_file(conf, UstatFile))
					with UstatDesc[conf]:
						with database(filename) as db:
							db("select * from stat where jid=?", (instance,))
							db_desc = db.fetchone()
							if db_desc and nick not in db_desc[6].split("-/-"):
								db("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_desc[6], nick), instance))
								db.commit()
		else:
			sUser = Chats[conf].get_user(nick)
			if sUser.source:
				filename = cefile(chat_file(conf, UstatFile))
				with UstatDesc[conf]:
					with database(filename) as db:
						db("select * from stat where jid=?", (sUser.source,))
						db_desc = db.fetchone()
						if db_desc:
							if stype == Types[4]:
								scode = stanza.getStatusCode()
								if scode == sCodes[0]:
									status = "banned:(%s)" % UnicodeType(stanza.getReason())
								elif scode == sCodes[2]:
									status = "kicked:(%s)" % UnicodeType(stanza.getReason())
								else:
									status = UnicodeType(stanza.getStatus())
								db("update stat set seen=?, leave=? where jid=?", (strTime(local = False), status, sUser.source))
							elif stype in [Types[3], None]:
								if (time.time() - sUser.date[0]) <= 0.8:
									db("update stat set joined=?, joins=? where jid=?", (sUser.date[2], (db_desc[3] + 1), sUser.source))
									nick = nick.strip()
									if nick not in db_desc[6].split("-/-"):
										db("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_desc[6], nick), sUser.source))
								arole = "%s/%s" % (sUser.role)
								if db_desc[1] != arole:
									db("update stat set arole=? where jid=?", (arole, sUser.source))
						else:
							db("insert into stat values (?,?,?,?,?,?,?)", (sUser.source, "%s/%s" % (sUser.role), sUser.date[2], 1, "", "", nick))
						db.commit()

def init_stat_base(conf):
	filename = cefile(chat_file(conf, UstatFile))
	if not os.path.isfile(filename):
		with database(filename) as db:
			db("create table stat (jid text, arole text, joined text, joins integer, seen text, leave text, nicks text)")
			db.commit()
	UstatDesc[conf] = iThr.Semaphore()

def edit_stat_desc(conf):
	del UstatDesc[conf]

expansions[exp_name].funcs_add([command_user_stats, command_here, calc_user_stat, init_stat_base, edit_stat_desc])
expansions[exp_name].ls.extend(["UstatAnsBase", "UstatFile", "UstatDesc"])

command_handler(command_user_stats, {"RU": "юзерстат", "EN": "userstat"}, 2, exp_name)
command_handler(command_here, {"RU": "пребывание", "EN": "here"}, 1, exp_name)

handler_register(init_stat_base, "01si", exp_name)
handler_register(edit_stat_desc, "04si", exp_name)
handler_register(calc_user_stat, "02eh", exp_name)
