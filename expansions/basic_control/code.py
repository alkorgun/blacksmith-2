# coding: utf-8

#  BlackSmith mark.2
# exp_name = "basic_control" # /code.py v.x14
#  Id: 06~8c
#  Code © (2009-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def Check(self, conf):
		Numb = itypes.Number()
		while Chats.has_key(conf):
			if Chats[conf].IamHere != None:
				break
			sleep(0.4)
			if Numb.plus() >= 50:
				break

	compile_chat = compile__("^[^\s'\"@<>&]+?@(?:conference|muc|conf|chat|group)\.[\w-]+?\.[\.\w-]+?$")

	def command_join(self, stype, source, body, disp):
		if body:
			ls = body.split()
			conf = (ls.pop(0)).lower()
			if self.compile_chat.match(conf):
				if conf not in Chats:
					confname = dynamic % (conf)
					if not check_nosimbols(confname):
						confname = encode_filename(confname)
					if not os.path.exists(confname):
						try:
							os.makedirs(confname, 0755)
						except Exception:
							confname = None
					if confname:
						codename, disp_, cPref, nick = None, None, None, DefNick
						while ls:
							x = ls.pop()
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
						inst = get_source(source[1], source[2])
						if GodName != inst:
							delivery(self.AnsBase[0] % (source[2], inst, conf))
						if not disp_:
							disp_ = IdleClient()
						Chats[conf] = sConf(conf, disp_, codename, cPref, nick)
						Chats[conf].load_all()
						Chats[conf].join()
						self.Check(conf)
						if Chats.has_key(conf) and Chats[conf].IamHere:
							Message(conf, self.AnsBase[7] % (ProdName, source[2]), disp_)
							answer = self.AnsBase[2] % (conf)
						else:
							answer = self.AnsBase[3] % (conf)
							sleep(3.6)
							if ejoinTimerName(conf) in ithr.getNames():
								answer += self.AnsBase[13]
					else:
						answer = self.AnsBase[15] % (conf)
				else:
					answer = self.AnsBase[5]
			else:
				answer = self.AnsBase[6] % (conf)
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_rejoin(self, stype, source, body, disp):
		if body:
			conf = body.split()[0].lower()
		else:
			conf = source[1]
		if Chats.has_key(conf):
			if online(Chats[conf].disp):
				Chats[conf].leave(self.AnsBase[8] % (source[2]))
				sleep(2)
				Chats[conf].join()
				self.Check(conf)
				if Chats.has_key(conf) and Chats[conf].IamHere:
					answer = AnsBase[4]
				else:
					answer = AnsBase[7]
			else:
				answer = self.AnsBase[14]
		else:
			answer = AnsBase[8]
		Answer(answer, stype, source, disp)

	def command_leave(self, stype, source, body, disp):
		if body:
			conf = body.split()[0].lower()
		else:
			conf = source[1]
		if not body or enough_access(source[1], source[2], 7) or conf == source[1]:
			if Chats.has_key(conf):
				source_ = get_source(source[1], source[2])
				if GodName != source_:
					delivery(self.AnsBase[4] % (source[2], source_, conf))
				info = self.AnsBase[9] % (source[2])
				Message(conf, info, Chats[conf].disp)
				sleep(2)
				Chats[conf].full_leave(info)
				if conf != source[1]:
					answer = self.AnsBase[10] % (conf)
			else:
				answer = AnsBase[8]
		else:
			answer = AnsBase[10]
		if locals().has_key(sBase[6]):
			Answer(answer, stype, source, disp)

	def command_reconnect(self, stype, source, body, disp):
		if body:
			Name = body.split()[0].lower()
		else:
			Name = get_disp(disp)
		if InstancesDesc.has_key(Name):
			thrName = "%s-%s" % (sBase[13], Name)
			if Clients.has_key(Name):
				for thr in ithr.enumerate():
					if thrName == thr.getName():
						thr.kill()
				if online(Name):
					try:
						Clients[Name].disconnect()
					except IOError:
						pass
			if connect_client(Name, InstancesDesc[Name])[0]:
				try:
					startThr(composeThr(Dispatcher, thrName, (Name,)), -1)
				except RuntimeError:
					answer = self.AnsBase[16]
				else:
					for conf in Chats.itervalues():
						if Name == conf.disp:
							conf.join()
					answer = AnsBase[4]
			else:
				answer = AnsBase[7]
		else:
			answer = self.AnsBase[17] % (Name)
		Answer(answer, stype, source, disp)

	def command_reload(self, stype, source, body, disp):
		exit_desclr = self.AnsBase[11] % (source[2])
		if body.lower() not in ("-s", "silent", "тихо".decode("utf-8")):
			if body:
				exit_desclr += self.AnsBase[1] % (body)
			for conf in Chats.itervalues():
				Message(conf.name, exit_desclr, conf.disp)
		sleep(6)
		VarCache["alive"] = False
		ithr.killAllThreads()
		for disp in Clients.keys():
			if online(disp):
				sUnavailable(disp, exit_desclr)
		call_sfunctions("03si")
		Exit("\n\nRestart command...", 0, 15)

	def command_exit(self, stype, source, body, disp):
		exit_desclr = self.AnsBase[12] % (source[2])
		if body.lower() not in ("-s", "silent", "тихо".decode("utf-8")):
			if body:
				exit_desclr += self.AnsBase[1] % (body)
			for conf in Chats.itervalues():
				Message(conf.name, exit_desclr, conf.disp)
		sleep(6)
		VarCache["alive"] = False
		ithr.killAllThreads()
		for disp in Clients.keys():
			if online(disp):
				sUnavailable(disp, exit_desclr)
		call_sfunctions("03si")
		Exit("\n\nSysExit command...", 1, 15)

	commands = (
		(command_join, "join", 7,),
		(command_rejoin, "rejoin", 7,),
		(command_leave, "leave", 6,),
		(command_reconnect, "reconnect", 8,),
		(command_reload, "reload", 8,),
		(command_exit, "exit", 8,)
	)
