# coding: utf-8

#  BlackSmith mark.2
exp_name = "sconf_attrs" # /code.py v.x4
#  Id: 07~3b
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_redisp(self, ltype, source, body, disp):
		body = body.split()
		if len(body) >= 1:
			disp_ = (body.pop(0)).lower()
			if Clients.has_key(disp_):
				if body:
					conf = (body.pop(0)).lower()
				else:
					conf = source[1]
				if Chats.has_key(conf):
					if Chats[conf].disp != disp_:
						if online(disp_):
							Chats[conf].leave(self.AnsBase[3])
							Chats[conf].disp = disp_
							Chats[conf].save()
							sleep(0.6)
							Chats[conf].join()
							if conf == source[1]:
								disp = disp_
							answer = AnsBase[4]
						else:
							answer = self.AnsBase[0] % (disp_)
					else:
						answer = self.AnsBase[1] % (disp_)
				else:
					answer = AnsBase[8]
			else:
				answer = self.AnsBase[2] % (disp_)
		else:
			answer = AnsBase[2]
		Answer(answer, ltype, source, disp)

	def command_botnick(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				Nick = sub_desc(body, [(chr(32), chr(95)), chr(10), chr(13), chr(9)]).strip()
				if len(Nick) <= 16:
					Chats[source[1]].nick = xmpp.XMLescape(Nick)
					Chats[source[1]].save()
					Chats[source[1]].join()
					answer = self.AnsBase[4] % (Nick)
				else:
					answer = self.AnsBase[5]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	def command_prefix(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if enough_access(source[1], source[2], 6):
					body = body.lower()
					if body in ("del", "убрать".decode("utf-8")):
						if Chats[source[1]].cPref:
							Chats[source[1]].cPref = None
							Chats[source[1]].save()
							answer = self.AnsBase[6]
						else:
							answer = self.AnsBase[7]
					elif body in cPrefs:
						if Chats[source[1]].cPref != body:
							Chats[source[1]].cPref = body
							Chats[source[1]].save()
							answer = self.AnsBase[8] % (body)
						else:
							answer = self.AnsBase[9] % (body)
					else:
						answer = self.AnsBase[10] % ("', '".join(cPrefs))
				else:
					answer = AnsBase[10]
			elif Chats[source[1]].cPref:
				answer = self.AnsBase[11] % (Chats[source[1]].cPref)
			else:
				answer = self.AnsBase[12]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	StatusDesc = {"чат".decode("utf-8"): 0, "ушел".decode("utf-8"): 1, "нет".decode("utf-8"): 2, "занят".decode("utf-8"): 3}

	ChatStatus = "status.db"

	def command_status(self, ltype, source, body, disp):
		if body:
			body = body.split(None, 2)
			if len(body) == 3:
				state = (body.pop(1)).lower()
				if self.StatusDesc.has_key(state):
					state = sList[self.StatusDesc[state]]
				if state in sList:
					chat, status = body
					body = "%s|%s" % (state, status)
					chat = chat.lower()
					if chat in ("everywhere", "везде".decode("utf-8")):
						for conf in Chats.keys():
							Chats[conf].change_status(state, status)
							cat_file(chat_file(conf, self.ChatStatus), body)
						answer = AnsBase[4]
					elif chat in ("here", "здесь".decode("utf-8")):
						if Chats.has_key(source[1]):
							Chats[source[1]].change_status(state, status)
							cat_file(chat_file(source[1], self.ChatStatus), body)
							answer = AnsBase[4]
						else:
							answer = AnsBase[0]
					elif Chats.has_key(chat):
						Chats[chat].change_status(state, status)
						cat_file(chat_file(chat, self.ChatStatus), body)
						answer = AnsBase[4]
					else:
						answer = AnsBase[8]
				else:
					answer = self.AnsBase[13] % (state)
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_password(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				if body in ("none", "нет".decode("utf-8")):
					body = None
				Chats[source[1]].code = body
				Chats[source[1]].save()
				answer = AnsBase[4]
			else:
				answer = str(Chats[source[1]].code)
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	def load_status(self, conf):
		filename = chat_file(conf, self.ChatStatus)
		if initialize_file(filename, "%s|%s" % (sList[0], DefStatus)):
			Chats[conf].set_status(*get_file(filename).split("|", 1))

	commands = (
		(command_redisp, "botjid", 7,),
		(command_botnick, "botnick", 6,),
		(command_status, "botstatus", 7,),
		(command_password, "password", 6,),
		(command_prefix, "prefix", 1, False)
					)

	handlers = ((load_status, "01si"),)
