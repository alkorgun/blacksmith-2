# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "sheriff" # /code.py v.x3
#  Id: 15~3a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

GoodServers = ["jabber.ru", "xmpp.ru", "jabbers.ru", "xmpps.ru", "talkonaut.com", "jabber.org", "gtalk.com", "gmail.com", "jabberon.ru", "gajim.org", "jabbrik.ru", "worldskynet.net", "veganet.org", "qip.ru", "blackfishka.ru", "ya.ru"]

if DefLANG != "RU":
	GoodServers += ["jabber.com", "xmpp.com", "jabber.org", "jabber.uk"]

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

	def change_cfg(conf, key, val):
		if val in ["on", "1", "вкл".decode("utf-8")]:
			ChatsAttrs[conf]["laws"][key] = True
			answer = AnsBase[4]
		elif val in ["off", "0", "выкл".decode("utf-8")]:
			ChatsAttrs[conf]["laws"][key] = False
			answer = AnsBase[4]
		else:
			answer = AnsBase[2]
		return answer

	def alt_change_cfg(conf, key, val, drange):
		if check_number(val):
			val = int(val)
			if val in range(*drange):
				ChatsAttrs[conf]["laws"][key] = val
				answer = AnsBase[4]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[30]
		return answer

	if Chats.has_key(source[1]):
		if body:
			list = body.split()
			if len(list) >= 2:
				key, val = list[0].lower(), list[1].lower()
				if key in ["avipe", "антивайп".decode("utf-8")]:
					answer = change_cfg(source[1], "avipe", val)
				elif key in ["aspace", "антиспэйс".decode("utf-8")]:
					answer = change_cfg(source[1], "space", val)
				elif key in ["verif", "авторизация".decode("utf-8")]:
					answer = change_cfg(source[1], "verif", val)
				elif key in ["atiser", "антиреклама".decode("utf-8")]:
					answer = change_cfg(source[1], "tiser", val)
				elif key in ["aobscene", "антимат".decode("utf-8")]:
					answer = change_cfg(source[1], "obscene", val)
				elif key in ["acaps", "антикапс".decode("utf-8")]:
					answer = change_cfg(source[1], "lower", val)
				elif key in ["lnick", "никлен".decode("utf-8")]:
					answer = alt_change_cfg(source[1], "lnick", val, (12, 33))
				elif key in ["aban", "автобан".decode("utf-8")]:
					answer = alt_change_cfg(source[1], "aban", val, (2, 7))
				elif key in ["loyalty", "лояльность".decode("utf-8")]:
					answer = alt_change_cfg(source[1], "loyalty", val, (1, 6))
				elif key in ["devoice", "девойс".decode("utf-8")]:
					answer = alt_change_cfg(source[1], "dtime", val, (60, 361))
				elif key in ["msglen", "мсглен".decode("utf-8")]:
					answer = alt_change_cfg(source[1], "len", val, (512, 2049))
				elif key in ["prslen", "прзлен".decode("utf-8")]:
					answer = alt_change_cfg(source[1], "prlen", val, (128, 513))
				else:
					answer = AnsBase[2]
				if answer not in [AnsBase[2], AnsBase[30]]:
					cat_file(chat_file(source[1], LawsFile), str(ChatsAttrs[source[1]]["laws"]))
			else:
				answer = AnsBase[2]
		else:
			answer = sheriff_answers[24]
			if ChatsAttrs[source[1]]["laws"]["space"]:
				answer += sheriff_answers[25][:-1]
			else:
				answer += sheriff_answers[26][:-1]
			answer += sheriff_answers[27] % (ChatsAttrs[source[1]]["laws"]["lnick"])
			if ChatsAttrs[source[1]]["laws"]["avipe"]:
				answer += sheriff_answers[25]
			else:
				answer += sheriff_answers[26]
			answer += sheriff_answers[28] % (ChatsAttrs[source[1]]["laws"]["aban"])
			if ChatsAttrs[source[1]]["laws"]["verif"]:
				answer += sheriff_answers[25]
			else:
				answer += sheriff_answers[26]
			answer += sheriff_answers[29] % (ChatsAttrs[source[1]]["laws"]["loyalty"])
			if ChatsAttrs[source[1]]["laws"]["tiser"]:
				answer += sheriff_answers[25]
			else:
				answer += sheriff_answers[26]
			answer += sheriff_answers[30] % (ChatsAttrs[source[1]]["laws"]["dtime"])
			if ChatsAttrs[source[1]]["laws"]["obscene"]:
				answer += sheriff_answers[25][:-1]
			else:
				answer += sheriff_answers[26][:-1]
			answer += sheriff_answers[31] % (ChatsAttrs[source[1]]["laws"]["len"])
			if ChatsAttrs[source[1]]["laws"]["lower"]:
				answer += sheriff_answers[25][:-1]
			else:
				answer += sheriff_answers[26][:-1]
			answer += sheriff_answers[32] % (ChatsAttrs[source[1]]["laws"]["prlen"])
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
	for x in sheriff_answers[33].split("/"):
		if body.count(x):
			return True
	return False

def lower_checker(conf, body):
	col, body = 0, replace_all(body, [" "] + Chats[conf].get_nicks(), "").strip()
	for x in tuple(body):
		if x.isupper():
			col += 1
	if col > 12 and col > (len(body) / 3):
		return True
	return False

def check_nick(conf, nick):

	def nick_checker(conf, nick):
		nick = nick.lower()
		for x in ["%s", "%d", "%f"]:
			if nick.count(x):
				return True
		nick = nick.split()[0]
		if nick in Cmds.keys():
			return True
		if Chats[conf].cPref and nick.startswith(Chats[conf].cPref):
			if nick[1:] in Cmds.keys():
				return True
		return False

	if nick:
		if len(nick) > ChatsAttrs[conf]["laws"]["lnick"]:
			spesial_kick(conf, nick, sheriff_answers[0] % (ChatsAttrs[conf]["laws"]["lnick"]))
		if nick_checker(conf, nick):
			spesial_kick(conf, nick, sheriff_answers[1])
		if ChatsAttrs[conf]["laws"]["space"]:
			if len(nick) != len(nick.strip()):
				spesial_kick(conf, nick, sheriff_answers[2])
		if ChatsAttrs[conf]["laws"]["obscene"]:
			if obscene_checker(nick):
				spesial_kick(conf, nick, sheriff_answers[3])

def sheriff_set(ltype, source, source_, access, loyalty, body, disp):
	if access <= loyalty:
		if Federal_Jail[source[1]].has_key(source_):
			Federal_Jail[source[1]][source_].offenses += 1
			if Federal_Jail[source[1]][source_].offenses in [1, 2]:
				Answer(body, ltype, source, disp)
				raise iThr.ThrKill("exit")
			elif Federal_Jail[source[1]][source_].offenses == 3:
				Chats[source[1]].visitor(source[2], "%s: %s" % (get_self_nick(source[1]), body))
				Federal_Jail[source[1]][source_].SetDevoice()
				Msend(source[0], sheriff_answers[16] % (body, ChatsAttrs[source[1]]["laws"]["dtime"]), disp)
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
	if isConf and source[2] and Chats[source[1]].ismoder:
		access = get_access(source[1], source[2])
		loyalty = sheriffs_loyalty(source[1])
		if access <= loyalty[0]:
			source_ = get_source(source[1], source[2])
			if ChatsAttrs[source[1]]["laws"]["tiser"]:
				if tiser_checker(body):
					if access <= loyalty[1]:
						if Federal_Jail[source[1]].has_key(source_):
							Federal_Jail[source[1]][source_].SetDevoice()
						spesial_kick(source[1], source[2], sheriff_answers[4])
					else:
						Answer(sheriff_answers[4], ltype, source, disp)
					raise iThr.ThrKill("exit")
			if Federal_Jail[source[1]].has_key(source_):
				if ChatsAttrs[source[1]]["laws"]["verif"]:
					if access < 2 and Federal_Jail[source[1]][source_].vakey and ltype == Types[0]:
						if Federal_Jail[source[1]][source_].vakey == body.lower():
							Federal_Jail[source[1]][source_].Autenticated()
							Chats[source[1]].participant(source[2], sheriff_answers[20] % get_self_nick(source[1]))
							Msend(source[0], sheriff_answers[21], disp)
						elif Federal_Jail[source[1]][source_].vnumb.plus() >= 3:
							Federal_Jail[source[1]][source_].vnumb = itypes.Number()
							spesial_kick(source[1], source[2], sheriff_answers[22])
						else:
							Msend(source[0], sheriff_answers[23], disp)
						raise iThr.ThrKill("exit")
				Federal_Jail[source[1]][source_].addMsTime()
				list = Federal_Jail[source[1]][source_].msdates
				len_msg = len(list)
				if len_msg >= 4:
					if (list[len_msg - 1] - list[0]) <= 6:
						Federal_Jail[source[1]][source_].msdates = [list[len_msg - 1]]
						Federal_Jail[source[1]][source_].SetDevoice()
						spesial_kick(source[1], source[2], sheriff_answers[15])
					else:
						Federal_Jail[source[1]][source_].msdates.pop(0)
				del list, len_msg
			if ltype == Types[1]:
				if ChatsAttrs[source[1]]["laws"]["obscene"]:
					if obscene_checker(body):
						sheriff_set(ltype, source, source_, access, loyalty[1], sheriff_answers[5], disp)
				if ChatsAttrs[source[1]]["laws"]["len"]:
					if len(body) > ChatsAttrs[source[1]]["laws"]["len"]:
						sheriff_set(ltype, source, source_, access, loyalty[1], sheriff_answers[6], disp)
				if ChatsAttrs[source[1]]["laws"]["lower"]:
					if lower_checker(source[1], body):
						sheriff_set(ltype, source, source_, access, loyalty[1], sheriff_answers[7], disp)

def AvipeClear(conf, list):
	if Chats.has_key(conf):
		Antivipe[conf]["clear"] = []
		for sUser in Chats[conf].get_users():
			if sUser.source in list:
				if not Chats[conf].isHereNow(sUser.nick):
					if Chats[conf].isHere(sUser.nick):
						del Chats[conf].users[sUser.nick]
					if Federal_Jail[conf].has_key(sUser.source):
						del Federal_Jail[conf][sUser.source]
		for x in list:
			Chats[conf].none(x)

def antivipe_func(conf, nick, afl, source):

	def get_server(source, state = 0):
		if source.count("@"):
			source = source.split("@")[1]
			if state:
				source = source.split(".", 1)[1]
		return source

	if ChatsAttrs[conf]["laws"]["avipe"] and Chats[conf].ismoder and afl == AflRoles[2]:
		NowTime = time.time()
		if (NowTime - Chats[conf].sdate) >= 60:
			difference = (NowTime - Antivipe[conf]["ltime"])
			if difference > 360 and Antivipe[conf]["clear"]:
				sThread(AvipeClear.func_name, AvipeClear, (conf, Antivipe[conf]["clear"],))
			if difference > 15:
				Antivipe[conf]["ltime"] = NowTime
				Antivipe[conf]["jids"] = [source]
			else:
				Antivipe[conf]["jids"].append(source)
				joined = Antivipe[conf]["jids"]
				col = len(joined)
				if col >= 3:
					Antivipe[conf]["ltime"] = NowTime
					BsNick = get_self_nick(conf)
					Server = get_server(source)
					if Server == get_server(joined[col - 2]) and Server == get_server(joined[col - 3]):
						if Server not in (GoodServers + [get_server(conf, True)]):
							Chats[conf].ban(Server, sheriff_answers[12] % (BsNick))
							for sUser in Chats[conf].get_users():
								if sUser.source and sUser.ishere:
									if sUser.nick != BsNick and sUser.afl == AflRoles[2]:
										if Server == get_server(sUser.source):
											if Federal_Jail[conf].has_key(sUser.source):
												if not Federal_Jail[conf][sUser.source].verif:
													Chats[conf].kick(sUser.nick, sheriff_answers[12] % (BsNick))
						else:
							for sUser in Chats[conf].get_users():
								if sUser.source and sUser.ishere:
									if sUser.nick != BsNick and sUser.afl == AflRoles[2]:
										if Server == get_server(sUser.source):
											if Federal_Jail[conf].has_key(sUser.source):
												if not Federal_Jail[conf][sUser.source].verif:
													Antivipe[conf]["clear"].append(sUser.source)
													Chats[conf].ban(sUser.source, sheriff_answers[12] % (BsNick))
					else:
						Antivipe[conf]["clear"].append(source)
						Chats[conf].ban(source, sheriff_answers[12] % (BsNick))
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
						Federal_Jail[conf][sUser.source] = rUser(sUser.dates[0])
					else:
						Federal_Jail[conf][sUser.source].addPrTime()
					isHere = Federal_Jail[conf][sUser.source].ishere
					if not isHere:
						Federal_Jail[conf][sUser.source].ishere = True
						if Federal_Jail[conf][sUser.source].devoice:
							etime = Federal_Jail[conf][sUser.source].GetDevoice()
							if etime < ChatsAttrs[conf]["laws"]["dtime"]:
								Chats[conf].visitor(nick, sheriff_answers[11] % get_self_nick(conf))
								Msend("%s/%s" % (conf, nick), sheriff_answers[14] % timeElapsed(ChatsAttrs[conf]["laws"]["dtime"] - etime), disp)
							else:
								Federal_Jail[conf][sUser.source].devoice = 0
					if sUser.access >= 2 and not Federal_Jail[conf][sUser.source].verif:
						Federal_Jail[conf][sUser.source].Autenticated()
					if not relapser or not isHere:
						antivipe_func(conf, nick, sUser.afl, sUser.source)
						check_nick(conf, nick)
						if ChatsAttrs[conf]["laws"]["verif"] and not Federal_Jail[conf][sUser.source].devoice and sUser.access <= 1 and AflRoles[2] == GetRole(stanza)[0]:
							if not Federal_Jail[conf][sUser.source].verif:
								Chats[conf].visitor(nick, sheriff_answers[17] % get_self_nick(conf))
								ques = choice(sheriff_answers[19].splitlines()).split("|")
								Federal_Jail[conf][sUser.source].vakey = (ques[1].strip()).lower()
								Msend("%s/%s" % (conf, nick), sheriff_answers[18] % (ques[0].strip()), disp)
								del ques
					del isHere
					list = Federal_Jail[conf][sUser.source].prdates
					len_prs = len(list)
					if len_prs >= 4:
						if (list[len_prs - 1] - list[0]) <= 10:
							Federal_Jail[conf][sUser.source].prdates = [list[len_prs - 1]]
							spesial_kick(conf, nick, sheriff_answers[13])
						else:
							Federal_Jail[conf][sUser.source].prdates.pop(0)
					del list, len_prs
					status = stanza.getStatus()
					if status:
						if ChatsAttrs[conf]["laws"]["tiser"]:
							if tiser_checker(status):
								spesial_kick(conf, nick, sheriff_answers[4])
						if ChatsAttrs[conf]["laws"]["obscene"]:
							if obscene_checker(status):
								spesial_kick(conf, nick, sheriff_answers[8])
						if ChatsAttrs[conf]["laws"]["prlen"]:
							if len(status) > ChatsAttrs[conf]["laws"]["prlen"]:
								spesial_kick(conf, nick, sheriff_answers[9])
				elif stype == Types[4]:
					if relapser:
						scode = stanza.getStatusCode()
						if scode in [sCodes[0], sCodes[3]]:
							del Federal_Jail[conf][sUser.source]
						elif scode == sCodes[2]:
							Federal_Jail[conf][sUser.source].leaved()
							Federal_Jail[conf][sUser.source].kicks += 1
							if ChatsAttrs[conf]["laws"]["aban"] and Chats[conf].ismoder:
								if ChatsAttrs[conf]["laws"]["aban"] <= Federal_Jail[conf][sUser.source].kicks:
									del Federal_Jail[conf][sUser.source]
									Chats[conf].ban(sUser.source, sheriff_answers[10] % (get_self_nick(conf), ChatsAttrs[conf]["laws"]["aban"]))
						else:
							Federal_Jail[conf][sUser.source].leaved()
			elif relapser:
				del Federal_Jail[conf][sUser.source]

def Security_01si(conf):
	Federal_Jail[conf] = {}
	Antivipe[conf] = {"ltime": 0, "jids": [], "clear": []}
	if not ChatsAttrs.has_key(conf):
		ChatsAttrs[conf] = {}
	ChatsAttrs[conf]["laws"] = {"avipe": True, "space": True, "verif": False, "tiser": True, "obscene": False, "lower": False, "dtime": 180, "loyalty": 1, "aban": 3, "prlen": 256, "lnick": 24, "len": 1024}
	Name = chat_file(conf, LawsFile)
	if initialize_file(Name, str(ChatsAttrs[conf]["laws"])):
		ChatsAttrs[conf]["laws"] = eval(get_file(Name))

def Security_04si(conf):
	del Federal_Jail[conf]
	del Antivipe[conf]

expansions[exp_name].funcs_add([command_order, spesial_kick, sheriffs_loyalty, tiser_checker, obscene_checker, lower_checker, check_nick, sheriff_set, AvipeClear, antivipe_func, Security_01eh, Security_02eh, Security_01si, Security_04si])
expansions[exp_name].ls.extend(["sheriff_answers", "GoodServers", "LawsFile", "Federal_Jail", "Antivipe", "rUser"])

command_handler(command_order, {"RU": "ордер", "EN": "order"}, 6, exp_name)

handler_register(Security_01si, "01si", exp_name)
handler_register(Security_04si, "04si", exp_name)
handler_register(Security_01eh, "01eh", exp_name)
handler_register(Security_02eh, "02eh", exp_name)
