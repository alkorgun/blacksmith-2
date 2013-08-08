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

		def change_cfg(conf, Name, mode):
			if mode in ("on", "1", "вкл".decode("utf-8")):
				ChatsAttrs[conf]["laws"][Name] = True
				answer = AnsBase[4]
			elif mode in ("off", "0", "выкл".decode("utf-8")):
				ChatsAttrs[conf]["laws"][Name] = False
				answer = AnsBase[4]
			else:
				answer = AnsBase[2]
			return answer

		def alt_change_cfg(conf, Name, mode, drange):
			if isNumber(mode):
				mode = int(mode)
				if mode in xrange(*drange):
					ChatsAttrs[conf]["laws"][Name] = mode
					answer = AnsBase[4]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[30]
			return answer

		if Chats.has_key(source[1]):
			if body:
				ls = (body.lower()).split()
				Name = ls.pop(0)
				if ls:
					mode = ls.pop(0)
					if Name in ("servers", "сервера".decode("utf-8")):
						if ls:
							jid = ls.pop(0)
							if jid.count(chr(46)):
								if mode in ("add", "+"):
									if jid not in (self.GoodServers + ChatsAttrs[source[1]]["laws"]["list"]):
										ChatsAttrs[source[1]]["laws"]["list"].append(jid)
										answer = AnsBase[4]
									else:
										answer = self.AnsBase[34]
								elif mode in ("del", "-"):
									if ChatsAttrs[source[1]]["laws"]["list"].count(jid):
										ChatsAttrs[source[1]]["laws"]["list"].remove(jid)
										answer = AnsBase[4]
									else:
										answer = self.AnsBase[35]
								else:
									answer = AnsBase[2]
							else:
								answer = self.AnsBase[36]
						else:
							answer = AnsBase[2]
					elif Name in ("awipe", "антивайп".decode("utf-8")):
						answer = change_cfg(source[1], "awipe", mode)
					elif Name in ("aspace", "антиспэйс".decode("utf-8")):
						answer = change_cfg(source[1], "space", mode)
					elif Name in ("sparta", "спарта".decode("utf-8")):
						answer = change_cfg(source[1], "sparta", mode)
					elif Name in ("verif", "авторизация".decode("utf-8")):
						answer = change_cfg(source[1], "verif", mode)
					elif Name in ("atiser", "антиреклама".decode("utf-8")):
						answer = change_cfg(source[1], "tiser", mode)
					elif Name in ("aobscene", "антимат".decode("utf-8")):
						answer = change_cfg(source[1], "obscene", mode)
					elif Name in ("acaps", "антикапс".decode("utf-8")):
						answer = change_cfg(source[1], "lower", mode)
					elif Name in ("lnick", "никлен".decode("utf-8")):
						answer = alt_change_cfg(source[1], "lnick", mode, (12, 33))
					elif Name in ("aban", "автобан".decode("utf-8")):
						answer = alt_change_cfg(source[1], "aban", mode, (2, 7))
					elif Name in ("loyalty", "лояльность".decode("utf-8")):
						answer = alt_change_cfg(source[1], "loyalty", mode, (1, 6))
					elif Name in ("devoice", "девойс".decode("utf-8")):
						answer = alt_change_cfg(source[1], "dtime", mode, (60, 361))
					elif Name in ("msglen", "мсглен".decode("utf-8")):
						answer = alt_change_cfg(source[1], "len", mode, (512, 2049))
					elif Name in ("prslen", "прзлен".decode("utf-8")):
						answer = alt_change_cfg(source[1], "prlen", mode, (128, 513))
					else:
						answer = AnsBase[2]
					if answer == AnsBase[4]:
						cat_file(chat_file(source[1], self.LawsFile), str(ChatsAttrs[source[1]]["laws"]))
				elif Name in ("servers", "сервера".decode("utf-8")):
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

	def special_kick(self, conf, nick, text):
		Chats[conf].kick(nick, "%s: %s" % (get_nick(conf), text))
		raise iThr.ThrKill("exit")

	def sheriffs_loyalty(self, conf):
		access = loy = ChatsAttrs[conf]["laws"]["loyalty"]
		if access > 2:
			access = 2
		return (loy, access)

	compile_link = compile__("(?:http[s]?|ftp|svn)://[^\s'\"<>]+", 64)
	compile_chat = compile__("[^\s]+?@(?:conference|muc|chat|room)\.[\w-]+?\.[\w-]+", 64)

	def tiser_checker(self, body):
		body = body.lower()
		if self.compile_link.search(body) or self.compile_chat.search(body):
			return True
		return False

	def lower_checker(self, conf, body):
		numb, body = 0, sub_desc(body, [chr(32), chr(10), chr(13), chr(9)] + Chats[conf].get_nicks()).strip()
		for char in body:
			if char.isupper():
				numb += 1
		if numb > 12 and numb > (len(body) / 3):
			return True
		return False

	Obscene = compile__(Obscene, 66)

	obscene_checker = lambda self, body: self.Obscene.search(chr(32) + body + chr(32))

	def check_nick(self, conf, nick):

		def nick_checker(conf, nick):
			if ("%" in nick) or ("/" in nick):
				return True
			nick = nick.split()[0].lower()
			if Cmds.has_key(nick):
				return True
			if Chats[conf].cPref and nick.startswith(Chats[conf].cPref):
				if Cmds.has_key(nick[1:]):
					return True
			return False

		if (nick.strip()):
			if len(nick) > ChatsAttrs[conf]["laws"]["lnick"]:
				self.special_kick(conf, nick, self.AnsBase[0] % (ChatsAttrs[conf]["laws"]["lnick"]))
			if nick_checker(conf, nick):
				self.special_kick(conf, nick, self.AnsBase[1])
			if ChatsAttrs[conf]["laws"]["space"]:
				if len(nick) != len(nick.strip()):
					self.special_kick(conf, nick, self.AnsBase[2])
			if ChatsAttrs[conf]["laws"]["obscene"]:
				if self.obscene_checker(nick):
					self.special_kick(conf, nick, self.AnsBase[3])

	def sheriff_set(self, stype, source, source_, access, loyalty, body, disp):
		if access <= loyalty:
			prisoner = self.Prison[source[1]].get(source_)
			if prisoner:
				prisoner.offenses += 1
				if prisoner.offenses in (1, 2):
					Answer(body, stype, source, disp); raise iThr.ThrKill("exit")
				elif prisoner.offenses == 3:
					Chats[source[1]].visitor(source[2], "%s: %s" % (get_nick(source[1]), body))
					prisoner.setDevoice()
					Message(source[0], self.AnsBase[16] % (body, ChatsAttrs[source[1]]["laws"]["dtime"]), disp)
					raise iThr.ThrKill("exit")
				else:
					prisoner.setDevoice()
					self.special_kick(source[1], source[2], body)
			else:
				self.special_kick(source[1], source[2], body)
		else:
			Answer(body, stype, source, disp); raise iThr.ThrKill("exit")

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
								raise iThr.ThrKill("exit")
						if ChatsAttrs[source[1]]["laws"]["verif"]:
							if access < 2 and prisoner.vakey and stype == Types[0]:
								if prisoner.vakey == body.lower():
									prisoner.autenticated()
									Chats[source[1]].participant(source[2], self.AnsBase[20] % get_nick(source[1]))
									Message(source[0], self.AnsBase[21], disp)
								elif prisoner.vnumb.plus() >= 3:
									prisoner.vnumb = itypes.Number()
									self.special_kick(source[1], source[2], self.AnsBase[22])
								else:
									Message(source[0], self.AnsBase[23], disp)
								raise iThr.ThrKill("exit")
						list = prisoner.msdates
						if len(list) >= 4:
							if (list[-1] - list[0]) <= 6:
								prisoner.msdates = [list.pop()]
								prisoner.setDevoice()
								self.special_kick(source[1], source[2], self.AnsBase[15])
							else:
								prisoner.msdates.pop(0)
						del list
					if stype == Types[1]:
						if ChatsAttrs[source[1]]["laws"]["obscene"]:
							if self.obscene_checker(body):
								self.sheriff_set(stype, source, source_, access, loyalty[1], self.AnsBase[5], disp)
						if ChatsAttrs[source[1]]["laws"]["len"]:
							if len(body) > ChatsAttrs[source[1]]["laws"]["len"]:
								self.sheriff_set(stype, source, source_, access, loyalty[1], self.AnsBase[6], disp)
						if ChatsAttrs[source[1]]["laws"]["lower"]:
							if self.lower_checker(source[1], body):
								self.sheriff_set(stype, source, source_, access, loyalty[1], self.AnsBase[7], disp)

	def awipeClear(self, conf, list):
		if Chats.has_key(conf):
			self.Antiwipe[conf]["clear"] = []
			for sUser in Chats[conf].get_users():
				if sUser.source in list:
					if not sUser.ishere:
						if Chats[conf].isHere(sUser.nick):
							del Chats[conf].desc[sUser.nick]
						if self.Prison[conf].has_key(sUser.source):
							del self.Prison[conf][sUser.source]
			for source_ in list:
				Chats[conf].none(source_); sleep(0.4)

	def get_server(self, source, state = False):
		at = chr(64)
		if at in source:
			source = source.split(at)[1]
			if state:
				source = source.split(chr(46), 1)[1]
		return source

	GoodServers__ = lambda self, conf: (self.GoodServers + ChatsAttrs[conf]["laws"]["list"] + [self.get_server(conf, True)])

	def check_wipe(self, conf, nick, role, inst):
		if role == aRoles[2]:
			BsNick = get_nick(conf)
			if ChatsAttrs[conf]["laws"]["sparta"]:
				jid = self.get_server(inst)
				if jid not in self.GoodServers__(conf):
					Reason = ("%s: This is SPARTA!!" % BsNick)
					Chats[conf].outcast(jid, Reason); Chats[conf].kick(nick, Reason)
			elif ChatsAttrs[conf]["laws"]["awipe"]:
				Time = time.time()
				if (Time - Chats[conf].sdate) >= 60:
					difference = (Time - self.Antiwipe[conf]["ltime"])
					if difference > 360 and self.Antiwipe[conf]["clear"]:
						sThread(self.awipeClear.func_name, self.awipeClear, (conf, self.Antiwipe[conf]["clear"],))
					if difference > 15:
						self.Antiwipe[conf]["ltime"] = Time
						self.Antiwipe[conf]["jids"] = [inst]
					else:
						self.Antiwipe[conf]["jids"].append(inst)
						joined = self.Antiwipe[conf]["jids"]
						Numb = len(joined)
						if Numb >= 3:
							self.Antiwipe[conf]["ltime"] = Time
							jid = self.get_server(inst)
							if jid == self.get_server(joined[Numb - 2]) and jid == self.get_server(joined[Numb - 3]):
								if jid not in self.GoodServers__(conf):
									ls = []
									for sUser in Chats[conf].get_users():
										if sUser.source and sUser.ishere:
											if sUser.nick != BsNick and sUser.role[0] == aRoles[2]:
												if jid == self.get_server(sUser.source):
													if self.Prison[conf].has_key(sUser.source):
														if not self.Prison[conf][sUser.source].verif:
															ls.append(sUser)
									Chats[conf].outcast(jid, self.AnsBase[12] % (BsNick))
									if ls:
										for sUser in ls:
											Chats[conf].kick(sUser.nick, self.AnsBase[12] % (BsNick))
								else:
									for sUser in Chats[conf].get_users():
										if sUser.source and sUser.ishere:
											if sUser.nick != BsNick and sUser.role[0] == aRoles[2]:
												if jid == self.get_server(sUser.source):
													if self.Prison[conf].has_key(sUser.source):
														if not self.Prison[conf][sUser.source].verif:
															self.Antiwipe[conf]["clear"].append(sUser.source)
															Chats[conf].outcast(sUser.source, self.AnsBase[12] % (BsNick))
							else:
								self.Antiwipe[conf]["clear"].append(inst)
								Chats[conf].outcast(inst, self.AnsBase[12] % (BsNick))
							raise iThr.ThrKill("exit")

	Questions = []

	def sheriff_04eh(self, conf, nick, source_, role, stanza, disp):
		if source_ and nick != get_nick(conf):
			access = get_access(conf, nick)
			if access <= self.sheriffs_loyalty(conf)[1]:
				prisoner = self.Prison[conf].get(source_)
				if prisoner:
					prisoner.addPrTime()
					if prisoner.devoice:
						eTime = prisoner.getDevoice()
						if (eTime < ChatsAttrs[conf]["laws"]["dtime"]):
							Chats[conf].visitor(nick, self.AnsBase[11] % get_nick(conf))
							Message("%s/%s" % (conf, nick), self.AnsBase[14] % Time2Text(ChatsAttrs[conf]["laws"]["dtime"] - eTime), disp)
						else:
							prisoner.devoice = 0
				else:
					self.Prison[conf][source_] = prisoner = self.Convict()
				if not prisoner.verif and access >= 2:
					prisoner.autenticated()
				self.check_wipe(conf, nick, role[0], source_)
				self.check_nick(conf, nick)
				if ChatsAttrs[conf]["laws"]["verif"] and access < 2 and aRoles[2] == role[0]:
					if not prisoner.verif and not prisoner.devoice:
						Chats[conf].visitor(nick, self.AnsBase[17] % get_nick(conf))
						if not self.Questions:
							for qu in self.AnsBase[19].splitlines():
								qu, an = qu.split(chr(124), 1)
								self.Questions.append((qu.strip(), (an.strip()).lower()))
						qu, an = choice(self.Questions)
						prisoner.vakey = an
						Message("%s/%s" % (conf, nick), self.AnsBase[18] % (qu), disp)
						del qu, an
				list = prisoner.prdates
				if len(list) >= 4:
					if (list[-1] - list[0]) <= 10:
						prisoner.prdates = [list.pop()]
						self.special_kick(conf, nick, self.AnsBase[13])
					else:
						prisoner.prdates.pop(0)
				del list
				status = stanza.getStatus()
				if status:
					if ChatsAttrs[conf]["laws"]["tiser"]:
						if self.tiser_checker(status):
							self.special_kick(conf, nick, self.AnsBase[4])
					if ChatsAttrs[conf]["laws"]["obscene"]:
						if self.obscene_checker(status):
							self.special_kick(conf, nick, self.AnsBase[8])
					if ChatsAttrs[conf]["laws"]["prlen"]:
						if len(status) > ChatsAttrs[conf]["laws"]["prlen"]:
							self.special_kick(conf, nick, self.AnsBase[9])

	def sheriff_05eh(self, conf, nick, sbody, scode, disp):
		if nick != get_nick(conf):
			source_ = get_source(conf, nick)
			if source_:
				prisoner = self.Prison[conf].get(source_)
				if prisoner:
					if not Chats[conf].isModer or scode in (sCodes[0], sCodes[3]):
						del self.Prison[conf][source_]
					else:
						prisoner.leaved()
						if scode == sCodes[2] and prisoner.kicks.plus() >= ChatsAttrs[conf]["laws"]["aban"]:
							if ChatsAttrs[conf]["laws"]["aban"]:
								del self.Prison[conf][source_]
								Chats[conf].outcast(source_, self.AnsBase[10] % (get_nick(conf), ChatsAttrs[conf]["laws"]["aban"]))

	def sheriff_06eh(self, conf, old_nick, nick, disp):
		if nick != get_nick(conf) and Chats[conf].isModer:
			sUser = Chats[conf].get_user(nick)
			if getattr(sUser, "source", None):
				prisoner = self.Prison[conf].get(sUser.source)
				if prisoner:
					prisoner.addPrTime()
					self.check_wipe(conf, nick, sUser.role[0], sUser.source)
					self.check_nick(conf, nick)
					list = prisoner.prdates
					if len(list) >= 4:
						if (list[-1] - list[0]) <= 10:
							prisoner.prdates = [list.pop()]
							self.special_kick(conf, nick, self.AnsBase[13])
						else:
							prisoner.prdates.pop(0)

	def sheriff_07eh(self, conf, nick, role, disp):
		if nick != get_nick(conf):
			sUser = Chats[conf].get_user(nick)
			if getattr(sUser, "source", None):
				prisoner = ((sUser.access <= self.sheriffs_loyalty(conf)[1]) and Chats[conf].isModer)
				if self.Prison[conf].has_key(sUser.source):
					if not prisoner:
						del self.Prison[conf][sUser.source]
				elif prisoner:
					self.Prison[conf][sUser.source] = self.Convict()

	def sheriff_08eh(self, conf, nick, stanza, disp):
		if nick != get_nick(conf) and Chats[conf].isModer:
			source_ = get_source(conf, nick)
			if source_:
				prisoner = self.Prison[conf].get(source_)
				if prisoner:
					prisoner.addPrTime()
					list = prisoner.prdates
					if len(list) >= 4:
						if (list[-1] - list[0]) <= 10:
							prisoner.prdates = [list.pop()]
							self.special_kick(conf, nick, self.AnsBase[13])
						else:
							prisoner.prdates.pop(0)
					del list
					status = stanza.getStatus()
					if status:
						if ChatsAttrs[conf]["laws"]["tiser"]:
							if self.tiser_checker(status):
								self.special_kick(conf, nick, self.AnsBase[4])
						if ChatsAttrs[conf]["laws"]["obscene"]:
							if self.obscene_checker(status):
								self.special_kick(conf, nick, self.AnsBase[8])
						if ChatsAttrs[conf]["laws"]["prlen"]:
							if len(status) > ChatsAttrs[conf]["laws"]["prlen"]:
								self.special_kick(conf, nick, self.AnsBase[9])

	def sheriff_01si(self, conf):
		self.Prison[conf] = {}
		self.Antiwipe[conf] = {"ltime": 0, "jids": [], "clear": []}
		if not ChatsAttrs.has_key(conf):
			ChatsAttrs[conf] = {}
		ChatsAttrs[conf]["laws"] = {"awipe": True, "space": True, "verif": False, "tiser": True, "obscene": False, "lower": False, "sparta": False, "list": [], "dtime": 180, "loyalty": 1, "aban": 3, "prlen": 256, "lnick": 24, "len": 1024}
		Name = chat_file(conf, self.LawsFile)
		if initialize_file(Name, str(ChatsAttrs[conf]["laws"])):
			ChatsAttrs[conf]["laws"] = eval(get_file(Name))

	def sheriff_04si(self, conf):
		del self.Prison[conf]
		del self.Antiwipe[conf]

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
