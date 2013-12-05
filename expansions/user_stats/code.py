# coding: utf-8

#  BlackSmith mark.2
# exp_name = "user_stats" # /code.py v.x7
#  Id: 17~6c
#  Code © (2010-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		check_sqlite()
		expansion.__init__(self, name)

	UstatsFile = "jstat.db"

	UstatsDesc = {}

	db = lambda self, conf: database(cefile(chat_file(conf, self.UstatsFile)), self.UstatsDesc[conf])

	def command_user_stats(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if not body:
				body = get_source(source[1], source[2])
			elif Chats[source[1]].isHere(body):
				body = get_source(source[1], body)
			with self.db(source[1]) as db:
				db("select * from stat where jid=?", (body,))
				db_desc = db.fetchone()
			if db_desc:
				answer = self.AnsBase[0] % (db_desc[3], db_desc[2], db_desc[1])
				if db_desc[3] >= 2 and db_desc[4]:
					answer += self.AnsBase[1] % (db_desc[4], db_desc[5])
				answer += self.AnsBase[2] % (", ".join(sorted(db_desc[6].split("-/-"))))
			else:
				answer = self.AnsBase[3]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	def command_here(self, stype, source, nick, disp):
		if Chats.has_key(source[1]):
			if not nick:
				nick = source[2]
			if Chats[source[1]].isHereTS(nick):
				jtc = Time2Text(time.time() - Chats[source[1]].get_user(nick).date[0])
				if nick != source[2]:
					answer = self.AnsBase[4] % (nick, jtc)
				else:
					answer = self.AnsBase[5] % (jtc)
			else:
				answer = self.AnsBase[6]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	def calc_stat_04eh(self, conf, nick, instance, role, stanza, disp):
		if instance and nick != get_nick(conf):
			date = strfTime(local = False)
			with self.db(conf) as db:
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

	def calc_stat_05eh(self, conf, nick, sbody, scode, disp):
		if nick != get_nick(conf):
			source_ = get_source(conf, nick)
			if source_:
				sbody = str(sbody)
				if scode == sCodes[0]:
					sbody = "banned:(%s)" % (sbody)
				elif scode == sCodes[2]:
					sbody = "kicked:(%s)" % (sbody)
				date = strfTime(local = False)
				with self.db(conf) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						db("update stat set seen=?, leave=? where jid=?", (date, sbody, source_))
						db.commit()

	def calc_stat_06eh(self, conf, old_nick, nick, disp):
		if nick != get_nick(conf):
			source_ = get_source(conf, nick)
			if source_:
				with self.db(conf) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc and nick not in db_desc[6].split("-/-"):
						db("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_desc[6], nick), source_))
						db.commit()

	def calc_stat_07eh(self, conf, nick, role, disp):
		if nick != get_nick(conf):
			source_ = get_source(conf, nick)
			if source_:
				with self.db(conf) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						arole = "%s/%s" % (role)
						if db_desc[1] != arole:
							db("update stat set arole=? where jid=?", (arole, source_))
							db.commit()

	def init_stat_base(self, conf):
		filename = cefile(chat_file(conf, self.UstatsFile))
		if not os.path.isfile(filename):
			with database(filename) as db:
				db("create table stat (jid text, arole text, joined text, joins integer, seen text, leave text, nicks text)")
				db.commit()
		self.UstatsDesc[conf] = ithr.Semaphore()

	def edit_stat_desc(self, conf):
		del self.UstatsDesc[conf]

	commands = (
		(command_user_stats, "userstat", 2,),
		(command_here, "here", 1,)
	)

	handlers = (
		(init_stat_base, "01si"),
		(edit_stat_desc, "04si"),
		(calc_stat_04eh, "04eh"),
		(calc_stat_05eh, "05eh"),
		(calc_stat_06eh, "06eh"),
		(calc_stat_07eh, "07eh")
	)
