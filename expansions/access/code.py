# coding: utf-8

#  BlackSmith mark.2
exp_name = "access" # /code.py v.x2
#  Id: 20~2b
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	AccessFile = dynamic % ("access.db")
	ChatAccessFile = "access.db"

	def command_get_access(self, ltype, source, body, disp):

		def get_acc(access):
			if access >= 8:
				access = "%d (BOSS)" % (access)
			elif access == 7:
				access = "7 (Chief)"
			else:
				access = str(access)
			return access

		if not body:
			answer = self.AnsBase[0] % get_acc(get_access(source[1], source[2]))
		elif Chats.has_key(source[1]):
			if Chats[source[1]].isHere(body):
				answer = self.AnsBase[1] % (body, get_acc(get_access(source[1], body)))
			elif Galist.has_key(body):
				answer = self.AnsBase[1] % (body, get_acc(Galist.get(body, 0)))
			elif Chats[source[1]].alist.has_key(body):
				answer = self.AnsBase[1] % (body, str(Chats[source[1]].alist.get(body, 0)))
			else:
				answer = self.AnsBase[2] % (body)
		elif Galist.has_key(body):
			answer = self.AnsBase[1] % (body, get_acc(Galist.get(body, 0)))
		else:
			answer = self.AnsBase[2] % (body)
		Answer(answer, ltype, source, disp)

	def command_get_galist(self, ltype, source, body, disp):
		if Galist:
			list = []
			for x, y in Galist.items():
				list.append([y, x])
			list.sort()
			list.reverse()
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			answer, Numb = self.AnsBase[5], itypes.Number()
			for x in list:
				answer += "%d) %s - %d\n" % (Numb.plus(), x[1], x[0])
			Msend(source[0], answer, disp)
		else:
			Answer(self.AnsBase[3], ltype, source, disp)

	def command_get_lalist(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if Chats[source[1]].alist:
				list = []
				for x, y in Chats[source[1]].alist.items():
					list.append([y, x])
				list.sort()
				list.reverse()
				if ltype == Types[1]:
					Answer(AnsBase[11], ltype, source, disp)
				answer, Numb = self.AnsBase[5], itypes.Number()
				for x in list:
					answer += "%d) %s - %d\n" % (Numb.plus(), x[1], x[0])
				Msend(source[0], answer, disp)
			else:
				answer = self.AnsBase[4]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_set_access(self, ltype, source, body, disp):

		def set_access(instance, access = None):
			if access != None:
				Galist[instance] = access
			else:
				del Galist[instance]
			cat_file(self.AccessFile, str(Galist))
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
							answer = self.AnsBase[6] % (Nick)
					elif isNumber(access):
						access = int(access)
						if access in xrange(-1, 9):
							set_access(instance, access)
							answer = AnsBase[4]
						else:
							answer = self.AnsBase[7]
					else:
						answer = AnsBase[30]
				else:
					answer = self.AnsBase[10] % (Nick)
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_set_local_access(self, ltype, source, body, disp):

		def set_access(conf, instance, access = None):
			if access != None:
				Chats[conf].alist[instance] = access
			else:
				del Chats[conf].alist[instance]
			cat_file(chat_file(conf, self.ChatAccessFile), str(Chats[conf].alist))
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
								answer = self.AnsBase[6] % (Nick)
						elif not Galist.has_key(instance):
							if isNumber(access):
								access = int(access)
								if access in xrange(7):
									set_access(source[1], instance, access)
									answer = AnsBase[4]
								else:
									answer = self.AnsBase[8]
							else:
								answer = AnsBase[30]
						else:
							answer = self.AnsBase[9] % (Nick)
					else:
						answer = self.AnsBase[10] % (Nick)
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	def load_acclist(self):
		if initialize_file(self.AccessFile):
			Galist.update(eval(get_file(self.AccessFile)))

	def load_local_acclist(self, conf):
		filename = chat_file(conf, self.ChatAccessFile)
		if initialize_file(filename):
			Chats[conf].alist.update(eval(get_file(filename)))

	commands = (
		(command_get_access, "access", 1,),
		(command_get_galist, "acclist", 7,),
		(command_get_lalist, "acclist2", 4,),
		(command_set_access, "gaccess", 8,),
		(command_set_local_access, "laccess", 6,)
					)

	handlers = (
		(load_acclist, "00si"),
		(load_local_acclist, "01si")
					)
