# coding: utf-8

#  BlackSmith mark.2
exp_name = "talkers" # /code.py v.x5
#  Id: 14~4b
#  Code © (2010-2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	TalkersFile = "talkers.db"

	TalkersDesc = {}

	def command_talkers(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				ls = body.split()
				if len(ls) >= 2:
					a1 = (ls.pop(0)).lower()
					if a1 in ("top", "топ".decode("utf-8")):
						a2 = (ls.pop(0)).lower()
						if ls and isNumber(ls[0]):
							Number = int(ls.pop(0))
							if Number > 256:
								Number = 256
						else:
							Number = 0
						if a2 in ("local", "локальный".decode("utf-8")):
							filename = cefile(chat_file(source[1], self.TalkersFile))
							with self.TalkersDesc[source[1]]:
								with database(filename) as db:
									db("select * from talkers order by -msgs")
									db_desc = db.fetchmany(Number if Number > 0 else 10)
							if db_desc:
								answer, Numb = self.AnsBase[0], itypes.Number()
								for x in db_desc:
									answer += "\n%d. %s\t\t%d\t%d\t%s" % (Numb.plus(), x[1], x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
							else:
								answer = self.AnsBase[1]
						elif a2 in ("global", "глобальный".decode("utf-8")):
							Glob_dbs = {}
							for conf in Chats.keys():
								filename = cefile(chat_file(conf, self.TalkersFile))
								with self.TalkersDesc[conf]:
									with database(filename) as db:
										db("select * from talkers order by -msgs")
										db_desc = db.fetchmany(256)
								for x in db_desc:
									if Glob_dbs.has_key(x[0]):
										Glob_dbs[x[0]][2] += x[2]
										Glob_dbs[x[0]][3] += x[3]
									else:
										Glob_dbs[x[0]] = list(x)
							if Glob_dbs:
								Top_list, limit = [], (Number if Number > 0 else 20)
								for x, y in Glob_dbs.items():
									Top_list.append([y[2], y[3], y[1]])
								del Glob_dbs
								answer, Numb = self.AnsBase[0], itypes.Number()
								Top_list.sort()
								Top_list.reverse()
								for x in Top_list:
									answer += "\n%d. %s\t\t%d\t%d\t%s" % (Numb.plus(), x[2], x[0], x[1], str(round((float(x[1]) / x[0]), 1)))
									if Numb._int() >= limit:
										break
							else:
								answer = self.AnsBase[1]
						else:
							answer = AnsBase[2]
					elif a1 in ("global", "глобальный".decode("utf-8")):
						a2 = body[((body.lower()).find(a1) + len(a1)):].strip()

						def get_talker_stats(source_):
							x, y = 0, 0
							for conf in Chats.keys():
								filename = cefile(chat_file(conf, self.TalkersFile))
								with self.TalkersDesc[conf]:
									with database(filename) as db:
										db("select * from talkers where jid=?", (source_,))
										db_desc = db.fetchone()
								if db_desc:
									x += db_desc[2]
									y += db_desc[3]
							if x:
								answer = self.AnsBase[2] % (x, y, str(round((float(y) / x), 1)))
							else:
								answer = self.AnsBase[1]
							return answer

						if a2 in ("mine", "мой".decode("utf-8")):
							source_ = get_source(source[1], source[2])
							if source_:
								answer = get_talker_stats(source_)
							else:
								answer = self.AnsBase[1]
						else:
							if Chats[source[1]].isHere(a2):
								source_ = get_source(source[1], a2)
							else:
								source_ = (ls.pop(0)).lower()
								if not isSource(source_):
									source_ = None
							if source_:
								answer = get_talker_stats(source_)
							else:
								Glob_dbs = {}
								for conf in Chats.keys():
									filename = cefile(chat_file(conf, self.TalkersFile))
									with self.TalkersDesc[conf]:
										with database(filename) as db:
											db("select * from talkers where (jid like ? or lastnick like ?) order by -msgs", (a2, a2))
											db_desc = db.fetchmany(10)
									for x in db_desc:
										if Glob_dbs.has_key(x[0]):
											Glob_dbs[x[0]][2] += x[2]
											Glob_dbs[x[0]][3] += x[3]
										else:
											Glob_dbs[x[0]] = x
								if Glob_dbs:
									Usr_list = []
									for x, y in Glob_dbs.items():
										Usr_list.append([y[2], y[3], y[1]])
									del Glob_dbs
									answer, Numb = self.AnsBase[0], itypes.Number()
									Usr_list.sort()
									Usr_list.reverse()
									for x in Usr_list:
										answer += "\n%d. %s\t\t%d\t%d\t%s" % (Numb.plus(), x[2], x[0], x[1], str(round((float(x[1]) / x[0]), 1)))
										if Numb._int() >= 10:
											break
									answer += self.AnsBase[3]
								else:
									answer = self.AnsBase[1]
					elif a1 in ("local", "локальный".decode("utf-8")):
						a2 = body[((body.lower()).find(a1) + len(a1)):].strip()

						def get_talker_stats(source_, conf):
							filename = cefile(chat_file(conf, self.TalkersFile))
							with self.TalkersDesc[conf]:
								with database(filename) as db:
									db("select * from talkers where jid=?", (source_,))
									x = db.fetchone()
							if x:
								answer = self.AnsBase[2] % (x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
							else:
								answer = self.AnsBase[1]
							return answer

						if a2 in ("mine", "мой".decode("utf-8")):
							source_ = get_source(source[1], source[2])
							if source_:
								answer = get_talker_stats(source_, source[1])
							else:
								answer = self.AnsBase[1]
						else:
							if Chats[source[1]].isHere(a2):
								source_ = get_source(source[1], a2)
							else:
								source_ = (ls.pop(0)).lower()
								if not isSource(source_):
									source_ = None
							if source_:
								answer = get_talker_stats(source_, source[1])
							else:
								filename = cefile(chat_file(source[1], self.TalkersFile))
								with self.TalkersDesc[source[1]]:
									with database(filename) as db:
										db("select * from talkers where (jid like ? or lastnick like ?) order by -msgs", (a2, a2))
										db_desc = db.fetchmany(10)
								if db_desc:
									answer, Numb = self.AnsBase[0], itypes.Number()
									for x in db_desc:
										answer += "\n%d. %s\t\t%d\t%d\t%s" % (Numb.plus(), x[1], x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
									answer += self.AnsBase[3]
								else:
									answer = self.AnsBase[1]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	def calculate_talkers(self, stanza, isConf, ltype, source, body, isToBs, disp):
		if isConf and ltype == Types[1] and source[2]:
			source_ = get_source(source[1], source[2])
			if source_:
				nick = source[2].strip()
				filename = cefile(chat_file(source[1], self.TalkersFile))
				with self.TalkersDesc[source[1]]:
					with database(filename) as db:
						db("select * from talkers where jid=?", (source_,))
						db_desc = db.fetchone()
						if db_desc:
							db("update talkers set lastnick=?, msgs=?, words=? where jid=?", (nick, (db_desc[2] + 1), (db_desc[3] + len(body.split())), source_))
						else:
							db("insert into talkers values (?,?,?,?)", (source_, nick, 1, len(body.split())))
						db.commit()

	def init_talkers_base(self, conf):
		filename = cefile(chat_file(conf, self.TalkersFile))
		if not os.path.isfile(filename):
			with database(filename) as db:
				db("create table talkers (jid text, lastnick text, msgs integer, words integer)")
				db.commit()
		self.TalkersDesc[conf] = iThr.Semaphore()

	def edit_talkers_desc(self, conf):
		del self.TalkersDesc[conf]

	commands = ((command_talkers, "talkers", 2,),)

	handlers = (
		(init_talkers_base, "01si"),
		(edit_talkers_desc, "04si"),
		(calculate_talkers, "01eh")
					)
