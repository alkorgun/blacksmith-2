# coding: utf-8

#  BlackSmith mark.2
# exp_name = "access" # /code.py v.x3
#  Id: 20~3c
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	AccessFile = dynamic % ("access.db")
	ChatAccessFile = "access.db"

	accessDesc = (
		"Visitor", # 0
		"Participant", # 1
		"Member", # 2
		"Moder", # 3
		"Member/Moder", # 4
		"Admin", # 5
		"Owner", # 6
		"Chief", # 7
		"God" # 8
					)

	def get_acc(self, access):
		if access > 8:
			access = "%d (Gandalf)" % (access)
		elif access < 0:
			access = "%d (f7u12)" % (access)
		else:
			access = "%d (%s)" % (access, self.accessDesc[access])
		return access

	def command_get_access(self, stype, source, body, disp):
		if not body:
			answer = self.AnsBase[0] % self.get_acc(get_access(source[1], source[2]))
		elif Chats.has_key(source[1]):
			if Chats[source[1]].isHere(body):
				answer = self.AnsBase[1] % (body, self.get_acc(get_access(source[1], body)))
			elif Galist.has_key(body):
				answer = self.AnsBase[1] % (body, self.get_acc(Galist.get(body, 0)))
			elif Chats[source[1]].alist.has_key(body):
				answer = self.AnsBase[1] % (body, str(Chats[source[1]].alist.get(body, 0)))
			else:
				answer = self.AnsBase[2] % (body)
		elif Galist.has_key(body):
			answer = self.AnsBase[1] % (body, self.get_acc(Galist.get(body, 0)))
		else:
			answer = self.AnsBase[2] % (body)
		Answer(answer, stype, source, disp)

	def command_get_galist(self, stype, source, body, disp):
		if Galist:
			ls = sorted([(acc, user) for user, acc in Galist.iteritems()], reverse = True)
			if stype == Types[1]:
				answer = AnsBase[11]
			Message(source[0], self.AnsBase[5] + enumerated_list("%s - %d" % (user, acc) for acc, user in ls), disp)
		else:
			answer = self.AnsBase[3]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_get_lalist(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if Chats[source[1]].alist:
				ls = sorted([(acc, user) for user, acc in Chats[source[1]].alist.iteritems()], reverse = True)
				if stype == Types[1]:
					answer = AnsBase[11]
				Message(source[0], self.AnsBase[5] + enumerated_list("%s - %d" % (user, acc) for acc, user in ls), disp)
			else:
				answer = self.AnsBase[4]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def command_set_access(self, stype, source, body, disp):

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
					if access == chr(33):
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
		Answer(answer, stype, source, disp)

	def command_set_local_access(self, stype, source, body, disp):

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
						if access == chr(33):
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
		Answer(answer, stype, source, disp)

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
