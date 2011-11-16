# coding: utf-8

#  BlackSmith mark.2
exp_name = "user_stats" # /code.py v.x4
#  Id: 17~3a
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
				db_desc = db.fetchone()
		if db_desc:
			answer = UstatAnsBase[0] % (db_desc[3], db_desc[2], db_desc[1])
			if db_desc[3] >= 2 and db_desc[4]:
				answer += UstatAnsBase[1] % (db_desc[4], db_desc[5])
			answer += UstatAnsBase[2] % (", ".join(sorted(db_desc[6].split("-/-"))))
		else:
			answer = UstatAnsBase[3]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def command_here(ltype, source, nick, disp):
	if Chats.has_key(source[1]):
		if not nick:
			nick = source[2]
		if Chats[source[1]].isHereTS(nick):
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

def calc_stat_04eh(conf, nick, instance, role, stanza, disp):
	if instance and nick != get_self_nick(conf):
		date, filename = strTime(local = False), cefile(chat_file(conf, UstatFile))
		with UstatDesc[conf]:
			with database(filename) as db:
				db("select * from stat where jid=?", (instance,))
				db_desc = db.fetchone()
				if db_desc:
					db("update stat set joined=?, joins=? where jid=?", (date, (db_desc[3] + 1), instance))
					if nick not in db_desc[6].split("-/-"):
						db("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_desc[6], nick), instance))
					arole = "%s/%s" % (role)
					if db_desc[1] != arole:
						db("update stat set arole=? where jid=?", (arole, instance))
					db.commit()
				else:
					db("insert into stat values (?,?,?,?,?,?,?)", (instance, "%s/%s" % (role), date, 1, "", "", nick))
					db.commit()

def calc_stat_05eh(conf, nick, sbody, scode, disp):
	if nick != get_self_nick(conf):
		source_ = get_source(conf, nick)
		if source_:
			sbody = UnicodeType(sbody)
			if scode == sCodes[0]:
				sbody = "banned:(%s)" % (sbody)
			elif scode == sCodes[2]:
				sbody = "kicked:(%s)" % (sbody)
			date, filename = strTime(local = False), cefile(chat_file(conf, UstatFile))
			with UstatDesc[conf]:
				with database(filename) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						db("update stat set seen=?, leave=? where jid=?", (date, sbody, source_))
						db.commit()

def calc_stat_06eh(conf, old_nick, nick, disp):
	if nick != get_self_nick(conf):
		source_ = get_source(conf, nick)
		if source_:
			filename = cefile(chat_file(conf, UstatFile))
			with UstatDesc[conf]:
				with database(filename) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc and nick not in db_desc[6].split("-/-"):
						db("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_desc[6], nick), source_))
						db.commit()

def calc_stat_07eh(conf, nick, role, disp):
	if nick != get_self_nick(conf):
		source_ = get_source(conf, nick)
		if source_:
			filename = cefile(chat_file(conf, UstatFile))
			with UstatDesc[conf]:
				with database(filename) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						arole = "%s/%s" % (role)
						if db_desc[1] != arole:
							db("update stat set arole=? where jid=?", (arole, source_))
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

expansions[exp_name].funcs_add([command_user_stats, command_here, calc_stat_04eh, calc_stat_05eh, calc_stat_06eh, calc_stat_07eh, init_stat_base, edit_stat_desc])
expansions[exp_name].ls.extend(["UstatAnsBase", "UstatFile", "UstatDesc"])

command_handler(command_user_stats, {"RU": "юзерстат", "EN": "userstat"}, 2, exp_name)
command_handler(command_here, {"RU": "пребывание", "EN": "here"}, 1, exp_name)

handler_register(init_stat_base, "01si", exp_name)
handler_register(edit_stat_desc, "04si", exp_name)
handler_register(calc_stat_04eh, "04eh", exp_name)
handler_register(calc_stat_05eh, "05eh", exp_name)
handler_register(calc_stat_06eh, "06eh", exp_name)
handler_register(calc_stat_07eh, "07eh", exp_name)
