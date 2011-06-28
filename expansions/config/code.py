# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "config" # /code.py v.x2
#  Id: 19~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def get_config(config, cfg = ""):
	for s in config.sections():
		cfg += "[%s]\n" % (s.upper())
		for (o, v) in config.items(s):
			cfg += "%s = %s\n" % (o.upper(), str(v))
	return cfg.strip()

def command_config(ltype, source, body, disp):
	if body:
		ConfigDesc = {}
		for x in body.split():
			if not x.count("="):
				continue
			option, value = x.split("=", 1)
			if not value:
				continue
			option = option.lower()
			for section in GenCon.sections():
				if option in GenCon.options(section):
					if option in ["chat", "incoming", "memory", "private", "port"]:
						if check_number(value):
							value = str(int(value))
						else:
							continue
					elif option in ["tls", "getexc", "mserve"]:
						if value not in [str(True), str(False)]:
							continue
					elif option in ["status", "resource"]:
						value = replace_all(value, {"_": " "})
					if not ConfigDesc.has_key(section):
						ConfigDesc[section] = dict()
					ConfigDesc[section][option] = value
		if ConfigDesc:
			for section in ConfigDesc.keys():
				for (option, value) in ConfigDesc[section].items():
					GenCon.set(section, option, value)
			cat_file(GenConFile, get_config(GenCon))
			changes = []
			for options in ConfigDesc.values():
				changes.extend(options.keys())
			changes = [option.upper() for option in changes]
			answer = config_answers[0] % (", ".join(changes))
		else:
			answer = config_answers[1]
	else:
		if ltype == Types[1]:
			Answer(AnsBase[11], ltype, source, disp)
		Msend(source[0], get_config(GenCon, config_answers[2]), disp)
	if locals().has_key(Types[23]):
		Answer(answer, ltype, source, disp)

def command_cls_config(ltype, source, body, disp):
	if body:
		list = body.split()
		if len(list) >= 2:
			body = (list.pop(0)).lower()
			if body in ["del", "удалить".decode("utf-8")]:
				Name = (list.pop(0)).lower()
				if InstansesDesc.has_key(Name):
					clients = Clients.keys()
					if not Clients.has_key(Name) or len(clients) >= 2:
						if Name == Gen_disp:
							clients.remove(Gen_disp)
							Gen = choice(clients)
							delivery(config_answers[6] % Gen)
							globals()["Gen_disp"], Con = Gen, client_config(GenCon, "CLIENT")[1]
							for x in ConDisp.sections():
								z = client_config(ConDisp, x)
								if Gen == z[0]:
									Con = z[1]
									ConDisp.remove_section(x)
							GenCon.set("CLIENT", "serv", Con[0])
							GenCon.set("CLIENT", "port", Con[1])
							GenCon.set("CLIENT", "host", Con[2])
							GenCon.set("CLIENT", "user", Con[3])
							GenCon.set("CLIENT", "pass", Con[4])
							cat_file(GenConFile, get_config(GenCon))
							for x in ConDisp.sections():
								if Gen == client_config(ConDisp, x)[0]:
									ConDisp.remove_section(x)
						if Clients.has_key(Name):
							ThrIds = iThr.ThrNames()
							ThrName = "%s%s" % (Types[13], Name)
							if ThrName in ThrIds:
								for Thr in iThr.enumerate():
									if Thr._Thread__name == ThrName:
										Thr.kill()
						for conf in Chats.keys():
							if Chats[conf].disp == Name:
								if online(Name):
									Msend(conf, config_answers[4], Name)
									time.sleep(0.2)
								Chats[conf].leave(config_answers[5])
								Chats[conf].disp = IdleClient()
								Chats[conf].save()
								time.sleep(0.6)
								Chats[conf].join()
						if online(Name):
							try:
								Clients[Name].disconnect()
							except:
								pass
						if Flood.has_key(Name):
							del Flood[Name]
						del InstansesDesc[Name]
						for x in ConDisp.sections():
							if Name == client_config(ConDisp, x)[0]:
								ConDisp.remove_section(x)
						cat_file(ConDispFile, get_config(ConDisp))
						if Clients.has_key(Name):
							del Clients[Name]
						answer = AnsBase[4]
					else:
						answer = config_answers[7]
				else:
					answer = config_answers[11]
			elif body in ["add", "добавить".decode("utf-8")]:
				if len(list) >= 3:
					host = (list.pop(0)).lower()
					user = (list.pop(0)).lower()
					code = (list.pop(0))
					if list:
						port = (list.pop(0))
						if not check_number(port):
							port = "5222"
					else:
						port = "5222"
					jid = "%s@%s" % (user, host)
					serv = (host)
					if list:
						serv = (list.pop(0)).lower()
					if not Clients.has_key(jid):
						if not InstansesDesc.has_key(jid):
							if connect_client(jid, (serv, port, host, user, code))[0]:
								Numb = itypes.Number()
								Name = "CLIENT%d" % (len(ConDisp.sections()) + Numb.plus())
								while ConDisp.has_section(Name):
									Name = "CLIENT%d" % (len(ConDisp.sections()) + Numb.plus())
								ConDisp.add_section(Name)
								ConDisp.set(Name, "serv", serv)
								ConDisp.set(Name, "port", port)
								ConDisp.set(Name, "host", host)
								ConDisp.set(Name, "user", user)
								ConDisp.set(Name, "pass", code)
								Instance, desc = client_config(ConDisp, Name)
								InstansesDesc[Instance] = desc
								cat_file(ConDispFile, get_config(ConDisp))
								try:
									Try_Thr(composeThr(Dispatch_handler, "%s%s" % (Types[13], Instance), (Instance,)), -1)
								except RuntimeError:
									answer = config_answers[8]
								else:
									for conf in Chats.keys():
										if Instance == Chats[conf].disp:
											Chats[conf].join()
									answer = AnsBase[4]
							else:
								answer = config_answers[9]
						else:
							answer = config_answers[10]
					else:
						answer = config_answers[10]
				else:
					answer = AnsBase[2]
			elif body in ["password", "пароль".decode("utf-8")]:
				Name = (list.pop(0)).lower()
				if InstansesDesc.has_key(Name):
					if list:
						code = (list.pop(0))
						if list:
							if (list.pop(0)).lower() in ["set", "записать".decode("utf-8")]:
								changed = True
					else:
						from string import digits, letters
						code, symbols = "", "%s%s._(!}{#)" % (digits, letters)
						del digits, letters
						for x in range(24):
							code += choice(symbols)
					if not locals().has_key("changed"):
						if Clients.has_key(Name):
							try:
								changed = xmpp.features.changePasswordTo(Clients[Name], code)
							except:
								changed = False
						else:
							changed = False
					if changed:
						if Name == Gen_disp:
							GenCon.set("CLIENT", "pass", code)
							cat_file(GenConFile, get_config(GenCon))
						else:
							for x in ConDisp.sections():
								if Name == client_config(ConDisp, x)[0]:
									ConDisp.set(x, "pass", code)
									cat_file(ConDispFile, get_config(ConDisp))
									break
						serv = InstansesDesc[Name][0]
						port = InstansesDesc[Name][1]
						host = InstansesDesc[Name][2]
						user = InstansesDesc[Name][3]
						InstansesDesc[Name] = (serv, port, host, user, code)
						answer = AnsBase[4]
					else:
						answer = AnsBase[7]
				else:
					answer = config_answers[11]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[2]
	elif not len(ConDisp.sections()):
		answer = config_answers[3]
	else:
		if ltype == Types[1]:
			Answer(AnsBase[11], ltype, source, disp)
		Msend(source[0], get_config(ConDisp, config_answers[2]), disp)
	if locals().has_key(Types[23]):
		Answer(answer, ltype, source)

expansions[exp_name].funcs_add([get_config, command_config, command_cls_config])
expansions[exp_name].ls.extend(["config_answers"])

command_handler(command_config, {"RU": "конфиг", "EN": "config"}, 8, exp_name)
command_handler(command_cls_config, {"RU": "клиент", "EN": "client"}, 8, exp_name)
