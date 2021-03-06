# coding: utf-8

#  BlackSmith mark.2
# exp_name = "cron" # /code.py v.x6
#  Id: 27~5c
#  Code © (2010-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	CronFile = dynamic % ("cdesc.db")

	CronDesc, CronCounter = dict(), itypes.Number()

	def def_cron(self):

		def exe_cron(command, instance, ls, repeat = ()):
			inst = get_source(ls[1][1], ls[1][2])
			if inst == instance or (not inst or not instance):
				gt = time.mktime(time.gmtime())
				rlen = len(repeat)
				if rlen == 1 and (repeat[0] >= 360):
					Answer(self.AnsBase[0] % (command), ls[0], ls[1], ls[3])
				Cmds[command].execute(*ls)
				if rlen == 2:
					seconds, repeats = (repeat)
					if repeats.reduce():
						self.CronDesc[self.CronCounter.plus()] = ((seconds + gt), (command, instance, ls, repeat))

		while VarCache["alive"]:
			sleep(2)
			if not expansions.has_key(self.name):
				break
			Time = time.mktime(time.gmtime())
			for id, (date, ls) in self.CronDesc.items():
				if Time > date:
					if Cmds.has_key(ls[0]):
						sThread("command(cron)", exe_cron, ls)
					del self.CronDesc[id]

	def add_cron(self, disp, ls, body, Te, source, stype, gt, answer, repeat, **etc):
		cmd = (ls.pop(0)).lower()
		if Cmds.has_key(cmd):
			if enough_access(source[1], source[2], Cmds[cmd].access):
				if ls:
					body = body[((body.lower()).find(cmd) + len(cmd)):].strip()
				else:
					body = ""
				if 1024 >= len(body):
					instance = get_source(source[1], source[2])
					self.CronDesc[self.CronCounter.plus()] = (Te, (cmd, instance, (stype, source, body, get_disp(disp)), repeat))
					self.cdesc_save()
				else:
					answer = AnsBase[5]
			else:
				answer = AnsBase[10]
		else:
			answer = AnsBase[6]
		return answer

	def command_cron(self, stype, source, body, disp):
		gt = time.gmtime()
		if body:
			ls = body.split()
			if len(ls) >= 2:
				arg0 = (ls.pop(0)).lower()
				if arg0 in ("stop", "стоп".decode("utf-8")):
					id = ls.pop(0)
					if isNumber(id):
						id = int(id)
						if id in self.CronDesc:
							if enough_access(source[1], source[2], 7):
								del self.CronDesc[id]; self.cdesc_save()
								answer = AnsBase[4]
							else:
								date, ls = self.CronDesc[id]
								if ls[1] == get_source(source[1], source[2]):
									del self.CronDesc[id]; self.cdesc_save()
									answer = AnsBase[4]
								else:
									answer = AnsBase[10]
						else:
							answer = self.AnsBase[1] % (id)
					else:
						answer = AnsBase[30]
				elif arg0 in ("cycled", "цикл".decode("utf-8")):
					if len(ls) >= 3:
						Te = ls.pop(0)
						Tr = ls.pop(0)
						if isNumber(Te) and isNumber(Tr):
							Te, Tr = int(Te), int(Tr)
							if Te <= 240 and Tr > 4:
								answer = self.AnsBase[2]
							elif 59 < Te and Te*Tr <= 4147200 or enough_access(source[1], source[2], 7):
								t_ls, repeat = [Te], (Te, itypes.Number(Tr))
								for x in xrange(7):
									t_ls.append(t_ls[-1] + Te)
								Time = time.mktime(gt)
								Te += Time
								answer = self.AnsBase[4] % enumerated_list([time.ctime(dt + Time) for dt in t_ls])
								if Tr > 8:
									answer += self.AnsBase[3] % (Tr - 8)
								add = self.add_cron
								del self
								answer = add(**locals())
							else:
								answer = self.AnsBase[5]
						else:
							answer = AnsBase[30]
					else:
						answer = AnsBase[2]
				elif arg0 in ("date", "дата".decode("utf-8")):
					if len(ls) >= 2:
						date = list(gt)
						Te = ls.pop(0)
						Te = Te.split("&")
						date[6], date[7], date[8] = 0, 0, 0
						Time = Te.pop(0)
						Time = Time.split(":")
						try:
							date[3] = int(Time.pop(0))
							if Time:
								date[4] = int(Time.pop(0))
								if Time:
									date[5] = int(Time.pop(0))
								else:
									date[5] = 0
							else:
								date[4], date[5] = 0, 0
						except Exception:
							answer = AnsBase[2]
						else:
							Date = (Te.pop(0) if Te else None)
							if Date:
								Date = Date.split(".")
								try:
									date[2] = int(Date.pop(0))
									if Date:
										date[1] = int(Date.pop(0))
										if Date:
											date[0] = int(Date.pop(0))
								except Exception:
									answer = AnsBase[2]
						if not locals().has_key(sBase[6]):
							try:
								date = time.struct_time(date)
							except Exception:
								answer = AnsBase[2]
							else:
								Time, Te = time.mktime(gt), time.mktime(date)
								if Te > Time:
									if 59 < Te <= 4147200 or enough_access(source[1], source[2], 7):
										repeat = ((Te - Time),)
										try:
											answer = self.AnsBase[6] % time.ctime(Te)
										except ValueError:
											answer = self.AnsBase[9]
										else:
											add = self.add_cron
											del self
											answer = add(**locals())
									else:
										answer = self.AnsBase[5]
								else:
									answer = AnsBase[2]
					else:
						answer = AnsBase[2]
				elif isNumber(arg0):
					Te = int(arg0)
					if 59 < Te <= 4147200 or enough_access(source[1], source[2], 7):
						repeat = (Te,)
						Te += time.mktime(gt)
						answer = self.AnsBase[6] % time.ctime(Te)
						add = self.add_cron
						del self
						answer = add(**locals())
					else:
						answer = self.AnsBase[5]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		elif not self.CronDesc:
			answer = self.AnsBase[7]
		else:
			Time = time.mktime(gt)
			ls = []
			for id, (date, desc) in sorted(self.CronDesc.items()):
				if date > Time:
					line = "%d (%s) [%s]" % (id, desc[0], time.ctime(date))
					ls.append(line)
			answer = self.AnsBase[8] % enumerated_list(ls)
		Answer(answer, stype, source, disp)

	def start_cron(self):
		Name = self.def_cron.__name__
		for thr in ithr.enumerate():
			if thr.name.startswith(Name):
				thr.kill()
		if initialize_file(self.CronFile, "({}, 0)"):
			cdesc, ccnt = eval(get_file(self.CronFile))
			Time = time.mktime(time.gmtime())
			for id, (date, ls) in cdesc.items():
				if Time > date:
					del cdesc[id]
				elif len(ls[3]) == 2:
					command, instance, ls__, repeat = ls
					seconds, repeats = repeat
					repeat = (seconds, itypes.Number(repeats))
					ls = (command, instance, ls__, repeat)
					cdesc[id] = (date, ls)
			self.CronDesc.update(cdesc)
			self.CronCounter.__init__(ccnt)
		composeThr(self.def_cron, Name).start()

	def cdesc_save(self, conf = None):
		if not conf:
			cdesc = self.CronDesc.copy()
			for id, (date, ls) in cdesc.items():
				command, instance, ls__, repeat = ls
				if len(repeat) == 2:
					seconds, repeats = repeat
					repeat = (seconds, int(repeats))
				stype, source, body, disp = ls__
				one, two, three = source
				source = (str(one), two, three)
				ls__ = (stype, source, body, disp)
				ls = (command, instance, ls__, repeat)
				cdesc[id] = (date, ls)
			cat_file(self.CronFile, str((cdesc, int(self.CronCounter))))

	commands = ((command_cron, "cron", 5,),)

	handlers = (
		(start_cron, "02si"),
		(cdesc_save, "03si")
	)
