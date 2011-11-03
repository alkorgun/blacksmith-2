# coding: utf-8

#  BlackSmith mark.2
exp_name = "sheriff" # /code.py v.x4
#  Id: 15~4a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

GoodServers = ["jabber.ru", "xmpp.ru", "jabbers.ru", "xmpps.ru", "talkonaut.com", "jabber.org", "gtalk.com", "gmail.com", "jabberon.ru", "gajim.org", "jabbrik.ru", "worldskynet.net", "veganet.org", "qip.ru", "blackfishka.ru", "ya.ru"]

if DefLANG != "RU":
	GoodServers += ["jabber.com", "xmpp.com", "jabber.uk", "jabberworld.net"]

LawsFile = "laws.db"

Federal_Jail, Antiwipe = {}, {}

class rUser:

	def __init__(self):
		self.devoice = 0
		self.prdates = [time.time()]
		self.msdates = []
		self.offenses = 0
		self.verif = False
		self.kicks = itypes.Number()
		self.vakey = ""
		self.vnumb = itypes.Number()

	def Autenticated(self):
		self.verif = True
		self.vakey = ""
		delattr(self, "vnumb")

	def leaved(self):
		self.msdates = []
		self.vakey = ""

	def SetDevoice(self):
		self.devoice = time.time()

	GetDevoice = lambda self: (time.time() - self.devoice)

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
				elif Name in ("awipe", "антивайп".decode("utf-8")):
					answer = change_cfg(source[1], "awipe", mode)
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
			if ChatsAttrs[source[1]]["laws"]["awipe"]:
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
	for dkey in ["@", "conf", "ence"]:
		if body.count(dkey):
			c1 += 1
	for dkey in ["http", "//", "www"]:
		if body.count(dkey):
			c2 += 1
	if c1 == 3 or c2 > 1:
		return True
	return False

def obscene_checker(body):
	body = " %s " % body.lower()
	for dkey in SheriffAnsBase[33].split(chr(47)):
		if body.count(dkey):
			return True
	return False

def lower_checker(conf, body):
	Numb, body = 0, sub_desc(body, [chr(32), chr(10), chr(13), chr(9)] + Chats[conf].get_nicks()).strip()
	for char in list(body):
		if char.isupper():
			Numb += 1
	if Numb > 12 and Numb > (len(body) / 3):
		return True
	return False

def check_nick(conf, nick):

	def nick_checker(conf, nick):
		nick = nick.lower()
		for dkey in ("%s", "%d", "%i", "%f"):
			if nick.count(dkey):
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
		prisoner = Federal_Jail[source[1]].get(source_)
		if prisoner:
			prisoner.offenses += 1
			if prisoner.offenses in (1, 2):
				Answer(body, ltype, source, disp)
				raise iThr.ThrKill("exit")
			elif prisoner.offenses == 3:
				Chats[source[1]].visitor(source[2], "%s: %s" % (get_self_nick(source[1]), body))
				prisoner.SetDevoice()
				Msend(source[0], SheriffAnsBase[16] % (body, ChatsAttrs[source[1]]["laws"]["dtime"]), disp)
				raise iThr.ThrKill("exit")
			else:
				prisoner.SetDevoice()
				spesial_kick(source[1], source[2], body)
		else:
			spesial_kick(source[1], source[2], body)
	else:
		Answer(body, ltype, source, disp)
		raise iThr.ThrKill("exit")

def Security_01eh(stanza, isConf, ltype, source, body, isToBs, disp):
	if isConf and source[2] and Chats[source[1]].isModer:
		source_ = get_source(source[1], source[2])
		if source_:
			loyalty, access = sheriffs_loyalty(source[1]), get_access(source[1], source[2])
			if access <= loyalty[0]:
				prisoner = Federal_Jail[source[1]].get(source_)
				if prisoner:
					prisoner.addMsTime()
					if ChatsAttrs[source[1]]["laws"]["tiser"]:
						if tiser_checker(body):
							if access <= loyalty[1]:
								if prisoner:
									prisoner.SetDevoice()
								spesial_kick(source[1], source[2], SheriffAnsBase[4])
							else:
								Answer(SheriffAnsBase[4], ltype, source, disp)
							raise iThr.ThrKill("exit")
					if ChatsAttrs[source[1]]["laws"]["verif"]:
						if access < 2 and prisoner.vakey and ltype == Types[0]:
							if prisoner.vakey == body.lower():
								prisoner.Autenticated()
								Chats[source[1]].participant(source[2], SheriffAnsBase[20] % get_self_nick(source[1]))
								Msend(source[0], SheriffAnsBase[21], disp)
							elif prisoner.vnumb.plus() >= 3:
								prisoner.vnumb = itypes.Number()
								spesial_kick(source[1], source[2], SheriffAnsBase[22])
							else:
								Msend(source[0], SheriffAnsBase[23], disp)
							raise iThr.ThrKill("exit")
					list = getattr(prisoner, "msdates")
					if len(list) >= 4:
						if (list[-1] - list[0]) <= 6:
							prisoner.msdates = [list.pop()]
							prisoner.SetDevoice()
							spesial_kick(source[1], source[2], SheriffAnsBase[15])
						else:
							prisoner.msdates.pop(0)
					del list
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

def AwipeClear(conf, list):
	if Chats.has_key(conf):
		Antiwipe[conf]["clear"] = []
		for sUser in Chats[conf].get_users():
			if sUser.source in list:
				if not sUser.ishere:
					if Chats[conf].isHere(sUser.nick):
						del Chats[conf].desc[sUser.nick]
					if Federal_Jail[conf].has_key(sUser.source):
						del Federal_Jail[conf][sUser.source]
		for source_ in list:
			Chats[conf].none(source_); time.sleep(0.4)

def get_server(source, state = 0):
	At = chr(64)
	if source.count(At):
		source = source.split(At)[1]
		if state:
			source = source.split(chr(46), 1)[1]
	return source

GoodServers__ = lambda conf: (GoodServers + ChatsAttrs[conf]["laws"]["list"] + [get_server(conf, True)])

def check_wipe(conf, nick, role, inst):
	if role == AflRoles[2]:
		BsNick = get_self_nick(conf)
		if ChatsAttrs[conf]["laws"]["sparta"]:
			jid = get_server(inst)
			if jid not in GoodServers__(conf):
				Reason = ("%s: This is SPARTA!!" % BsNick)
				Chats[conf].ban(jid, Reason); Chats[conf].kick(nick, Reason)
		elif ChatsAttrs[conf]["laws"]["awipe"]:
			NowTime = time.time()
			if (NowTime - Chats[conf].sdate) >= 60:
				difference = (NowTime - Antiwipe[conf]["ltime"])
				if difference > 360 and Antiwipe[conf]["clear"]:
					sThread(AwipeClear.func_name, AwipeClear, (conf, Antiwipe[conf]["clear"],))
				if difference > 15:
					Antiwipe[conf]["ltime"] = NowTime
					Antiwipe[conf]["jids"] = [inst]
				else:
					Antiwipe[conf]["jids"].append(inst)
					joined = Antiwipe[conf]["jids"]
					Numb = len(joined)
					if Numb >= 3:
						Antiwipe[conf]["ltime"] = NowTime
						jid = get_server(inst)
						if jid == get_server(joined[Numb - 2]) and jid == get_server(joined[Numb - 3]):
							if jid not in GoodServers__(conf):
								ls = []
								for sUser in Chats[conf].get_users():
									if sUser.source and sUser.ishere:
										if sUser.nick != BsNick and sUser.role[0] == AflRoles[2]:
											if jid == get_server(sUser.source):
												if Federal_Jail[conf].has_key(sUser.source):
													if not Federal_Jail[conf][sUser.source].verif:
														ls.append(sUser)
								Chats[conf].ban(jid, SheriffAnsBase[12] % (BsNick))
								if ls:
									for sUser in ls:
										Chats[conf].kick(sUser.nick, SheriffAnsBase[12] % (BsNick))
							else:
								for sUser in Chats[conf].get_users():
									if sUser.source and sUser.ishere:
										if sUser.nick != BsNick and sUser.role[0] == AflRoles[2]:
											if jid == get_server(sUser.source):
												if Federal_Jail[conf].has_key(sUser.source):
													if not Federal_Jail[conf][sUser.source].verif:
														Antiwipe[conf]["clear"].append(sUser.source)
														Chats[conf].ban(sUser.source, SheriffAnsBase[12] % (BsNick))
						else:
							Antiwipe[conf]["clear"].append(inst)
							Chats[conf].ban(inst, SheriffAnsBase[12] % (BsNick))
						raise iThr.ThrKill("exit")

def Security_04eh(conf, nick, source_, role, stanza, disp):
	if source_ and nick != get_self_nick(conf):
		access = get_access(conf, nick)
		if access <= sheriffs_loyalty(conf)[1]:
			prisoner = Federal_Jail[conf].get(source_)
			if prisoner:
				prisoner.addPrTime()
				if prisoner.devoice:
					eTime = prisoner.GetDevoice()
					if (eTime < ChatsAttrs[conf]["laws"]["dtime"]):
						Chats[conf].visitor(nick, SheriffAnsBase[11] % get_self_nick(conf))
						Msend("%s/%s" % (conf, nick), SheriffAnsBase[14] % Time2Text(ChatsAttrs[conf]["laws"]["dtime"] - eTime), disp)
					else:
						prisoner.devoice = 0
			else:
				Federal_Jail[conf][source_] = prisoner = rUser()
			if not prisoner.verif and access >= 2:
				prisoner.Autenticated()
			check_wipe(conf, nick, role[0], source_)
			check_nick(conf, nick)
			if ChatsAttrs[conf]["laws"]["verif"] and access < 2 and AflRoles[2] == role[0]:
				if not prisoner.verif and not prisoner.devoice:
					Chats[conf].visitor(nick, SheriffAnsBase[17] % get_self_nick(conf))
					ques = choice(SheriffAnsBase[19].splitlines())
					ques = ques.split(chr(124), 1)
					prisoner.vakey = (ques[1].strip()).lower()
					Msend("%s/%s" % (conf, nick), SheriffAnsBase[18] % (ques[0].strip()), disp)
					del ques
			list = getattr(prisoner, "prdates")
			if len(list) >= 4:
				if (list[-1] - list[0]) <= 10:
					prisoner.prdates = [list.pop()]
					spesial_kick(conf, nick, SheriffAnsBase[13])
				else:
					prisoner.prdates.pop(0)
			del list
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

def Security_05eh(conf, nick, sbody, scode, disp):
	if nick != get_self_nick(conf):
		source_ = get_source(conf, nick)
		if source_:
			prisoner = Federal_Jail[conf].get(source_)
			if prisoner:
				if not Chats[conf].isModer or scode in (sCodes[0], sCodes[3]):
					del Federal_Jail[conf][source_]
				else:
					prisoner.leaved()
					if scode == sCodes[2] and prisoner.kicks.plus() >= ChatsAttrs[conf]["laws"]["aban"]:
						if ChatsAttrs[conf]["laws"]["aban"]:
							del Federal_Jail[conf][source_]
							Chats[conf].ban(source_, SheriffAnsBase[10] % (get_self_nick(conf), ChatsAttrs[conf]["laws"]["aban"]))

def Security_06eh(conf, old_nick, nick, disp):
	if nick != get_self_nick(conf) and Chats[conf].isModer:
		sUser = Chats[conf].get_user(nick)
		if getattr(sUser, "source", 0):
			prisoner = Federal_Jail[conf].get(sUser.source)
			if prisoner:
				prisoner.addPrTime()
				check_wipe(conf, nick, sUser.role[0], sUser.source)
				check_nick(conf, nick)
				list = getattr(prisoner, "prdates")
				if len(list) >= 4:
					if (list[-1] - list[0]) <= 10:
						prisoner.prdates = [list.pop()]
						spesial_kick(conf, nick, SheriffAnsBase[13])
					else:
						prisoner.prdates.pop(0)

def Security_07eh(conf, nick, role, disp):
	if nick != get_self_nick(conf):
		sUser = Chats[conf].get_user(nick)
		if getattr(sUser, "source", 0):
			prisoner = ((sUser.access <= sheriffs_loyalty(conf)[1]) and Chats[conf].isModer)
			if Federal_Jail[conf].has_key(sUser.source):
				if not prisoner:
					del Federal_Jail[conf][sUser.source]
			elif prisoner:
				Federal_Jail[conf][sUser.source] = rUser()

def Security_08eh(conf, nick, stanza, disp):
	if nick != get_self_nick(conf) and Chats[conf].isModer:
		source_ = get_source(conf, nick)
		if source_:
			prisoner = Federal_Jail[conf].get(source_)
			if prisoner:
				prisoner.addPrTime()
				list = getattr(prisoner, "prdates")
				if len(list) >= 4:
					if (list[-1] - list[0]) <= 10:
						prisoner.prdates = [list.pop()]
						spesial_kick(conf, nick, SheriffAnsBase[13])
					else:
						prisoner.prdates.pop(0)
				del list
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

def Security_01si(conf):
	Federal_Jail[conf] = {}
	Antiwipe[conf] = {"ltime": 0, "jids": [], "clear": []}
	if not ChatsAttrs.has_key(conf):
		ChatsAttrs[conf] = {}
	ChatsAttrs[conf]["laws"] = {"awipe": True, "space": True, "verif": False, "tiser": True, "obscene": False, "lower": False, "sparta": False, "list": [], "dtime": 180, "loyalty": 1, "aban": 3, "prlen": 256, "lnick": 24, "len": 1024}
	Name = chat_file(conf, LawsFile)
	if initialize_file(Name, str(ChatsAttrs[conf]["laws"])):
		ChatsAttrs[conf]["laws"] = eval(get_file(Name))
		if not ChatsAttrs[conf]["laws"].has_key("list"):
			ChatsAttrs[conf]["laws"]["sparta"] = False
			ChatsAttrs[conf]["laws"]["list"] = []
			cat_file(Name, str(ChatsAttrs[conf]["laws"]))
		if ChatsAttrs[conf]["laws"].has_key("avipe"):
			Awipe = ChatsAttrs[conf]["laws"].pop("avipe")
			ChatsAttrs[conf]["laws"]["awipe"] = Awipe
			cat_file(Name, str(ChatsAttrs[conf]["laws"]))

def Security_04si(conf):
	del Federal_Jail[conf]
	del Antiwipe[conf]

expansions[exp_name].funcs_add([command_order, spesial_kick, sheriffs_loyalty, tiser_checker, obscene_checker, lower_checker, check_nick, sheriff_set, AwipeClear, get_server, check_wipe, Security_01eh, Security_04eh, Security_05eh, Security_06eh, Security_07eh, Security_08eh, Security_01si, Security_04si])
expansions[exp_name].ls.extend(["SheriffAnsBase", "GoodServers", "LawsFile", "Federal_Jail", "Antiwipe", rUser.__name__, "GoodServers__"])

command_handler(command_order, {"RU": "ордер", "EN": "order"}, 6, exp_name)

handler_register(Security_01si, "01si", exp_name)
handler_register(Security_04si, "04si", exp_name)
handler_register(Security_01eh, "01eh", exp_name)
handler_register(Security_04eh, "04eh", exp_name)
handler_register(Security_05eh, "05eh", exp_name)
handler_register(Security_06eh, "06eh", exp_name)
handler_register(Security_07eh, "07eh", exp_name)
handler_register(Security_08eh, "08eh", exp_name)
