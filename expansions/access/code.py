# coding: utf-8

#  BlackSmith mark.2
exp_name = "access" # /code.py v.x1
#  Id: 20~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

AccessFile = dynamic % ("access.db")
ChatAccessFile = "access.db"

def command_get_access(ltype, source, body, disp):

	def get_acc(access):
		if access >= 8:
			access = "%d (BOSS)" % (access)
		elif access == 7:
			access = "7 (Chief)"
		else:
			access = str(access)
		return access

	if not body:
		answer = AccAnsBase[0] % get_acc(get_access(source[1], source[2]))
	elif Chats.has_key(source[1]):
		if Chats[source[1]].isHere(body):
			answer = AccAnsBase[1] % (body, get_acc(get_access(source[1], body)))
		elif Galist.has_key(body):
			answer = AccAnsBase[1] % (body, get_acc(Galist.get(body, 0)))
		elif Chats[source[1]].alist.has_key(body):
			answer = AccAnsBase[1] % (body, str(Chats[source[1]].alist.get(body, 0)))
		else:
			answer = AccAnsBase[2] % (body)
	elif Galist.has_key(body):
		answer = AccAnsBase[1] % (body, get_acc(Galist.get(body, 0)))
	else:
		answer = AccAnsBase[2] % (body)
	Answer(answer, ltype, source, disp)

def command_get_galist(ltype, source, body, disp):
	if Galist:
		list = []
		for x, y in Galist.items():
			list.append([y, x])
		list.sort()
		list.reverse()
		if ltype == Types[1]:
			Answer(AnsBase[11], ltype, source, disp)
		answer, Numb = AccAnsBase[5], itypes.Number()
		for x in list:
			answer += "%d) %s - %d\n" % (Numb.plus(), x[1], x[0])
		Msend(source[0], answer, disp)
	else:
		Answer(AccAnsBase[3], ltype, source, disp)

def command_get_lalist(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if Chats[source[1]].alist:
			list = []
			for x, y in Chats[source[1]].alist.items():
				list.append([y, x])
			list.sort()
			list.reverse()
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			answer, Numb = AccAnsBase[5], itypes.Number()
			for x in list:
				answer += "%d) %s - %d\n" % (Numb.plus(), x[1], x[0])
			Msend(source[0], answer, disp)
		else:
			answer = AccAnsBase[4]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_set_access(ltype, source, body, disp):

	def set_access(instance, access = None):
		if access != None:
			Galist[instance] = access
		else:
			del Galist[instance]
		cat_file(AccessFile, str(Galist))
		for conf in Chats.keys():
			for sUser in Chats[conf].get_users():
				if sUser.source and sUser.source == instance:
					if access == None:
						access = Chats[conf].alist.get(instance, None)
					if access != None:
						sUser.access = access
					else:
						sUser.calc_acc()

	if body:
		body = body.split(None, 1)
		if len(body) == 2:
			Nick = body.pop(1)
			if Chats.has_key(source[1]):
				if Chats[source[1]].isHere(Nick):
					instance = get_source(source[1], Nick)
			if not locals().has_key("instance"):
				instance = (Nick.split())[0].lower()
				if not isSource(instance):
					instance = None
			if instance:
				access = body.pop(0)
				if access == "!":
					if Galist.has_key(instance):
						set_access(instance)
						answer = AnsBase[4]
					else:
						answer = AccAnsBase[6] % (Nick)
				elif isNumber(access):
					access = int(access)
					if access in range(-1, 9):
						set_access(instance, access)
						answer = AnsBase[4]
					else:
						answer = AccAnsBase[7]
				else:
					answer = AnsBase[30]
			else:
				answer = AccAnsBase[10] % (Nick)
		else:
			answer = AnsBase[2]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_set_local_access(ltype, source, body, disp):

	def set_access(conf, instance, access = None):
		if access != None:
			Chats[conf].alist[instance] = access
		else:
			del Chats[conf].alist[instance]
		cat_file(chat_file(conf, ChatAccessFile), str(Chats[conf].alist))
		for sUser in Chats[conf].get_users():
			if sUser.source and sUser.source == instance:
				if access == None:
					access = Galist.get(instance, None)
				if access != None:
					sUser.access = access
				else:
					sUser.calc_acc()

	if Chats.has_key(source[1]):
		if body:
			body = body.split(None, 1)
			if len(body) == 2:
				Nick = body.pop(1)
				if Chats[source[1]].isHere(Nick):
					instance = get_source(source[1], Nick)
				else:
					instance = (Nick.split())[0].lower()
					if not isSource(instance):
						instance = None
				if instance:
					access = body.pop(0)
					if access == "!":
						if Chats[source[1]].alist.has_key(instance):
							set_access(source[1], instance)
							answer = AnsBase[4]
						else:
							answer = AccAnsBase[6] % (Nick)
					elif not Galist.has_key(instance):
						if isNumber(access):
							access = int(access)
							if access in range(7):
								set_access(source[1], instance, access)
								answer = AnsBase[4]
							else:
								answer = AccAnsBase[8]
						else:
							answer = AnsBase[30]
					else:
						answer = AccAnsBase[9] % (Nick)
				else:
					answer = AccAnsBase[10] % (Nick)
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

def load_acclist():
	if initialize_file(AccessFile):
		Galist.update(eval(get_file(AccessFile)))

def load_local_acclist(conf):
	filename = chat_file(conf, ChatAccessFile)
	if initialize_file(filename):
		Chats[conf].alist.update(eval(get_file(filename)))

expansions[exp_name].funcs_add([command_get_access, command_get_galist, command_get_lalist, command_set_access, command_set_local_access, load_acclist, load_local_acclist])
expansions[exp_name].ls.extend(["AccessFile", "ChatAccessFile", "AccAnsBase"])

command_handler(command_get_access, {"RU": "доступ", "EN": "access"}, 1, exp_name)
command_handler(command_get_galist, {"RU": "доступы", "EN": "acclist"}, 7, exp_name)
command_handler(command_get_lalist, {"RU": "доступы*", "EN": "acclist2"}, 4, exp_name)
command_handler(command_set_access, {"RU": "глобдоступ", "EN": "globaccess"}, 8, exp_name)
command_handler(command_set_local_access, {"RU": "локдоступ", "EN": "locaccess"}, 6, exp_name)

handler_register(load_acclist, "00si", exp_name)
handler_register(load_local_acclist, "01si", exp_name)
