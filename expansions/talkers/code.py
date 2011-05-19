# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "talkers" # /code.py v.x3
#  Id: 14~2a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

TalkersFile = "talkers.db"

def command_talkers(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			list_ = body.split()
			if len(list_) >= 2:
				key2, key = body[(body.find(" ") + 1):].strip(), list_[0].lower()
				if key in ["top", "топ".decode("utf-8")]:
					if key2 in ["local", "локальный".decode("utf-8")]:
						base = sqlite3.connect(cefile(chat_file(source[1], TalkersFile)), timeout = 8)
						cu = base.cursor()
						base_data = cu.execute("select * from talkers order by -msgs").fetchmany(10)
						base.close()
						if base_data:
							answer, numb = talkers_answers[0], itypes.Number()
							for x in base_data:
								answer += "\n%d. %s\t\t%d\t%d\t%s" % (numb.plus(), x[1], x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
						else:
							answer = talkers_answers[1]
					elif key2 in ["global", "глобальный".decode("utf-8")]:
						Glob_dbs = {}
						for conf in Chats.keys():
							base = sqlite3.connect(cefile(chat_file(conf, TalkersFile)), timeout = 8)
							cu = base.cursor()
							base_data = cu.execute("select * from talkers order by -msgs").fetchmany(99)
							base.close()
							for x in base_data:
								if Glob_dbs.has_key(x[0]):
									Glob_dbs[x[0]][2] += x[2]
									Glob_dbs[x[0]][3] += x[3]
								else:
									Glob_dbs[x[0]] = list(x)
						if Glob_dbs:
							Top_list = []
							for x, y in Glob_dbs.items():
								Top_list.append([y[2], y[3], y[1]])
							del Glob_dbs
							answer, numb = talkers_answers[0], itypes.Number()
							Top_list.sort()
							Top_list.reverse()
							for x in Top_list:
								answer += "\n%d. %s\t\t%d\t%d\t%s" % (numb.plus(), x[2], x[0], x[1], str(round((float(x[1]) / x[0]), 1)))
								if numb._int() >= 20:
									break
						else:
							answer = talkers_answers[1]
					else:
						answer = AnsBase[2]
				elif key in ["global", "глобальный".decode("utf-8")]:
					if key2 in ["my", "мой".decode("utf-8")]:
						source_ = get_source(source[1], source[2])
						if source_:
							x, y = 0, 0
							for conf in Chats.keys():
								base = sqlite3.connect(cefile(chat_file(conf, TalkersFile)), timeout = 8)
								cu = base.cursor()
								base_data = cu.execute("select * from talkers where jid=?", (source_,)).fetchone()
								base.close()
								if base_data:
									x += base_data[2]
									y += base_data[3]
							if x:
								answer = talkers_answers[2] % (x, y, str(round((float(y) / x), 1)))
							else:
								answer = talkers_answers[1]
						else:
							answer = talkers_answers[1]
					else:
						if Chats[source[1]].isHere(key2):
							source_ = get_source(source[1], key2)
						else:
							source_ = list_[1].lower()
							if not (source_.count("@") and source_.count(".")):
								source_ = None
						if source_:
							base = sqlite3.connect(cefile(chat_file(source[1], TalkersFile)), timeout = 8)
							cu = base.cursor()
							x = cu.execute("select * from talkers where jid=?", (source_,)).fetchone()
							base.close()
							if x:
								answer = talkers_answers[2] % (x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
							else:
								answer = talkers_answers[1]
						else:
							Glob_dbs = {}
							for conf in Chats.keys():
								base = sqlite3.connect(cefile(chat_file(conf, TalkersFile)), timeout = 8)
								cu = base.cursor()
								base_data = cu.execute("select * from talkers where (jid like ? or lastnick like ?) order by -msgs", (key2, key2)).fetchmany(10)
								base.close()
								for x in base_data:
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
								answer, numb = talkers_answers[0], itypes.Number()
								Usr_list.sort()
								Usr_list.reverse()
								for x in Usr_list:
									answer += "\n%d. %s\t\t%d\t%d\t%s" % (numb.plus(), x[2], x[0], x[1], str(round((float(x[1]) / x[0]), 1)))
									if numb._int() >= 10:
										break
								answer += talkers_answers[3]
							else:
								answer = talkers_answers[1]
				elif key in ["local", "локальный".decode("utf-8")]:
					if key2 in ["my", "мой".decode("utf-8")]:
						source_ = get_source(source[1], source[2])
						if source_:
							base = sqlite3.connect(cefile(chat_file(source[1], TalkersFile)), timeout = 8)
							cu = base.cursor()
							x = cu.execute("select * from talkers where jid=?", (source_,)).fetchone()
							base.close()
							if x:
								answer = talkers_answers[2] % (x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
							else:
								answer = talkers_answers[1]
						else:
							answer = talkers_answers[1]
					else:
						if Chats[source[1]].isHere(key2):
							source_ = get_source(source[1], key2)
						else:
							source_ = list_[1].lower()
							if not (source_.count("@") and source_.count(".")):
								source_ = None
						if source_:
							base = sqlite3.connect(cefile(chat_file(source[1], TalkersFile)), timeout = 8)
							cu = base.cursor()
							x = cu.execute("select * from talkers where jid=?", (source_,)).fetchone()
							base.close()
							if x:
								answer = talkers_answers[2] % (x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
							else:
								answer = talkers_answers[1]
						else:
							base = sqlite3.connect(cefile(chat_file(source[1], TalkersFile)), timeout = 8)
							cu = base.cursor()
							base_data = cu.execute("select * from talkers where (jid like ? or lastnick like ?) order by -msgs", (key2, key2)).fetchmany(10)
							base.close()
							if base_data:
								answer, numb = talkers_answers[0], itypes.Number()
								for x in base_data:
									answer += "\n%d. %s\t\t%d\t%d\t%s" % (numb.plus(), x[1], x[2], x[3], str(round((float(x[3]) / x[2]), 1)))
								answer += talkers_answers[3]
							else:
								answer = talkers_answers[1]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def calculate_talkers(stanza, isConf, ltype, source, body, isToBs, disp):
	if ltype == Types[1] and source[2]:
		source_ = get_source(source[1], source[2])
		if source_:
			nick = source[2].strip()
			base = sqlite3.connect(cefile(chat_file(source[1], TalkersFile)), timeout = 8)
			cu = base.cursor()
			db_data = cu.execute("select * from talkers where jid=?", (source_,)).fetchone()
			if db_data:
				cu.execute("update talkers set lastnick=?, msgs=?, words=? where jid=?", (nick, (db_data[2] + 1), (db_data[3] + len(body.split())), source_))
			else:
				cu.execute("insert into talkers values (?,?,?,?)", (source_, nick, 1, len(body.split())))
			base.commit()
			base.close()

def init_talkers_base(conf):
	db_file = cefile(chat_file(conf, TalkersFile))
	if not os.path.isfile(db_file):
		base = sqlite3.connect(db_file)
		cu = base.cursor()
		cu.execute("create table talkers (jid text, lastnick text, msgs integer, words integer)")
		base.commit()
		base.close()

expansions[exp_name].funcs_add([command_talkers, calculate_talkers, init_talkers_base])
expansions[exp_name].ls.extend(["talkers_answers", "TalkersFile"])

command_handler(command_talkers, {"RU": "трёп", "EN": "talkers"}, 2, exp_name)

handler_register(init_talkers_base, "01si", exp_name)
handler_register(calculate_talkers, "01eh", exp_name)
