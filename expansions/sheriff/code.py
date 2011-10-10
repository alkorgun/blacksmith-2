# coding: utf-8

#  BlackSmith mark.2
exp_name = "sheriff" # /code.py v.x3
#  Id: 15~3a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

GoodServers = ["jabber.ru", "xmpp.ru", "jabbers.ru", "xmpps.ru", "talkonaut.com", "jabber.org", "gtalk.com", "gmail.com", "jabberon.ru", "gajim.org", "jabbrik.ru", "worldskynet.net", "veganet.org", "qip.ru", "blackfishka.ru", "ya.ru"]

if DefLANG != "RU":
	GoodServers += ["jabber.com", "xmpp.com", "jabber.uk", "jabberworld.net"]

LawsFile = "laws.db"

Federal_Jail, Antivipe = {}, {}

class rUser:

	def __init__(self, joined):
		self.ishere = True
		self.devoice = 0
		self.prdates = [joined]
		self.msdates = []
		self.offenses = 0
		self.verif = False
		self.kicks = 0
		self.vakey = ""
		self.vnumb = itypes.Number()

	def Autenticated(self):
		self.verif = True
		self.vakey = ""
		del self.vnumb

	def leaved(self):
		self.ishere = False
		self.msdates = []
		self.vakey = ""

	def SetDevoice(self):
		self.devoice = time.time()

	def GetDevoice(self):
		return (time.time() - self.devoice)

	def addPrTime(self):
		self.prdates.append(time.time())

	def addMsTime(self):
		self.msdates.append(time.time())

def command_order(ltype, source, body, disp):

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
								if jid not in (GoodServers + ChatsAttrs[source[1]]["laws"]["list"]):
									ChatsAttrs[source[1]]["laws"]["list"].append(jid)
									answer = AnsBase[4]
								else:
									answer = SheriffAnsBase[34]
							elif mode in ("del", "-"):
								if ChatsAttrs[source[1]]["laws"]["list"].count(jid):
									ChatsAttrs[source[1]]["laws"]["list"].remove(jid)
									answer = AnsBase[4]
								else:
									answer = SheriffAnsBase[35]
							else:
								answer = AnsBase[2]
						else:
							answer = SheriffAnsBase[36]
					else:
						answer = AnsBase[2]
				elif Name in ("avipe", "антивайп".decode("utf-8")):
					answer = change_cfg(source[1], "avipe", mode)
				elif Name in ("aspace", "антиспэйс".decode("utf-8")):
					answer = change_cfg(source[1], "space", mode)
				elif Name in ("sparta", "спарта".decode("utf-8")):
					answer = change_cfg(source[1], "space", mode)
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
					cat_file(chat_file(source[1], LawsFile), str(ChatsAttrs[source[1]]["laws"]))
			elif Name in ("servers", "сервера".decode("utf-8")):
				answer = "\nDefault:\n%s" % enumerated_list(sorted(GoodServers))
				if ChatsAttrs[source[1]]["laws"]["list"]:
					answer += "\n\nDefined:\n%s" % enumerated_list(sorted(ChatsAttrs[source[1]]["laws"]["list"]))
			else:
				answer = AnsBase[2]
		else:
			answer = SheriffAnsBase[24]
			if ChatsAttrs[source[1]]["laws"]["space"]:
				answer += SheriffAnsBase[25][:-1]
			else:
				answer += SheriffAnsBase[26][:-1]
			answer += SheriffAnsBase[27] % (ChatsAttrs[source[1]]["laws"]["lnick"])
			if ChatsAttrs[source[1]]["laws"]["avipe"]:
				answer += SheriffAnsBase[25]
			else:
				answer += SheriffAnsBase[26]
			answer += SheriffAnsBase[28] % (ChatsAttrs[source[1]]["laws"]["aban"])
			if ChatsAttrs[source[1]]["laws"]["verif"]:
				answer += SheriffAnsBase[25]
			else:
				answer += SheriffAnsBase[26]
			answer += SheriffAnsBase[29] % (ChatsAttrs[source[1]]["laws"]["loyalty"])
			if ChatsAttrs[source[1]]["laws"]["tiser"]:
				answer += SheriffAnsBase[25]
			else:
				answer += SheriffAnsBase[26]
			answer += SheriffAnsBase[30] % (ChatsAttrs[source[1]]["laws"]["dtime"])
			if ChatsAttrs[source[1]]["laws"]["obscene"]:
				answer += SheriffAnsBase[25][:-1]
			else:
				answer += SheriffAnsBase[26][:-1]
			answer += SheriffAnsBase[31] % (ChatsAttrs[source[1]]["laws"]["len"])
			if ChatsAttrs[source[1]]["laws"]["lower"]:
				answer += SheriffAnsBase[25][:-1]
			else:
				answer += SheriffAnsBase[26][:-1]
			answer += SheriffAnsBase[32] % (ChatsAttrs[source[1]]["laws"]["prlen"])
			if ChatsAttrs[source[1]]["laws"]["sparta"]:
				answer += SheriffAnsBase[25][:-1]
			else:
				answer += SheriffAnsBase[26][:-1]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def spesial_kick(conf, nick, text):
	Chats[conf].kick(nick, "%s: %s" % (get_self_nick(conf), text))
	raise iThr.ThrKill("exit")

def sheriffs_loyalty(conf):
	access = loy = ChatsAttrs[conf]["laws"]["loyalty"]
	if access > 2:
		access = 2
	return (loy, access)

def tiser_checker(body):
	body = body.lower()
	c1, c2 = 0, 0
	for x in ["@", "conf", "ence"]:
		if body.count(x):
			c1 += 1
	for x in ["http", "//", "www"]:
		if body.count(x):
			c2 += 1
	if c1 == 3 or c2 > 1:
		return True
	return False

def obscene_checker(body):
	body = " %s " % body.lower()
	for x in SheriffAnsBase[33].split("/"):
		if body.count(x):
			return True
	return False

def lower_checker(conf, body):
	Numb, body = 0, sub_desc(body, [chr(32), chr(10), chr(13), chr(9)] + Chats[conf].get_nicks()).strip()
	for x in list(body):
		if x.isupper():
			Numb += 1
	if Numb > 12 and Numb > (len(body) / 3):
		return True
	return False

def check_nick(conf, nick):

	def nick_checker(conf, nick):
		nick = nick.lower()
		for x in ["%s", "%d", "%i", "%f"]:
			if nick.count(x):
				return True
		nick = nick.split()[0]
		if nick in Cmds.keys():
			return True
		if Chats[conf].cPref and nick.startswith(Chats[conf].cPref):
			if nick[1:] in Cmds.keys():
				return True
		return False

	if (nick.strip()):
		if len(nick) > ChatsAttrs[conf]["laws"]["lnick"]:
			spesial_kick(conf, nick, SheriffAnsBase[0] % (ChatsAttrs[conf]["laws"]["lnick"]))
		if nick_checker(conf, nick):
			spesial_kick(conf, nick, SheriffAnsBase[1])
		if ChatsAttrs[conf]["laws"]["space"]:
			if len(nick) != len(nick.strip()):
				spesial_kick(conf, nick, SheriffAnsBase[2])
		if ChatsAttrs[conf]["laws"]["obscene"]:
			if obscene_checker(nick):
				spesial_kick(conf, nick, SheriffAnsBase[3])

def sheriff_set(ltype, source, source_, access, loyalty, body, disp):
	if access <= loyalty:
		if Federal_Jail[source[1]].has_key(source_):
			Federal_Jail[source[1]][source_].offenses += 1
			if Federal_Jail[source[1]][source_].offenses in (1, 2):
				Answer(body, ltype, source, disp)
				raise iThr.ThrKill("exit")
			elif Federal_Jail[source[1]][source_].offenses == 3:
				Chats[source[1]].visitor(source[2], "%s: %s" % (get_self_nick(source[1]), body))
				Federal_Jail[source[1]][source_].SetDevoice()
				Msend(source[0], SheriffAnsBase[16] % (body, ChatsAttrs[source[1]]["laws"]["dtime"]), disp)
				raise iThr.ThrKill("exit")
			else:
				Federal_Jail[source[1]][source_].SetDevoice()
				spesial_kick(source[1], source[2], body)
		else:
			spesial_kick(source[1], source[2], body)
	else:
		Answer(body, ltype, source, disp)
		raise iThr.ThrKill("exit")

def Security_01eh(stanza, isConf, ltype, source, body, isToBs, disp):
	if isConf and source[2] and Chats[source[1]].isModer:
		loyalty, access = sheriffs_loyalty(source[1]), get_access(source[1], source[2])
		if access <= loyalty[0]:
			source_ = get_source(source[1], source[2])
			if ChatsAttrs[source[1]]["laws"]["tiser"]:
				if tiser_checker(body):
					if access <= loyalty[1]:
						if Federal_Jail[source[1]].has_key(source_):
							Federal_Jail[source[1]][source_].SetDevoice()
						spesial_kick(source[1], source[2], SheriffAnsBase[4])
					else:
						Answer(SheriffAnsBase[4], ltype, source, disp)
					raise iThr.ThrKill("exit")
			if Federal_Jail[source[1]].has_key(source_):
				if ChatsAttrs[source[1]]["laws"]["verif"]:
					if access < 2 and Federal_Jail[source[1]][source_].vakey and ltype == Types[0]:
						if Federal_Jail[source[1]][source_].vakey == body.lower():
							Federal_Jail[source[1]][source_].Autenticated()
							Chats[source[1]].participant(source[2], SheriffAnsBase[20] % get_self_nick(source[1]))
							Msend(source[0], SheriffAnsBase[21], disp)
						elif Federal_Jail[source[1]][source_].vnumb.plus() >= 3:
							Federal_Jail[source[1]][source_].vnumb = itypes.Number()
							spesial_kick(source[1], source[2], SheriffAnsBase[22])
						else:
							Msend(source[0], SheriffAnsBase[23], disp)
						raise iThr.ThrKill("exit")
				Federal_Jail[source[1]][source_].addMsTime()
				list = Federal_Jail[source[1]][source_].msdates
				len_msg = len(list)
				if len_msg >= 4:
					if (list[len_msg - 1] - list[0]) <= 6:
						Federal_Jail[source[1]][source_].msdates = [list[len_msg - 1]]
						Federal_Jail[source[1]][source_].SetDevoice()
						spesial_kick(source[1], source[2], SheriffAnsBase[15])
					else:
						Federal_Jail[source[1]][source_].msdates.pop(0)
				del list, len_msg
			if ltype == Types[1]:
				if ChatsAttrs[source[1]]["laws"]["obscene"]:
					if obscene_checker(body):
						sheriff_set(ltype, source, source_, access, loyalty[1], SheriffAnsBase[5], disp)
				if ChatsAttrs[source[1]]["laws"]["len"]:
					if len(body) > ChatsAttrs[source[1]]["laws"]["len"]:
						sheriff_set(ltype, source, source_, access, loyalty[1], SheriffAnsBase[6], disp)
				if ChatsAttrs[source[1]]["laws"]["lower"]:
					if lower_checker(source[1], body):
						sheriff_set(ltype, source, source_, access, loyalty[1], SheriffAnsBase[7], disp)

def AvipeClear(conf, list):
	if Chats.has_key(conf):
		Antivipe[conf]["clear"] = []
		for sUser in Chats[conf].get_users():
			if sUser.source in list:
				if sUser.ishere:
					if Chats[conf].isHere(sUser.nick):
						del Chats[conf].users[sUser.nick]
					if Federal_Jail[conf].has_key(sUser.source):
						del Federal_Jail[conf][sUser.source]
		for User in list:
			Chats[conf].none(User)
			time.sleep(0.4)

def get_server(source, state = 0):
	if source.count(chr(64)):
		source = source.split(chr(64))[1]
		if state:
			source = source.split(chr(46), 1)[1]
	return source

GoodServers__ = lambda conf: (GoodServers + ChatsAttrs[conf]["laws"]["list"] + [get_server(conf, True)])

def antivipe_func(conf, nick, role, source):
	if Chats[conf].isModer and role == AflRoles[2]:
		BsNick = get_self_nick(conf)
		if ChatsAttrs[conf]["laws"]["sparta"]:
			jid = get_server(source)
			if jid not in GoodServers__(conf):
				Reason = ("%s: This is SPARTA!!" % BsNick)
				Chats[conf].ban(jid, Reason); Chats[conf].kick(nick, Reason)
		elif ChatsAttrs[conf]["laws"]["avipe"]:
			NowTime = time.time()
			if (NowTime - Chats[conf].sdate) >= 60:
				difference = (NowTime - Antivipe[conf]["ltime"])
				if difference > 360 and Antivipe[conf]["clear"]:
					sThread(AvipeClear.func_name, AvipeClear, (conf, Antivipe[conf]["clear"],))
				if difference > 15:
					Antivipe[conf]["ltime"] = NowTime
					Antivipe[conf]["jids"] = [source,]
				else:
					Antivipe[conf]["jids"].append(source)
					joined = Antivipe[conf]["jids"]
					Numb = len(joined)
					if Numb >= 3:
						Antivipe[conf]["ltime"] = NowTime
						jid = get_server(source)
						if jid == get_server(joined[Numb - 2]) and jid == get_server(joined[Numb - 3]):
							if jid not in GoodServers__(conf):
								Chats[conf].ban(jid, SheriffAnsBase[12] % (BsNick))
								for sUser in Chats[conf].get_users():
									if sUser.source and sUser.ishere:
										if sUser.nick != BsNick and sUser.role[0] == AflRoles[2]:
											if jid == get_server(sUser.source):
												if Federal_Jail[conf].has_key(sUser.source):
													if not Federal_Jail[conf][sUser.source].verif:
														Chats[conf].kick(sUser.nick, SheriffAnsBase[12] % (BsNick))
							else:
								for sUser in Chats[conf].get_users():
									if sUser.source and sUser.ishere:
										if sUser.nick != BsNick and sUser.role[0] == AflRoles[2]:
											if jid == get_server(sUser.source):
												if Federal_Jail[conf].has_key(sUser.source):
													if not Federal_Jail[conf][sUser.source].verif:
														Antivipe[conf]["clear"].append(sUser.source)
														Chats[conf].ban(sUser.source, SheriffAnsBase[12] % (BsNick))
						else:
							Antivipe[conf]["clear"].append(source)
							Chats[conf].ban(source, SheriffAnsBase[12] % (BsNick))
						raise iThr.ThrKill("exit")

def Security_02eh(stanza, disp):
	(source, conf, stype, nick) = sAttrs(stanza)
	if nick != get_self_nick(conf):
		if not Chats[conf].isHere(nick):
			if stype == Types[4] and sCodes[1] == stanza.getStatusCode():
				source_ = stanza.getJid()
				if source_:
					nick = stanza.getNick()
					if get_access(conf, nick) <= sheriffs_loyalty(conf)[1]:
						if not Federal_Jail[conf].has_key(source_):
							Federal_Jail[conf][source_] = rUser(time.time())
						antivipe_func(conf, nick, GetRole(stanza)[0], source_)
						check_nick(conf, nick)
			raise iThr.ThrKill("exit")
		sUser = Chats[conf].get_user(nick)
		if sUser.source:
			relapser = Federal_Jail[conf].has_key(sUser.source)
			if sUser.access <= sheriffs_loyalty(conf)[1]:
				if stype in [Types[3], None]:
					if not relapser:
						Federal_Jail[conf][sUser.source] = rUser(sUser.date[0])
					else:
						Federal_Jail[conf][sUser.source].addPrTime()
					isHere = Federal_Jail[conf][sUser.source].ishere
					if not isHere:
						Federal_Jail[conf][sUser.source].ishere = True
						if Federal_Jail[conf][sUser.source].devoice:
							etime = Federal_Jail[conf][sUser.source].GetDevoice()
							if etime < ChatsAttrs[conf]["laws"]["dtime"]:
								Chats[conf].visitor(nick, SheriffAnsBase[11] % get_self_nick(conf))
								Msend("%s/%s" % (conf, nick), SheriffAnsBase[14] % Time2Text(ChatsAttrs[conf]["laws"]["dtime"] - etime), disp)
							else:
								Federal_Jail[conf][sUser.source].devoice = 0
					if sUser.access >= 2 and not Federal_Jail[conf][sUser.source].verif:
						Federal_Jail[conf][sUser.source].Autenticated()
					if not relapser or not isHere:
						antivipe_func(conf, nick, sUser.role[0], sUser.source)
						check_nick(conf, nick)
						if ChatsAttrs[conf]["laws"]["verif"] and not Federal_Jail[conf][sUser.source].devoice and sUser.access <= 1 and AflRoles[2] == GetRole(stanza)[0]:
							if not Federal_Jail[conf][sUser.source].verif:
								Chats[conf].visitor(nick, SheriffAnsBase[17] % get_self_nick(conf))
								ques = choice(SheriffAnsBase[19].splitlines()).split("|")
								Federal_Jail[conf][sUser.source].vakey = (ques[1].strip()).lower()
								Msend("%s/%s" % (conf, nick), SheriffAnsBase[18] % (ques[0].strip()), disp)
								del ques
					del isHere
					list = Federal_Jail[conf][sUser.source].prdates
					len_prs = len(list)
					if len_prs >= 4:
						if (list[len_prs - 1] - list[0]) <= 10:
							Federal_Jail[conf][sUser.source].prdates = [list[len_prs - 1]]
							spesial_kick(conf, nick, SheriffAnsBase[13])
						else:
							Federal_Jail[conf][sUser.source].prdates.pop(0)
					del list, len_prs
					status = stanza.getStatus()
					if status:
						if ChatsAttrs[conf]["laws"]["tiser"]:
							if tiser_checker(status):
								spesial_kick(conf, nick, SheriffAnsBase[4])
						if ChatsAttrs[conf]["laws"]["obscene"]:
							if obscene_checker(status):
								spesial_kick(conf, nick, SheriffAnsBase[8])
						if ChatsAttrs[conf]["laws"]["prlen"]:
							if len(status) > ChatsAttrs[conf]["laws"]["prlen"]:
								spesial_kick(conf, nick, SheriffAnsBase[9])
				elif stype == Types[4]:
					if relapser:
						scode = stanza.getStatusCode()
						if scode in [sCodes[0], sCodes[3]]:
							del Federal_Jail[conf][sUser.source]
						elif scode == sCodes[2]:
							Federal_Jail[conf][sUser.source].leaved()
							Federal_Jail[conf][sUser.source].kicks += 1
							if ChatsAttrs[conf]["laws"]["aban"] and Chats[conf].isModer:
								if ChatsAttrs[conf]["laws"]["aban"] <= Federal_Jail[conf][sUser.source].kicks:
									del Federal_Jail[conf][sUser.source]
									Chats[conf].ban(sUser.source, SheriffAnsBase[10] % (get_self_nick(conf), ChatsAttrs[conf]["laws"]["aban"]))
						else:
							Federal_Jail[conf][sUser.source].leaved()
			elif relapser:
				del Federal_Jail[conf][sUser.source]

def Security_01si(conf):
	Federal_Jail[conf] = {}
	Antivipe[conf] = {"ltime": 0, "jids": [], "clear": []}
	if not ChatsAttrs.has_key(conf):
		ChatsAttrs[conf] = {}
	ChatsAttrs[conf]["laws"] = {"avipe": True, "space": True, "verif": False, "tiser": True, "obscene": False, "lower": False, "sparta": False, "list": [], "dtime": 180, "loyalty": 1, "aban": 3, "prlen": 256, "lnick": 24, "len": 1024}
	Name = chat_file(conf, LawsFile)
	if initialize_file(Name, str(ChatsAttrs[conf]["laws"])):
		ChatsAttrs[conf]["laws"] = eval(get_file(Name))
		if not ChatsAttrs[conf]["laws"].has_key("list"):
			ChatsAttrs[conf]["laws"]["sparta"] = False
			ChatsAttrs[conf]["laws"]["list"] = []
			cat_file(Name, str(ChatsAttrs[conf]["laws"]))

def Security_04si(conf):
	del Federal_Jail[conf]
	del Antivipe[conf]

expansions[exp_name].funcs_add([command_order, spesial_kick, sheriffs_loyalty, tiser_checker, obscene_checker, lower_checker, check_nick, sheriff_set, AvipeClear, get_server, antivipe_func, Security_01eh, Security_02eh, Security_01si, Security_04si])
expansions[exp_name].ls.extend(["SheriffAnsBase", "GoodServers", "LawsFile", "Federal_Jail", "Antivipe", rUser.__name__, "GoodServers__"])

command_handler(command_order, {"RU": "ордер", "EN": "order"}, 6, exp_name)

handler_register(Security_01si, "01si", exp_name)
handler_register(Security_04si, "04si", exp_name)
handler_register(Security_01eh, "01eh", exp_name)
handler_register(Security_02eh, "02eh", exp_name)
