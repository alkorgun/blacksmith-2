# coding: utf-8

#  BlackSmith mark.2
# exp_name = "sheriff" # /code.py v.x8
#  Id: 15~6c
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	GoodServers = ["jabber.ru", "xmpp.ru", "jabbers.ru", "xmpps.ru", "jabber.org", "xmpp.org", "gmail.com", "jabberon.ru", "talkonaut.com", "gajim.org", "jabbrik.ru", "qip.ru", "blackfishka.ru", "helldev.net", "ya.ru", "jabberworld.net"]

	if (DefLANG != "RU"):
		GoodServers += ["jabber.com", "xmpp.com", "jabber.co.uk", "xmpp.co.uk"]

	LawsFile = "laws.db"

	Prison, Antiwipe = {}, {}

	class Convict(object):

		def __init__(self):
			self.devoice = 0
			self.prdates = [time.time()]
			self.msdates = []
			self.offenses = 0
			self.kicks = itypes.Number()
			self.verif = False
			self.vakey = ""
			self.vnumb = itypes.Number()

		def autenticated(self):
			self.verif = True
			self.vakey = ""
			delattr(self, "vnumb")

		def leaved(self):
			self.msdates = []
			self.vakey = ""

		def setDevoice(self):
			self.devoice = time.time()

		getDevoice = lambda self: (time.time() - self.devoice)

		def addPrTime(self):
			self.prdates.append(time.time())

		def addMsTime(self):
			self.msdates.append(time.time())

	def command_order(self, stype, source, body, disp):

		def change_cfg(chat, opt, state):
			if state in ("on", "1", "вкл".decode("utf-8")):
				ChatsAttrs[chat]["laws"][opt] = True
				answer = AnsBase[4]
			elif state in ("off", "0", "выкл".decode("utf-8")):
				ChatsAttrs[chat]["laws"][opt] = False
				answer = AnsBase[4]
			else:
				answer = AnsBase[2]
			return answer

		def alt_change_cfg(chat, opt, state, drange):
			if isNumber(state):
				state = int(state)
				if state in xrange(*drange):
					ChatsAttrs[chat]["laws"][opt] = state
					answer = AnsBase[4]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[30]
			return answer

		if Chats.has_key(source[1]):
			if body:
				ls = (body.lower()).split()
				arg0 = ls.pop(0)
				if ls:
					arg1 = ls.pop(0)
					if arg0 in ("servers", "сервера".decode("utf-8")):
						if ls:
							server = ls.pop(0)
							if server.count(chr(46)):
								if arg1 in ("add", "+"):
									if server not in (self.GoodServers + ChatsAttrs[source[1]]["laws"]["list"]):
										ChatsAttrs[source[1]]["laws"]["list"].append(server)
										answer = AnsBase[4]
									else:
										answer = self.AnsBase[34]
								elif arg1 in ("del", "-"):
									if server in ChatsAttrs[source[1]]["laws"]["list"]:
										ChatsAttrs[source[1]]["laws"]["list"].remove(server)
										answer = AnsBase[4]
									else:
										answer = self.AnsBase[35]
								else:
									answer = AnsBase[2]
							else:
								answer = self.AnsBase[36]
						else:
							answer = AnsBase[2]
					elif arg0 in ("awipe", "антивайп".decode("utf-8")):
						answer = change_cfg(source[1], "awipe", arg1)
					elif arg0 in ("aspace", "антиспэйс".decode("utf-8")):
						answer = change_cfg(source[1], "space", arg1)
					elif arg0 in ("sparta", "спарта".decode("utf-8")):
						answer = change_cfg(source[1], "sparta", arg1)
					elif arg0 in ("verif", "авторизация".decode("utf-8")):
						answer = change_cfg(source[1], "verif", arg1)
					elif arg0 in ("atiser", "антиреклама".decode("utf-8")):
						answer = change_cfg(source[1], "tiser", arg1)
					elif arg0 in ("aobscene", "антимат".decode("utf-8")):
						answer = change_cfg(source[1], "obscene", arg1)
					elif arg0 in ("acaps", "антикапс".decode("utf-8")):
						answer = change_cfg(source[1], "lower", arg1)
					elif arg0 in ("lnick", "никлен".decode("utf-8")):
						answer = alt_change_cfg(source[1], "lnick", arg1, (12, 33))
					elif arg0 in ("aban", "автобан".decode("utf-8")):
						answer = alt_change_cfg(source[1], "aban", arg1, (2, 7))
					elif arg0 in ("loyalty", "лояльность".decode("utf-8")):
						answer = alt_change_cfg(source[1], "loyalty", arg1, (1, 6))
					elif arg0 in ("devoice", "девойс".decode("utf-8")):
						answer = alt_change_cfg(source[1], "dtime", arg1, (60, 361))
					elif arg0 in ("msglen", "мсглен".decode("utf-8")):
						answer = alt_change_cfg(source[1], "len", arg1, (512, 2049))
					elif arg0 in ("prslen", "прзлен".decode("utf-8")):
						answer = alt_change_cfg(source[1], "prlen", arg1, (128, 513))
					else:
						answer = AnsBase[2]
					if answer == AnsBase[4]:
						cat_file(chat_file(source[1], self.LawsFile), str(ChatsAttrs[source[1]]["laws"]))
				elif arg0 in ("servers", "сервера".decode("utf-8")):
					answer = "\nDefault:\n%s" % enumerated_list(sorted(self.GoodServers))
					if ChatsAttrs[source[1]]["laws"]["list"]:
						answer += "\n\nDefined:\n%s" % enumerated_list(sorted(ChatsAttrs[source[1]]["laws"]["list"]))
				else:
					answer = AnsBase[2]
			else:
				answer = self.AnsBase[24]
				if ChatsAttrs[source[1]]["laws"]["space"]:
					answer += self.AnsBase[25][:-1]
				else:
					answer += self.AnsBase[26][:-1]
				answer += self.AnsBase[27] % (ChatsAttrs[source[1]]["laws"]["lnick"])
				if ChatsAttrs[source[1]]["laws"]["awipe"]:
					answer += self.AnsBase[25]
				else:
					answer += self.AnsBase[26]
				answer += self.AnsBase[28] % (ChatsAttrs[source[1]]["laws"]["aban"])
				if ChatsAttrs[source[1]]["laws"]["verif"]:
					answer += self.AnsBase[25]
				else:
					answer += self.AnsBase[26]
				answer += self.AnsBase[29] % (ChatsAttrs[source[1]]["laws"]["loyalty"])
				if ChatsAttrs[source[1]]["laws"]["tiser"]:
					answer += self.AnsBase[25]
				else:
					answer += self.AnsBase[26]
				answer += self.AnsBase[30] % (ChatsAttrs[source[1]]["laws"]["dtime"])
				if ChatsAttrs[source[1]]["laws"]["obscene"]:
					answer += self.AnsBase[25][:-1]
				else:
					answer += self.AnsBase[26][:-1]
				answer += self.AnsBase[31] % (ChatsAttrs[source[1]]["laws"]["len"])
				if ChatsAttrs[source[1]]["laws"]["lower"]:
					answer += self.AnsBase[25][:-1]
				else:
					answer += self.AnsBase[26][:-1]
				answer += self.AnsBase[32] % (ChatsAttrs[source[1]]["laws"]["prlen"])
				if ChatsAttrs[source[1]]["laws"]["sparta"]:
					answer += self.AnsBase[25][:-1]
				else:
					answer += self.AnsBase[26][:-1]
		else:
			answer = AnsBase[0]
		Answer(answer, stype, source, disp)

	def special_kick(self, chat, nick, text):
		Chats[chat].kick(nick, "%s: %s" % (get_nick(chat), text))
		raise ithr.ThrKill("exit")

	def sheriffs_loyalty(self, chat):
		access = loy = ChatsAttrs[chat]["laws"]["loyalty"]
		if access > 2:
			access = 2
		return (loy, access)

	compile_link = compile__("(?:http[s]?|ftp|svn)://[^\s'\"<>]+", 64)
	compile_chat = compile__("[^\s]+?@(?:conference|muc|conf|chat|group)\.[\w-]+?\.[\w-]+", 64)

	def tiser_checker(self, body):
		body = body.lower()
		if self.compile_link.search(body) or self.compile_chat.search(body):
			return True
		return False

	def lower_checker(self, chat, body):
		numb, body = 0, sub_desc(body, [chr(32), chr(10), chr(13), chr(9)] + Chats[chat].get_nicks()).strip()
		for char in body:
			if char.isupper():
				numb += 1
		if numb > 12 and numb > (len(body) / 3):
			return True
		return False

	Obscene = compile__(Obscene, 66)

	obscene_checker = lambda self, body: self.Obscene.search(chr(32) + body + chr(32))

	def check_nick(self, chat, nick):

		def nick_checker(chat, nick):
			if ("%" in nick) or ("/" in nick):
				return True
			nick = nick.split()[0].lower()
			if Cmds.has_key(nick):
				return True
			if Chats[chat].cPref and nick.startswith(Chats[chat].cPref):
				if Cmds.has_key(nick[1:]):
					return True
			return False

		if (nick.strip()):
			if len(nick) > ChatsAttrs[chat]["laws"]["lnick"]:
				self.special_kick(chat, nick, self.AnsBase[0] % (ChatsAttrs[chat]["laws"]["lnick"]))
			if nick_checker(chat, nick):
				self.special_kick(chat, nick, self.AnsBase[1])
			if ChatsAttrs[chat]["laws"]["space"]:
				if len(nick) != len(nick.strip()):
					self.special_kick(chat, nick, self.AnsBase[2])
			if ChatsAttrs[chat]["laws"]["obscene"]:
				if self.obscene_checker(nick):
					self.special_kick(chat, nick, self.AnsBase[3])

	def sheriff_set(self, stype, source, source_, access, loyalty, body, disp):
		if access <= loyalty:
			prisoner = self.Prison[source[1]].get(source_)
			if prisoner:
				prisoner.offenses += 1
				if prisoner.offenses in (1, 2):
					Answer(body, stype, source, disp); raise ithr.ThrKill("exit")
				elif prisoner.offenses == 3:
					Chats[source[1]].visitor(source[2], "%s: %s" % (get_nick(source[1]), body))
					prisoner.setDevoice()
					Message(source[0], self.AnsBase[16] % (body, ChatsAttrs[source[1]]["laws"]["dtime"]), disp)
					raise ithr.ThrKill("exit")
				else:
					prisoner.setDevoice()
					self.special_kick(source[1], source[2], body)
			else:
				self.special_kick(source[1], source[2], body)
		else:
			Answer(body, stype, source, disp); raise ithr.ThrKill("exit")

	def sheriff_01eh(self, stanza, isConf, stype, source, body, isToBs, disp):
		if isConf and source[2] and Chats[source[1]].isModer:
			source_ = get_source(source[1], source[2])
			if source_:
				loyalty, access = self.sheriffs_loyalty(source[1]), get_access(source[1], source[2])
				if access <= loyalty[0]:
					prisoner = self.Prison[source[1]].get(source_)
					if prisoner:
						prisoner.addMsTime()
						if ChatsAttrs[source[1]]["laws"]["tiser"]:
							if self.tiser_checker(body):
								if access <= loyalty[1]:
									if prisoner:
										prisoner.setDevoice()
									self.special_kick(source[1], source[2], self.AnsBase[4])
								else:
									Answer(self.AnsBase[4], stype, source, disp)
								raise ithr.ThrKill("exit")
						if ChatsAttrs[source[1]]["laws"]["verif"]:
							if access < 2 and prisoner.vakey and stype == sBase[0]:
								if prisoner.vakey == body.lower():
									prisoner.autenticated()
									Chats[source[1]].participant(source[2], self.AnsBase[20] % get_nick(source[1]))
									Message(source[0], self.AnsBase[21], disp)
								elif prisoner.vnumb.plus() >= 3:
									prisoner.vnumb = itypes.Number()
									self.special_kick(source[1], source[2], self.AnsBase[22])
								else:
									Message(source[0], self.AnsBase[23], disp)
								raise ithr.ThrKill("exit")
						list = prisoner.msdates
						if len(list) >= 4:
							if (list[-1] - list[0]) <= 6:
								prisoner.msdates = [list.pop()]
								prisoner.setDevoice()
								self.special_kick(source[1], source[2], self.AnsBase[15])
							else:
								prisoner.msdates.pop(0)
						del list
					if stype == sBase[1]:
						if ChatsAttrs[source[1]]["laws"]["obscene"]:
							if self.obscene_checker(body):
								self.sheriff_set(stype, source, source_, access, loyalty[1], self.AnsBase[5], disp)
						if ChatsAttrs[source[1]]["laws"]["len"]:
							if len(body) > ChatsAttrs[source[1]]["laws"]["len"]:
								self.sheriff_set(stype, source, source_, access, loyalty[1], self.AnsBase[6], disp)
						if ChatsAttrs[source[1]]["laws"]["lower"]:
							if self.lower_checker(source[1], body):
								self.sheriff_set(stype, source, source_, access, loyalty[1], self.AnsBase[7], disp)

	def awipeClear(self, chat, list):
		if chat in Chats:
			self.Antiwipe[chat]["clear"] = []
			for sUser in Chats[chat].get_users():
				if sUser.source in list:
					if not sUser.ishere:
						if Chats[chat].isHere(sUser.nick):
							del Chats[chat].desc[sUser.nick]
						if sUser.source in self.Prison[chat]:
							del self.Prison[chat][sUser.source]
			for source_ in list:
				Chats[chat].none(source_); sleep(0.4)

	def get_server(self, source, state = False):
		at = chr(64)
		if at in source:
			source = source.split(at)[1]
			if state:
				source = source.split(chr(46), 1)[1]
		return source

	GoodServers__ = lambda self, chat: (self.GoodServers + ChatsAttrs[chat]["laws"]["list"] + [self.get_server(chat, True)])

	def check_wipe(self, chat, nick, role, inst):
		if role == aRoles[2]:
			BsNick = get_nick(chat)
			if ChatsAttrs[chat]["laws"]["sparta"]:
				jid = self.get_server(inst)
				if jid not in self.GoodServers__(chat):
					Reason = ("%s: This is SPARTA!!" % BsNick)
					Chats[chat].outcast(jid, Reason); Chats[chat].kick(nick, Reason)
			elif ChatsAttrs[chat]["laws"]["awipe"]:
				Time = time.time()
				if (Time - Chats[chat].sdate) >= 60:
					difference = (Time - self.Antiwipe[chat]["ltime"])
					if difference > 360 and self.Antiwipe[chat]["clear"]:
						sThread(self.awipeClear.__name__, self.awipeClear, (chat, self.Antiwipe[chat]["clear"],))
					if difference > 15:
						self.Antiwipe[chat]["ltime"] = Time
						self.Antiwipe[chat]["jids"] = [inst]
					else:
						self.Antiwipe[chat]["jids"].append(inst)
						joined = self.Antiwipe[chat]["jids"]
						Numb = len(joined)
						if Numb >= 3:
							self.Antiwipe[chat]["ltime"] = Time
							jid = self.get_server(inst)
							if jid == self.get_server(joined[Numb - 2]) and jid == self.get_server(joined[Numb - 3]):
								if jid not in self.GoodServers__(chat):
									ls = []
									for sUser in Chats[chat].get_users():
										if sUser.source and sUser.ishere:
											if sUser.nick != BsNick and sUser.role[0] == aRoles[2]:
												if jid == self.get_server(sUser.source):
													if sUser.source in self.Prison[chat]:
														if not self.Prison[chat][sUser.source].verif:
															ls.append(sUser)
									Chats[chat].outcast(jid, self.AnsBase[12] % (BsNick))
									if ls:
										for sUser in ls:
											Chats[chat].kick(sUser.nick, self.AnsBase[12] % (BsNick))
								else:
									for sUser in Chats[chat].get_users():
										if sUser.source and sUser.ishere:
											if sUser.nick != BsNick and sUser.role[0] == aRoles[2]:
												if jid == self.get_server(sUser.source):
													if sUser.source in self.Prison[chat]:
														if not self.Prison[chat][sUser.source].verif:
															self.Antiwipe[chat]["clear"].append(sUser.source)
															Chats[chat].outcast(sUser.source, self.AnsBase[12] % (BsNick))
							else:
								self.Antiwipe[chat]["clear"].append(inst)
								Chats[chat].outcast(inst, self.AnsBase[12] % (BsNick))
							raise ithr.ThrKill("exit")

	Questions = []

	def sheriff_04eh(self, chat, nick, source_, role, stanza, disp):
		if source_ and nick != get_nick(chat):
			access = get_access(chat, nick)
			if access <= self.sheriffs_loyalty(chat)[1]:
				prisoner = self.Prison[chat].get(source_)
				if prisoner:
					prisoner.addPrTime()
					if prisoner.devoice:
						eTime = prisoner.getDevoice()
						if (eTime < ChatsAttrs[chat]["laws"]["dtime"]):
							Chats[chat].visitor(nick, self.AnsBase[11] % get_nick(chat))
							Message("%s/%s" % (chat, nick), self.AnsBase[14] % Time2Text(ChatsAttrs[chat]["laws"]["dtime"] - eTime), disp)
						else:
							prisoner.devoice = 0
				else:
					self.Prison[chat][source_] = prisoner = self.Convict()
				if not prisoner.verif and access >= 2:
					prisoner.autenticated()
				self.check_wipe(chat, nick, role[0], source_)
				self.check_nick(chat, nick)
				if ChatsAttrs[chat]["laws"]["verif"] and access < 2 and aRoles[2] == role[0]:
					if not prisoner.verif and not prisoner.devoice:
						Chats[chat].visitor(nick, self.AnsBase[17] % get_nick(chat))
						if not self.Questions:
							for qu in self.AnsBase[19].splitlines():
								qu, an = qu.split(chr(124), 1)
								self.Questions.append((qu.strip(), (an.strip()).lower()))
						qu, an = choice(self.Questions)
						prisoner.vakey = an
						Message("%s/%s" % (chat, nick), self.AnsBase[18] % (qu), disp)
						del qu, an
				list = prisoner.prdates
				if len(list) >= 4:
					if (list[-1] - list[0]) <= 10:
						prisoner.prdates = [list.pop()]
						self.special_kick(chat, nick, self.AnsBase[13])
					else:
						prisoner.prdates.pop(0)
				del list
				status = stanza.getStatus()
				if status:
					if ChatsAttrs[chat]["laws"]["tiser"]:
						if self.tiser_checker(status):
							self.special_kick(chat, nick, self.AnsBase[4])
					if ChatsAttrs[chat]["laws"]["obscene"]:
						if self.obscene_checker(status):
							self.special_kick(chat, nick, self.AnsBase[8])
					if ChatsAttrs[chat]["laws"]["prlen"]:
						if len(status) > ChatsAttrs[chat]["laws"]["prlen"]:
							self.special_kick(chat, nick, self.AnsBase[9])

	def sheriff_05eh(self, chat, nick, sbody, scode, disp):
		if nick != get_nick(chat):
			source_ = get_source(chat, nick)
			if source_:
				prisoner = self.Prison[chat].get(source_)
				if prisoner:
					if not Chats[chat].isModer or scode in (sCodes[0], sCodes[3]):
						del self.Prison[chat][source_]
					else:
						prisoner.leaved()
						if scode == sCodes[2] and prisoner.kicks.plus() >= ChatsAttrs[chat]["laws"]["aban"]:
							if ChatsAttrs[chat]["laws"]["aban"]:
								del self.Prison[chat][source_]
								Chats[chat].outcast(source_, self.AnsBase[10] % (get_nick(chat), ChatsAttrs[chat]["laws"]["aban"]))

	def sheriff_06eh(self, chat, old_nick, nick, disp):
		if nick != get_nick(chat) and Chats[chat].isModer:
			sUser = Chats[chat].get_user(nick)
			if getattr(sUser, "source", None):
				prisoner = self.Prison[chat].get(sUser.source)
				if prisoner:
					prisoner.addPrTime()
					self.check_wipe(chat, nick, sUser.role[0], sUser.source)
					self.check_nick(chat, nick)
					list = prisoner.prdates
					if len(list) >= 4:
						if (list[-1] - list[0]) <= 10:
							prisoner.prdates = [list.pop()]
							self.special_kick(chat, nick, self.AnsBase[13])
						else:
							prisoner.prdates.pop(0)

	def sheriff_07eh(self, chat, nick, role, disp):
		if nick != get_nick(chat):
			sUser = Chats[chat].get_user(nick)
			if getattr(sUser, "source", None):
				prisoner = ((sUser.access <= self.sheriffs_loyalty(chat)[1]) and Chats[chat].isModer)
				if sUser.source in self.Prison[chat]:
					if not prisoner:
						del self.Prison[chat][sUser.source]
				elif prisoner:
					self.Prison[chat][sUser.source] = self.Convict()

	def sheriff_08eh(self, chat, nick, stanza, disp):
		if nick != get_nick(chat) and Chats[chat].isModer:
			source_ = get_source(chat, nick)
			if source_:
				prisoner = self.Prison[chat].get(source_)
				if prisoner:
					prisoner.addPrTime()
					list = prisoner.prdates
					if len(list) >= 4:
						if (list[-1] - list[0]) <= 10:
							prisoner.prdates = [list.pop()]
							self.special_kick(chat, nick, self.AnsBase[13])
						else:
							prisoner.prdates.pop(0)
					del list
					status = stanza.getStatus()
					if status:
						if ChatsAttrs[chat]["laws"]["tiser"]:
							if self.tiser_checker(status):
								self.special_kick(chat, nick, self.AnsBase[4])
						if ChatsAttrs[chat]["laws"]["obscene"]:
							if self.obscene_checker(status):
								self.special_kick(chat, nick, self.AnsBase[8])
						if ChatsAttrs[chat]["laws"]["prlen"]:
							if len(status) > ChatsAttrs[chat]["laws"]["prlen"]:
								self.special_kick(chat, nick, self.AnsBase[9])

	def sheriff_01si(self, chat):
		self.Prison[chat] = {}
		self.Antiwipe[chat] = {"ltime": 0, "jids": [], "clear": []}
		desc = ChatsAttrs.setdefault(chat, {})
		desc["laws"] = {"awipe": True, "space": True, "verif": False, "tiser": True, "obscene": False, "lower": False, "sparta": False, "list": [], "dtime": 180, "loyalty": 1, "aban": 3, "prlen": 256, "lnick": 24, "len": 1024}
		filename = chat_file(chat, self.LawsFile)
		if initialize_file(filename, str(desc["laws"])):
			desc["laws"] = eval(get_file(filename))

	def sheriff_04si(self, chat):
		del self.Prison[chat]
		del self.Antiwipe[chat]

	commands = ((command_order, "order", 6,),)

	handlers = (
		(sheriff_01si, "01si"),
		(sheriff_04si, "04si"),
		(sheriff_01eh, "01eh"),
		(sheriff_04eh, "04eh"),
		(sheriff_05eh, "05eh"),
		(sheriff_06eh, "06eh"),
		(sheriff_07eh, "07eh"),
		(sheriff_08eh, "08eh")
	)

del Obscene
