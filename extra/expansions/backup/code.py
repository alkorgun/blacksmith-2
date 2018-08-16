# coding: utf-8

#  BlackSmith mark.2
# exp_name = "backup" # /code.py v.x3
#  Id: 36~3c
#  Code © (2012-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	BackupFolder = "backup/"
	OptsFolder = BackupFolder + "opts"
	SubjectsFolder = BackupFolder + "subjects"
	CopyDateFile = "copyed.db"

	affs = ("owner", "admin", "member", "outcast")

	affDesc = {
		"owners": 0,
		"овнеров".decode("utf-8"): 0,
		"admins": 1,
		"админов".decode("utf-8"): 1,
		"members": 2,
		"мемберов".decode("utf-8"): 2,
		"outcasts": 3,
		"баны".decode("utf-8"): 3
	}

	def get_backup(self, folder):
		backups = []
		if os.path.isdir(folder):
			for file in os.listdir(folder):
				try:
					backups.append(float(file))
				except ValueError:
					pass
		return backups

	def set_subject(self, chat, date, answer, conf = None):
		if not conf:
			conf = chat
		if conf not in Chats:
			raise SelfExc("exit")
		folder = cefile(chat_file(chat, self.SubjectsFolder))
		if date:
			backups = (date,)
		else:
			backups = self.get_backup(folder)
		if backups:
			date = max(backups)
			filename = "%s/%s" % (folder, date)
			if os.path.isfile(filename):
				Chats[conf].subject(get_file(filename).decode("utf-8"))
				answer.append(self.AnsBase[9] % time.ctime(date))
			else:
				answer.append(self.AnsBase[0])
		else:
			answer.append(self.AnsBase[0])

	def get_timer(self, chat, name):
		uTime = time.time()
		tdesc = ChatsAttrs[chat]["backup"]["flags"]
		if name in tdesc:
			timer = (uTime - tdesc[name])
		else:
			timer = uTime
		return timer, uTime, tdesc

	def set_options(self, chat, date, answer, stype, source, conf = None):
		if not conf:
			conf = chat
		if conf not in Chats:
			raise SelfExc("exit")
		folder = cefile(chat_file(chat, self.OptsFolder))
		if date:
			backups = (date,)
		else:
			backups = self.get_backup(folder)
		if backups:
			date = max(backups)
			filename = "%s/%s" % (folder, date)
			if os.path.isfile(filename):
				Chat = Chats[conf]
				if getattr(Chat.get_user(Chat.nick), "role", (None,))[0] != self.affs[0]:
					answer.append(self.AnsBase[18])
				else:
					try:
						form = xmpp.simplexml.XML2Node(get_file(filename))
					except Exception:
						answer.append(self.AnsBase[11])
					else:
						timer, uTime, tdesc = self.get_timer(conf, "opts")
						if timer >= 3600:
							tdesc["opts"] = uTime
							iq = xmpp.Iq(sBase[9], to = conf)
							query = iq.addChild(sBase[18], namespace = xmpp.NS_MUC_OWNER)
							query.addChild(node = form)
							iq.setID("Bs-i%d" % Info["outiq"].plus())
							CallForResponse(Chat.disp, iq, self.answer_accept_opts, {"date": date, "stype": stype, "source": source})
						else:
							answer.append(self.AnsBase[16] % Time2Text(3600 - timer))
			else:
				answer.append(self.AnsBase[4])
		else:
			answer.append(self.AnsBase[4])

	def set_roles(self, chat, date, answer, stype, source, role, conf = None):
		if not conf:
			conf = chat
		if conf not in Chats:
			raise SelfExc("exit")
		if role == self.affs[0] and getattr(Chats[conf].get_user(Chats[conf].nick), "role", (None,))[0] != self.affs[0]:
			answer.append(self.AnsBase[13])
		else:
			folder = cefile(chat_file(chat, (self.BackupFolder + role + "s")))
			if date:
				backups = (date,)
			else:
				backups = self.get_backup(folder)
			if backups:
				date = max(backups)
				filename = "%s/%s" % (folder, date)
				disp_str = Chats[conf].disp
				disp = Clients.get(disp_str, disp_str)
				if os.path.isfile(filename):
					timer, uTime, tdesc = self.get_timer(conf, role)
					if timer >= 3600:
						tdesc[role] = uTime
						with open(filename) as fp:
							while conf in Chats:
								line = fp.readline()
								if not line:
									break
								line = line.decode("utf-8")
								line = line.split(None, 1)
								data = line.pop(0)
								if data == disp_str:
									continue
								iq = xmpp.Iq(sBase[9], to = conf)
								iq.setID("Bs-i%d" % Info["outiq"].plus())
								query = xmpp.Node(sBase[18])
								query.setNamespace(xmpp.NS_MUC_ADMIN)
								arole = query.addChild("item", {sBase[11]: data, aRoles[0]: role})
								if line:
									arole.setTagData("reason", line[0])
								iq.addChild(node = query)
								sleep(0.2)
								Sender(disp, iq)
							else:
								raise SelfExc("exit")
						answer.append(self.AnsBase[8] % (role, time.ctime(date)))
					else:
						answer.append(self.AnsBase[17] % (role, Time2Text(3600 - timer)))
				else:
					answer.append(self.AnsBase[2] % role)
			else:
				answer.append(self.AnsBase[2] % role)

	restoreLock = ithr.allocate_lock()

	def command_backup(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				ls = body.split()
				body = (ls.pop(0)).lower()
				if body in ("list", "лист".decode("utf-8")):
					answer = ["\->"]
					for name in (self.affs + ("subject", "opt")):
						name += "s"
						backups = self.get_backup(cefile(chat_file(source[1], (self.BackupFolder + name))))
						name = name.capitalize()
						if backups:
							answer.append("%s:\n%s" % (name, ",\n".join(sorted(["%s (%s)" % (date, time.ctime(date)) for date in backups]))))
						else:
							answer.append("%s: None" % name)
					answer = str.join(chr(10)*2, answer)
				elif body in ("create", "создать".decode("utf-8")):
					if Chats[source[1]].isModer:
						timer, uTime, tdesc = self.get_timer(source[1], "make")
						if timer >= 3600:
							tdesc["make"] = uTime
							iq = xmpp.Iq(sBase[10], to = source[1])
							iq.addChild(sBase[18], namespace = xmpp.NS_MUC_OWNER)
							iq.setID("Bs-i%d" % Info["outiq"].plus())
							CallForResponse(disp, iq, self.answer_backup_opts, {"stype": stype, "source": source})
							for role in self.affs:
								iq = xmpp.Iq(sBase[10], to = source[1])
								query = xmpp.Node(sBase[18])
								query.setNamespace(xmpp.NS_MUC_ADMIN)
								query.addChild("item", {aRoles[0]: role})
								iq.addChild(node = query)
								iq.setID("Bs-i%d" % Info["outiq"].plus())
								CallForResponse(disp, iq, self.answer_backup_aflist, {"role": role, "stype": stype, "source": source})
							answer = self.AnsBase[int(bool(ChatsAttrs[source[1]]["backup"]["subjects"]["last"]))]
						else:
							answer = self.AnsBase[14] % Time2Text(3600 - timer)
					else:
						answer = self.AnsBase[12]
				elif ls and body in ("restore", "восстановить".decode("utf-8")):
					if Chats[source[1]].isModer:
						if not self.restoreLock.locked():
							with self.restoreLock:
								element = (ls.pop(0)).lower()
								if element in ("all", "всё".decode("utf-8")):
									answer = []
									self.set_subject(source[1], None, answer)
									self.set_options(source[1], None, answer, stype, source)
									for role in self.affs:
										self.set_roles(source[1], None, answer, stype, source, role)
									answer = str.join(chr(10), answer)
								else:
									try:
										if ls:
											date = float(ls.pop(0))
										else:
											date = None
									except ValueError:
										answer = self.AnsBase[2]
									else:
										answer = []
										if element in ("subject", "тему".decode("utf-8")):
											self.set_subject(source[1], date, answer)
											answer = answer[0]
										elif element in ("options", "опции".decode("utf-8")):
											self.set_options(source[1], date, answer, stype, source)
											if answer:
												answer = answer[0]
											else:
												del answer
										elif element in self.affDesc:
											self.set_roles(source[1], date, answer, stype, source, self.affs[self.affDesc[element]])
											answer = answer[0]
										else:
											answer = AnsBase[2]
						else:
							answer = self.AnsBase[15]
					else:
						answer = self.AnsBase[12]
				elif ls and body in ("copy", "скопировать".decode("utf-8")):
					chat = (ls.pop(0)).lower()
					if chat in Chats:
						if Chats[source[1]].isModer:
							if not self.restoreLock.locked():
								with self.restoreLock:
									timer, uTime, tdesc = self.get_timer(source[1], "copy")
									if timer >= 86400:
										if enough_access(source[1], source[2], 7):
											answer = []
											self.set_subject(chat, None, answer, source[1])
											self.set_options(chat, None, answer, stype, source, source[1])
											for role in self.affs:
												self.set_roles(chat, None, answer, stype, source, role, source[1])
											uTime = time.time()
											for chat in (chat, source[1]):
												ChatsAttrs[chat]["backup"]["flags"]["copy"] = uTime
												cat_file(chat_file(chat, self.CopyDateFile), str(uTime))
											answer = str.join(chr(10), answer)
										else:
											iq = xmpp.Iq(sBase[10], to = chat)
											query = xmpp.Node(sBase[18])
											query.setNamespace(xmpp.NS_MUC_ADMIN)
											query.addChild("item", {aRoles[0]: self.affs[0]})
											iq.addChild(node = query)
											iq.setID("Bs-i%d" % Info["outiq"].plus())
											CallForResponse(disp, iq, self.answer_check_owner, {"chat": chat, "stype": stype, "source": source})
									else:
										answer = self.AnsBase[21] % Time2Text(86400 - timer)
							else:
								answer = self.AnsBase[15]
						else:
							answer = self.AnsBase[12]
					else:
						answer = AnsBase[3] % (chat)
				else:
					answer = AnsBase[2]
			else:
				answer = [self.AnsBase[10]]
				for name in (self.affs + ("subject", "opt")):
					name += "s"
					backups = self.get_backup(cefile(chat_file(source[1], (self.BackupFolder + name))))
					name = name.capitalize()
					if backups:
						answer.append("%s: %s" % (name, time.ctime(max(backups))))
					else:
						answer.append("%s: None" % name)
				answer = str.join(chr(10), answer)
		else:
			answer = AnsBase[0]
		if locals().has_key(sBase[6]):
			Answer(answer, stype, source, disp)

	filter = "muc#roomconfig_filter_jid"

	def answer_backup_opts(self, disp, stanza, stype, source):
		if xmpp.isResultNode(stanza):
			folder = cefile(chat_file(source[1], self.OptsFolder))
			try:
				if not os.path.isdir(folder): os.makedirs(folder, 0755)
			except:
				answer = AnsBase[2]
			else:
				form = xmpp.DataForm("submit")
				for node in stanza.getQueryChildren():
					if node.getNamespace() == xmpp.NS_DATA:
						for field in node.getChildren():
							if field.getName() == "field":
								var = field.getAttr("var")
								if var != self.filter:
									ftype = field.getAttr("type")
									value = field.getTagData("value") or str()
									field = form.setField(var, value, ftype)
				form = str(form)
				cat_file("%s/%s" % (folder, time.time()), form.replace("><", ">\r\n<"))
				ls = self.get_backup(folder)
				if len(ls) > 3:
					del_file("%s/%s" % (folder, min(ls)))
				answer = self.AnsBase[5]
		else:
			answer = self.AnsBase[4]
		Answer(answer, stype, source, disp)

	def answer_backup_aflist(self, disp, stanza, role, stype, source):
		if xmpp.isResultNode(stanza):
			folder = cefile(chat_file(source[1], (self.BackupFolder + role + "s")))
			try:
				if not os.path.isdir(folder): os.makedirs(folder, 0755)
			except Exception:
				answer = AnsBase[2]
			else:
				jids = []
				for node in stanza.getQueryChildren():
					jid = node.getAttr("jid")
					if jid:
						signature = node.getTagData("reason")
						if signature:
							jid = "%s %s" % (jid, signature)
						jids.append(jid)
				if jids:
					cat_file("%s/%s" % (folder, time.time()), "\r\n".join(jids))
					backups = self.get_backup(folder)
					if len(backups) > 3:
						del_file("%s/%s" % (folder, min(backups)))
					answer = self.AnsBase[3] % (role)
				else:
					answer = self.AnsBase[2] % (role)
		else:
			answer = self.AnsBase[2] % (role)
		Answer(answer, stype, source, disp)

	def answer_accept_opts(self, disp, stanza, date, stype, source):
		if xmpp.isResultNode(stanza):
			answer = self.AnsBase[7] % time.ctime(date)
		else:
			answer = self.AnsBase[6]
		Answer(answer, stype, source, disp)

	def answer_check_owner(self, disp, stanza, chat, stype, source):
		if xmpp.isResultNode(stanza):
			source_ = get_source(source[1], source[2])
			for node in stanza.getQueryChildren():
				jid = node.getAttr("jid")
				if jid and jid == source_:
					if self.restoreLock.locked():
						answer = self.AnsBase[15]
						break
					with self.restoreLock:
						answer = []
						self.set_subject(chat, None, answer, source[1])
						self.set_options(chat, None, answer, stype, source, source[1])
						for role in self.affs:
							self.set_roles(chat, None, answer, stype, source, role, source[1])
						uTime = time.time()
						for chat in (chat, source[1]):
							ChatsAttrs[chat]["backup"]["flags"]["copy"] = uTime
							cat_file(chat_file(chat, self.CopyDateFile), str(uTime))
						answer = str.join(chr(10), answer)
					break
			else:
				answer = self.AnsBase[19] % (chat)
		else:
			answer = self.AnsBase[20] % (chat)
		Answer(answer, stype, source, disp)

	def subjects_backup(self, chat, nick, sbody, body, disp):
		sbody = sbody.replace(chr(10), chr(13) + chr(10))
		sdesc = ChatsAttrs[chat]["backup"]["subjects"]
		if not sdesc["list"] or sbody != sdesc["last"]:
			folder = cefile(chat_file(chat, self.SubjectsFolder))
			try:
				if not os.path.isdir(folder): os.makedirs(folder, 0755)
			except Exception:
				pass
			else:
				uTime = time.time()
				sdesc["last"] = sbody
				sdesc["list"].append(uTime)
				cat_file("%s/%s" % (folder, uTime), sbody)
				if len(sdesc["list"]) > 6:
					oldest = min(sdesc["list"])
					sdesc["list"].remove(oldest)
					del_file("%s/%s" % (folder, oldest))

	def init_backup(self, chat):
		folder = cefile(chat_file(chat, self.SubjectsFolder))
		backups = self.get_backup(folder)
		if backups:
			subjects = {
				"list": backups,
				"last": get_file("%s/%s" % (folder, max(backups))).decode("utf-8")
			}
		else:
			subjects = {"list": [], "last": None}
		desc = ChatsAttrs.setdefault(chat, {})
		desc["backup"] = {"subjects": subjects, "flags": {}}
		filename = cefile(chat_file(chat, self.CopyDateFile))
		if os.path.isfile(filename):
			desc["backup"]["flags"]["copy"] = eval(get_file(filename))

	commands = (
		(command_backup, "backup", 6,),
	)

	handlers = (
		(init_backup, "01si"),
		(subjects_backup, "09eh")
	)
