# coding: utf-8

#  BlackSmith mark.2
exp_name = "sconf_attrs" # /code.py v.x3
#  Id: 07~2a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_redisp(ltype, source, body, disp):
	body = body.split()
	if len(body) >= 1:
		disp_ = body[0].lower()
		if Clients.has_key(disp_):
			if len(body) >= 2:
				conf = body[1].lower()
			else:
				conf = source[1]
			if Chats.has_key(conf):
				if Chats[conf].disp != disp_:
					if online(disp_):
						Chats[conf].leave(CstatAnsBase[3])
						Chats[conf].disp = disp_
						Chats[conf].save()
						time.sleep(0.6)
						Chats[conf].join()
						if conf == source[1]:
							disp = disp_
						answer = AnsBase[4]
					else:
						answer = CstatAnsBase[0] % (disp_)
				else:
					answer = CstatAnsBase[1] % (disp_)
			else:
				answer = AnsBase[8]
		else:
			answer = CstatAnsBase[2] % (disp_)
	else:
		answer = AnsBase[2]
	Answer(answer, ltype, source, disp)

def command_botnick(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			Nick = sub_desc(body, [(chr(32), chr(95)), chr(10), chr(13), chr(9)]).strip()
			if len(Nick) <= 16:
				Chats[source[1]].nick = xmpp.XMLescape(Nick)
				Chats[source[1]].save()
				Chats[source[1]].join()
				answer = CstatAnsBase[4] % (Nick)
			else:
				answer = CstatAnsBase[5]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def command_prefix(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			if enough_access(source[1], source[2], 6):
				body = body.lower()
				if body in ["del", "убрать".decode("utf-8")]:
					if Chats[source[1]].cPref:
						Chats[source[1]].cPref = None
						Chats[source[1]].save()
						answer = CstatAnsBase[6]
					else:
						answer = CstatAnsBase[7]
				elif body in cPrefs:
					if Chats[source[1]].cPref != body:
						Chats[source[1]].cPref = body
						Chats[source[1]].save()
						answer = CstatAnsBase[8] % (body)
					else:
						answer = CstatAnsBase[9] % (body)
				else:
					answer = CstatAnsBase[10] % (", ".join(cPrefs))
			else:
				answer = AnsBase[10]
		elif Chats[source[1]].cPref:
			answer = CstatAnsBase[11] % (Chats[source[1]].cPref)
		else:
			answer = CstatAnsBase[12]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

StatusDesc = {"чат".decode("utf-8"): 0, "ушел".decode("utf-8"): 1, "нет".decode("utf-8"): 2, "занят".decode("utf-8"): 3}

ChatStatus = "status.db"

def command_status(ltype, source, body, disp):
	if body:
		list = body.split(None, 2)
		if len(list) == 3:
			state = list[1].lower()
			if StatusDesc.has_key(state):
				state = sList[StatusDesc[state]]
			if state in sList:
				chat = list[0].lower()
				status = list[2].strip()
				body = "%s|%s" % (state, status)
				if chat in ["everywhere", "везде".decode("utf-8")]:
					for conf in Chats.keys():
						Chats[conf].change_status(state, status)
						cat_file(chat_file(conf, ChatStatus), body)
					answer = AnsBase[4]
				elif chat in ["here", "здесь".decode("utf-8")]:
					if Chats.has_key(source[1]):
						Chats[source[1]].change_status(state, status)
						cat_file(chat_file(source[1], ChatStatus), body)
						answer = AnsBase[4]
					else:
						answer = AnsBase[0]
				elif Chats.has_key(chat):
					Chats[chat].change_status(state, status)
					cat_file(chat_file(chat, ChatStatus), body)
					answer = AnsBase[4]
				else:
					answer = AnsBase[8]
			else:
				answer = CstatAnsBase[13] % (state)
		else:
			answer = AnsBase[2]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_password(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			if body in ["none", "нет".decode("utf-8")]:
				body = None
			Chats[source[1]].code = body
			Chats[source[1]].save()
			answer = AnsBase[4]
		else:
			answer = str(Chats[source[1]].code)
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def load_status(conf):
	filename = chat_file(conf, ChatStatus)
	if initialize_file(filename, "%s|%s" % (sList[0], DefStatus)):
		Chats[conf].set_status(*get_file(filename).split("|", 1))

expansions[exp_name].funcs_add([command_redisp, command_botnick, command_prefix, command_status, command_password, load_status])
expansions[exp_name].ls.extend(["CstatAnsBase, StatusDesc, ChatStatus"])

command_handler(command_redisp, {"RU": "ботжид", "EN": "botjid"}, 7, exp_name)
command_handler(command_botnick, {"RU": "ботник", "EN": "botnick"}, 6, exp_name)
command_handler(command_status, {"RU": "ботстатус", "EN": "botstatus"}, 7, exp_name)
command_handler(command_password, {"RU": "пароль", "EN": "password"}, 6, exp_name)
command_handler(command_prefix, {"RU": "префикс", "EN": "prefix"}, 1, exp_name, False)

handler_register(load_status, "01si", exp_name)
