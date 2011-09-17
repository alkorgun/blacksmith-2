# coding: utf-8

#  BlackSmith mark.2
exp_name = "basic_control" # /code.py v.x8
#  Id: 06~2a
#  Code © (2009-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def Chat_check(conf):
	Numb = itypes.Number()
	while Chats.has_key(conf):
		if Chats[conf].IamHere != None:
			break
		time.sleep(.4)
		if Numb.plus() >= 50:
			break

def command_join(ltype, source, body, disp):
	if body:
		list = body.split()
		conf = (list.pop(0)).lower()
		if conf.count("@conference.") and conf.count(".") >= 2:
			if not Chats.has_key(conf):
				confname = dynamic % (conf)
				if not check_nosimbols(confname):
					confname = encode_filename(confname)
				if not os.path.exists(confname):
					try:
						os.makedirs(confname, 0755)
					except:
						confname = None
				if confname:
					codename, disp_, cPref, nick = None, None, None, DefNick
					while len(list):
						x = list.pop()
						if x.startswith("1="):
							x = x.split("1=", 1)
							if len(x) == 2 and x[1]:
								x = x[1].lower()
								if Clients.has_key(x):
									disp_ = x
						elif x.startswith("2="):
							x = x.split("2=", 1)
							if len(x) == 2 and x[1]:
								if len(x[1]) <= 16:
									nick = x[1]
						elif x.startswith("3="):
							x = x.split("3=", 1)
							if len(x) == 2 and x[1]:
								if x[1] in cPrefs:
									cPref = x[1]
						elif x.startswith("4="):
							x = x.split("4=", 1)
							if len(x) == 2 and x[1]:
								codename = x[1]
					source_ = get_source(source[1], source[2])
					if SuperAdmin != source_:
						delivery(ControlAnsBase[0] % (source[2], source_, conf))
					if not disp_:
						disp_ = IdleClient()
					Chats[conf] = sConf(conf, disp_, codename, cPref, nick)
					Chats[conf].load_all()
					Chats[conf].join()
					Chat_check(conf)
					if Chats.has_key(conf) and Chats[conf].IamHere:
						Msend(conf, ControlAnsBase[7] % (ProdName, source[2]), disp_)
						answer = ControlAnsBase[2] % (conf)
					else:
						answer = ControlAnsBase[3] % (conf)
						time.sleep(3.6)
						if ejoinTimerName(conf) in iThr.ThrNames():
							answer += ControlAnsBase[13]
				else:
					answer = ControlAnsBase[15]
			else:
				answer = ControlAnsBase[5]
		else:
			answer = ControlAnsBase[6] % (conf)
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_rejoin(ltype, source, body, disp):
	if body:
		conf = body.split()[0].lower()
	else:
		conf = source[1]
	if Chats.has_key(conf):
		if online(Chats[conf].disp):
			Chats[conf].leave(ControlAnsBase[8] % (source[2]))
			time.sleep(2)
			Chats[conf].join()
			Chat_check(conf)
			if Chats.has_key(conf) and Chats[conf].IamHere:
				answer = AnsBase[4]
			else:
				answer = AnsBase[7]
		else:
			answer = ControlAnsBase[14]
	else:
		answer = AnsBase[8]
	Answer(answer, ltype, source, disp)

def command_leave(ltype, source, body, disp):
	if body:
		conf = body.split()[0].lower()
	else:
		conf = source[1]
	if not body or enough_access(source[1], source[2], 7) or conf == source[1]:
		if Chats.has_key(conf):
			source_ = get_source(source[1], source[2])
			if SuperAdmin != source_:
				delivery(ControlAnsBase[4] % (source[2], source_, conf))
			info = ControlAnsBase[9] % (source[2])
			Msend(conf, info, Chats[conf].disp)
			time.sleep(2)
			Chats[conf].full_leave(info)
			if conf != source[1]:
				answer = ControlAnsBase[10] % (conf)
		else:
			answer = AnsBase[8]
	else:
		answer = AnsBase[10]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_reconnect(ltype, source, body, disp):
	if body:
		Name = body.split()[0].lower()
	else:
		Name = get_disp(disp)
	if InstansesDesc.has_key(Name):
		ThrName = "%s%s" % (Types[13], Name)
		if Clients.has_key(Name):
			ThrIds = iThr.ThrNames()
			if ThrName in ThrIds:
				for Thr in iThr.enumerate():
					if Thr._Thread__name == ThrName:
						Thr.kill()
			if online(Name):
				try:
					Clients[Name].disconnect()
				except:
					pass
		if connect_client(Name, InstansesDesc[Name])[0]:
			try:
				Try_Thr(composeThr(Dispatch_handler, ThrName, (Name,)), -1)
			except RuntimeError:
				answer = ControlAnsBase[16]
			else:
				for conf in Chats.keys():
					if Name == Chats[conf].disp:
						Chats[conf].join()
				answer = AnsBase[4]
		else:
			answer = AnsBase[7]
	else:
		answer = ControlAnsBase[17]
	Answer(answer, ltype, source, disp)

def command_reload(ltype, source, body, disp):
	exit_desclr = ControlAnsBase[11] % (source[2])
	if body:
		exit_desclr += ControlAnsBase[1] % (body)
	for conf in Chats.keys():
		Msend(conf, exit_desclr, Chats[conf].disp)
	time.sleep(6)
	VarCache["alive"] = False
	iThr.Threads_kill()
	for disp in Clients.keys():
		if online(disp):
			sUnavailable(disp, exit_desclr)
	call_sfunctions("03si")
	Exit("\n\nRestart command...", 0, 15)

def command_exit(ltype, source, body, disp):
	exit_desclr = ControlAnsBase[12] % (source[2])
	if body:
		exit_desclr += ControlAnsBase[1] % (body)
	for conf in Chats.keys():
		Msend(conf, exit_desclr, Chats[conf].disp)
	time.sleep(6)
	VarCache["alive"] = False
	iThr.Threads_kill()
	for disp in Clients.keys():
		if online(disp):
			sUnavailable(disp, exit_desclr)
	call_sfunctions("03si")
	Exit("\n\nSysExit command...", 1, 15)

expansions[exp_name].funcs_add([Chat_check, command_join, command_rejoin, command_leave, command_reconnect, command_reload, command_exit])
expansions[exp_name].ls.extend(["ControlAnsBase"])

command_handler(command_join, {"RU": "джойн", "EN": "join"}, 7, exp_name)
command_handler(command_rejoin, {"RU": "реджойн", "EN": "rejoin"}, 7, exp_name)
command_handler(command_leave, {"RU": "выйди", "EN": "leave"}, 6, exp_name)
command_handler(command_reconnect, {"RU": "реконнект", "EN": "reconnect"}, 8, exp_name)
command_handler(command_reload, {"RU": "рестарт", "EN": "reload"}, 8, exp_name)
command_handler(command_exit, {"RU": "выкл", "EN": "exit"}, 8, exp_name)
