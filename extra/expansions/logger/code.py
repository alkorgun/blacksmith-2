# coding: utf-8

#  BlackSmith mark.2
# exp_name = "logger" # /code.py v.x11
#  Id: 30~11c
#  Code © (2011-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		check_sqlite()
		expansion.__init__(self, name)

	On = True

	RootDir = "chatlogs"
	ConfigFile = dynamic % ("logger.db")
	ChatConfigFile = "logger.db"
	ChatsCache = "ChatsCache.dict"
	ChatsPasswords = "ChatsPasswords.dict"

	loggerDesc = {}
	leaveModes = {sCodes[2]: 9, sCodes[0]: 10}

	escapeTabs = lambda self, body: sub_desc(body, ((chr(10), "<br>"), (chr(9), "&#9;")))

	compile_link = compile__("((?:http[s]?|ftp|svn)://[^\s'\"@<>]+)")
	compile_chat = compile__("([^\s]+?@(?:conference|muc|conf|chat|group)\.[\w-]+?\.[\.\w-]+)")

	sub_link = lambda self, obj: "<a href=\"{0}\">{0}</a>".format(obj.group(1))
	sub_chat = lambda self, obj: "<a href=\"xmpp:{0}?join\">{0}</a>".format(obj.group(1))

	def sub_adds(self, body):
		body = xmpp.XMLescape(body)
		body = self.compile_chat.sub(self.sub_chat, body)
		body = self.compile_link.sub(self.sub_link, body)
		return body

	def addEvent(self, chat, nick, jid, data, mode):
		gt = time.gmtime()
		year, month, day = tuple(gt)[:3]
		st = time.strftime("%H:%M:%S", gt)
		with self.loggerDesc[chat]:
			with database(ChatsAttrs[chat]["ldir"]) as db:
				db("insert into chatlogs values (?,?,?,?,?,?,?,?)", (year, month, day, st, nick, jid, self.escapeTabs(data), mode))
				db.commit()

	enabled = lambda self, chat: self.On and (chat in self.loggerDesc)

	def logger_01eh(self, stanza, isConf, stype, source, body, isToBs, disp):
		if self.enabled(source[1]) and isConf and stype == sBase[1] and not isToBs and source[2]:
			instance = get_source(source[1], source[2]) or None
			nick = source[2].strip()
			if body.startswith("/me") and len(body) > 3:
				body = body[3:].lstrip()
				mode = 2
			else:
				mode = 1
			self.addEvent(source[1], nick, instance, self.sub_adds(body), mode)

	def logger_09eh(self, chat, nick, subject, body, disp):
		if self.enabled(chat):
			if nick:
				body = "%s set subject:\n%s" % (nick.strip(), subject.strip())
			self.addEvent(chat, None, None, self.sub_adds(body), 3)

	def logger_04eh(self, chat, nick, instance, role, stanza, disp):
		if self.enabled(chat) and nick != get_nick(chat):
			if not instance:
				instance = None
			nick = nick.strip()
			self.addEvent(chat, nick, instance, ("%s/%s" % role), 4)

	def logger_05eh(self, chat, nick, status, scode, disp):
		if self.enabled(chat) and nick != get_nick(chat):
			instance = get_source(chat, nick) or None
			nick = nick.strip()
			mode = self.leaveModes.get(scode, 5)
			self.addEvent(chat, nick, instance, xmpp.XMLescape(object_encode(status).strip()), mode)

	def logger_06eh(self, chat, old_nick, nick, disp):
		if self.enabled(chat) and nick != get_nick(chat):
			instance = get_source(chat, nick) or None
			old_nick = old_nick.strip()
			self.addEvent(chat, old_nick, instance, xmpp.XMLescape(nick.strip()), 6)

	def logger_07eh(self, chat, nick, role, disp):
		if self.enabled(chat) and nick != get_nick(chat):
			instance = get_source(chat, nick) or None
			nick = nick.strip()
			self.addEvent(chat, nick, instance, ("%s/%s" % role), 7)

	def logger_08eh(self, chat, nick, stanza, disp):
		if self.enabled(chat) and nick != get_nick(chat):
			instance = get_source(chat, nick) or None
			nick = nick.strip()
			show = stanza.getShow()
			body = stanza.getStatus()
			if body:
				body = "%s (%s)" % ((show or sList[2]), xmpp.XMLescape(body.strip()))
			else:
				body = (show or sList[2])
			self.addEvent(chat, nick, instance, body, 8)

	import fb2

	unescapeTabs = lambda self, body: sub_desc(body, (("<br>", chr(10)), ("&#9;", chr(9))))

	compile_href = compile__("<a href=\".+?\">((?:http[s]?|ftp|svn)://[^\s'\"<>]+)</a>")

	sub_href = lambda self, obj: obj.group(1)

	unescape = lambda self, data: self.fb2.sub_ehtmls(self.compile_href.sub(self.sub_href, self.unescapeTabs(data)))

	def command_logs(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if self.On:
				if self.loggerDesc.has_key(source[1]):
					body = body.split()
					if len(body) == 4:
						year, month, day, hour = body
						if all((isNumber(year), isNumber(month), isNumber(day), isNumber(hour))):
							hour = int(hour)
							if -1 < hour < 24:
								year, month, day, hour = int(year), int(month), int(day), "{0:02}".format(hour)
								with self.loggerDesc[source[1]]:
									with database(ChatsAttrs[source[1]]["ldir"]) as db:
										db("select * from chatlogs where year=? and month=? and day=? order by -time", (year, month, day))
										logs = db.fetchall()
								if logs:
									ls = []
									while logs:
										year, month, day, time, nick, jid, data, mode = logs.pop()
										if not time.startswith(hour):
											continue
										if mode == 1:
											line = "[%(time)s] <%(nick)s> %(data)s"
										elif mode == 2:
											line = "[%(time)s] *%(nick)s %(data)s"
										elif mode == 3:
											line = "[%(time)s] *** %(data)s"
										elif mode == 4:
											line = "[%(time)s] *** %(nick)s joined conference as %(data)s"
										elif mode == 5:
											line = "[%(time)s] *** %(nick)s leaved conference (%(data)s)"
										elif mode == 6:
											line = "[%(time)s] *** %(nick)s changed nick to %(data)s"
										elif mode == 7:
											line = "[%(time)s] *** %(nick)s became %(data)s"
										elif mode == 8:
											line = "[%(time)s] *** %(nick)s changed status to %(data)s"
										elif mode == 9:
											line = "[%(time)s] *** %(nick)s was kicked"
											if data:
												line += " (%(data)s)"
										else:
											line = "[%(time)s] *** %(nick)s was banned"
											if data:
												line += " (%(data)s)"
										if data:
											data = self.unescape(data)
										ls.append(line % vars())
									if ls:
										answer = str.join(chr(10), ls)
										if stype == sBase[1]:
											Message(source[0], answer, disp)
											answer = AnsBase[11]
									else:
										answer = self.AnsBase[3]
								else:
									answer = self.AnsBase[3]
							else:
								answer = AnsBase[2]
						else:
							answer = AnsBase[30]
					else:
						answer = AnsBase[2 if body else 1]
				else:
					answer = self.AnsBase[0]
			else:
				answer = self.AnsBase[2]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	def setPassword(self, chat, password = None):
		filename = os.path.join(self.RootDir, self.ChatsPasswords)
		if initialize_file(filename):
			desc = eval(get_file(filename))
			if password:
				desc[chat] = password
				answer = self.AnsBase[4] % (password)
			elif chat not in desc:
				return self.AnsBase[5]
			else:
				del desc[chat]
				answer = self.AnsBase[6]
			cat_file(filename, str(desc))
		else:
			answer = AnsBase[7]
		return answer

	def command_logger_state(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if self.On:
				if body:
					ls = body.split(None, 1)
					body = (ls.pop(0)).lower()
					if body in ("on", "1", "вкл".decode("utf-8")):
						if not self.loggerDesc.has_key(source[1]):
							self.logger_01si(source[1], True)
							answer = AnsBase[4]
						else:
							answer = self.AnsBase[1]
					elif body in ("off", "0", "выкл".decode("utf-8")):
						if self.loggerDesc.has_key(source[1]):
							del self.loggerDesc[source[1]]
							cat_file(chat_file(source[1], self.ChatConfigFile), str(False))
							answer = AnsBase[4]
						else:
							answer = self.AnsBase[0]
					elif body in ("password", "пароль".decode("utf-8")):
						if ls:
							answer = self.setPassword(source[1], ls[0][:16].strip())
						else:
							answer = self.setPassword(source[1])
					else:
						answer = AnsBase[2]
				else:
					filename = os.path.join(self.RootDir, self.ChatsPasswords)
					if os.path.isfile(filename):
						desc = eval(get_file(filename))
						if desc.has_key(source[1]):
							Message(source[0], self.AnsBase[4] % desc[source[1]])
					answer = self.AnsBase[int(source[1] in self.loggerDesc)]
			else:
				answer = self.AnsBase[2]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	getConfig = lambda self: str({"dir": self.RootDir, "enabled": self.On})

	def command_logger_control(self, stype, source, body, disp):
		if body:
			ls = body.split(None, 1)
			body = (ls.pop(0)).lower()
			if body in ("on", "1", "вкл".decode("utf-8")):
				if not self.On:
					self.On = True
					cat_file(self.ConfigFile, self.getConfig())
					for chat in Chats.keys():
						self.logger_01si(chat)
					for inst, ls in self.handlers:
						self.handler_register(getattr(self, inst.__name__), ls)
					answer = AnsBase[4]
				else:
					answer = self.AnsBase[1]
			elif body in ("off", "0", "выкл".decode("utf-8")):
				if self.On:
					self.On = False
					cat_file(self.ConfigFile, self.getConfig())
					self.clear_handlers()
					answer = AnsBase[4]
				else:
					answer = self.AnsBase[0]
			elif ls and body in ("folder", "директория".decode("utf-8")):
				folder = os.path.normpath(ls.pop(0))
				try:
					if not os.path.isdir(folder): os.makedirs(folder, 0755)
				except Exception:
					answer = AnsBase[2]
				else:
					file = os.path.join(self.RootDir, self.ChatsCache)
					if os.path.isfile(file):
						shutil.copy(file, os.path.join(folder, self.ChatsCache))
					for chat, lock in self.loggerDesc.iteritems():
						filename = (chat + ".db")
						if not check_nosymbols(chat):
							filename = encode_filename(filename)
						ldir = os.path.join(folder, filename)
						with lock:
							chat = ChatsAttrs[chat]
							shutil.copy(chat["ldir"], ldir)
							chat["ldir"] = ldir
					cat_file(self.ConfigFile, self.getConfig())
					answer = AnsBase[4]
			else:
				answer = AnsBase[2]
		else:
			answer = "%s Chatlogs root folder -> %s" % (self.AnsBase[int(self.On)], self.RootDir)
		Answer(answer, stype, source, disp)

	def logger_00si(self):
		if initialize_file(self.ConfigFile, self.getConfig()):
			desc = eval(get_file(self.ConfigFile))
			self.RootDir, self.On = desc.get("dir", self.RootDir), desc.get("enabled", False)
			if not self.On:
				self.clear_handlers()
			if not os.path.isdir(self.RootDir):
				try:
					os.makedirs(self.RootDir, 0755)
				except Exception:
					Print("\n\nCan't make logger's root folder! I'll disable the expansion.", color2)
					self.dels(True)

	def logger_01si(self, chat, enable = False):
		file = chat_file(chat, self.ChatConfigFile)
		if enable or initialize_file(file, str(False)):
			if enable or eval(get_file(file)):
				if enable:
					cat_file(file, str(True))
				filename = (chat + ".db")
				if not check_nosymbols(chat):
					filename = encode_filename(filename)
					file = os.path.join(self.RootDir, self.ChatsCache)
					if initialize_file(file):
						desc = eval(get_file(file))
						desc[chat] = filename
						cat_file(file, str(desc))
				ldir = os.path.join(self.RootDir, filename)
				if not os.path.isfile(ldir):
					with database(ldir) as db:
						db("create table chatlogs (year integer, month integer, day integer, time text, nick text, jid text, data text, mode integer)")
						db.commit()
				ChatsAttrs.setdefault(chat, {})["ldir"], self.loggerDesc[chat] = ldir, ithr.Semaphore()

	def logger_04si(self, chat):
#		if not check_nosymbols(chat):
#			filename = os.path.join(self.RootDir, self.ChatsCache)
#			if os.path.isfile(filename):
#				desc = eval(get_file(filename))
#				if chat in desc:
#					del desc[chat]
#					cat_file(filename, str(desc))
#		filename = os.path.join(self.RootDir, self.ChatsPasswords)
#		if os.path.isfile(filename):
#			desc = eval(get_file(filename))
#			if chat in desc:
#				del desc[chat]
#				cat_file(filename, str(desc))
		if self.loggerDesc.has_key(chat):
			del self.loggerDesc[chat]

	commands = (
		(command_logs, "logs", 4,),
		(command_logger_state, "logger", 6,),
		(command_logger_control, "logger2", 8,)
	)

	handlers = (
		(logger_00si, "00si"),
		(logger_01si, "01si"),
		(logger_04si, "04si"),
		(logger_01eh, "01eh"),
		(logger_09eh, "09eh"),
		(logger_04eh, "04eh"),
		(logger_05eh, "05eh"),
		(logger_06eh, "06eh"),
		(logger_07eh, "07eh"),
		(logger_08eh, "08eh")
	)
