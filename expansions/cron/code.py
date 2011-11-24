# coding: utf-8

#  BlackSmith mark.2
exp_name = "cron" # /code.py v.x3
#  Id: 27~2a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

CronFile = dynamic % ("cdesc.db")

CronDesc, CronCounter = dict(), itypes.Number()

def def_cron():
	exp_name = "cron"

	def exe_cron(command, instance, ls, repeat = ()):
		inst = get_source(ls[1][1], ls[1][2])
		if inst == instance or (not inst or not instance):
			gt = time.mktime(time.gmtime())
			rlen = len(repeat)
			if rlen == 1 and (repeat[0] >= 360):
				Answer(CronAnsBase[0] % (command), ls[0], ls[1], ls[3])
			Cmds[command].execute(*ls)
			if rlen == 2:
				seconds, repeats = (repeat)
				if repeats.reduce():
					CronDesc[CronCounter.plus()] = ((seconds + gt), (command, instance, ls, repeat))

	while VarCache["alive"]:
		time.sleep(2)
		if not expansions.has_key(exp_name):
			break
		Time = time.mktime(time.gmtime())
		for id, (date, ls) in CronDesc.items():
			if Time > date:
				if Cmds.has_key(ls[0]):
					sThread("command(cron)", exe_cron, ls)
				del CronDesc[id]

def getDate(ls, sft, sftime = "%H:%M:%S (%d.%m.%Y)"):
	ls[5] += sft
	while ls[5] >= 60:
		ls[5] -= 60
		ls[4] += 1
		if ls[4] >= 60:
			ls[4] -= 60
			ls[3] += 1
			if ls[3] >= 24:
				ls[3] -= 24
				ls[2] += 1
				days = (0, 31, (28 if (ls[0] % 4) else 29), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
				if ls[2] > days[ls[1]]:
					ls[2] -= days[ls[1]]
					ls[1] += 1
					if ls[1] > 12:
						ls[1] -= 12
						ls[0] += 1
	return time.strftime(sftime, time.struct_time(ls))

def add_cron(disp, ls, body, Te, source, ltype, gt, answer, repeat, **ext):
	cmd = (ls.pop(0)).lower()
	if Cmds.has_key(cmd):
		if enough_access(source[1], source[2], Cmds[cmd].access):
			if ls:
				body = body[((body.lower()).find(cmd) + (len(cmd) + 1)):].strip()
			else:
				body = ""
			if 1024 >= len(body):
				Time = time.mktime(gt)
				instance = get_source(source[1], source[2])
				CronDesc[CronCounter.plus()] = ((Te + Time), (cmd, instance, (ltype, source, body, get_disp(disp)), repeat))
				cdesc_save()
			else:
				answer = AnsBase[5]
		else:
			answer = AnsBase[10]
	else:
		answer = AnsBase[6]
	return answer

def command_cron(ltype, source, body, disp):
	gt = time.gmtime()
	if body:
		ls = body.split()
		if len(ls) >= 2:
			Mode = (ls.pop(0)).lower()
			if Mode in ("stop", "стоп".decode("utf-8")):
				id = ls.pop(0)
				if isNumber(id):
					id = int(id)
					if CronDesc.has_key(id):
						if enough_access(source[1], source[2], 7):
							del CronDesc[id]
							answer = AnsBase[4]
						else:
							date, ls = CronDesc.get(id)
							if ls[1] == get_source(source[1], source[2]):
								del CronDesc[id]
								answer = AnsBase[4]
							else:
								answer = AnsBase[10]
					else:
						answer = CronAnsBase[1] % (id)
				else:
					answer = AnsBase[30]
			elif Mode in ("cycled", "цикл".decode("utf-8")):
				if len(ls) >= 3:
					Te = ls.pop(0)
					Tr = ls.pop(0)
					if isNumber(Te) and isNumber(Tr):
						Te, Tr = int(Te), int(Tr)
						if Te <= 240 and Tr > 4:
							answer = CronAnsBase[2]
						elif 59 < Te and Te*Tr <= 4147200 or enough_access(source[1], source[2], 7):
							t_ls, repeat = [Te], (Te, itypes.Number(Tr))
							for x in xrange(1, Tr):
								t_ls.append(t_ls[-1] + Te)
							ltls = len(t_ls)
							t_ls = enumerated_list([getDate(list(gt), Tx) for Tx in t_ls[:8]])
							if ltls > 8:
								t_ls += CronAnsBase[3] % (ltls - 8)
							answer = CronAnsBase[4] % (t_ls)
							answer = add_cron(**locals())
						else:
							answer = CronAnsBase[5]
					else:
						answer = AnsBase[30]
				else:
					answer = AnsBase[2]
			elif Mode in ("date", "дата".decode("utf-8")):
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
					except:
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
							except:
								answer = AnsBase[2]
					if not locals().has_key(Types[12]):
						try:
							date = time.struct_time(date)
						except:
							answer = AnsBase[2]
						else:
							Time, Te = time.mktime(gt), time.mktime(date)
							if Te > Time:
								Te = (Te - Time)
								if 59 < Te <= 4147200 or enough_access(source[1], source[2], 7):
									repeat = (Te,)
									answer = CronAnsBase[6] % time.strftime("%H:%M:%S (%d.%m.%Y)", date)
									answer = add_cron(**locals())
								else:
									answer = CronAnsBase[5]
							else:
								answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			elif isNumber(Mode):
				Te = int(Mode)
				if 59 < Te <= 4147200 or enough_access(source[1], source[2], 7):
					repeat = (Te,)
					answer = CronAnsBase[6] % getDate(list(gt), Te)
					answer = add_cron(**locals())
				else:
					answer = CronAnsBase[5]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[2]
	elif not CronDesc:
		answer = CronAnsBase[7]
	else:
		Te = time.mktime(gt)
		ls = []
		for id, (date, desc) in CronDesc.items():
			if date > Te:
				line = "%d (%s) [%s]" % (id, desc[0], getDate(list(gt), int(date - Te)))
				ls.append(line)
		answer = CronAnsBase[8] % enumerated_list(sorted(ls))
	Answer(answer, ltype, source, disp)

def start_cron():
	Name = def_cron.func_name
	for Thr in iThr.enumerate():
		if Thr._Thread__name.startswith(Name):
			Thr.kill()
	if initialize_file(CronFile, "({}, 0)"):
		cdesc, ccnt = eval(get_file(CronFile))
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
		CronDesc.update(cdesc)
		CronCounter.__init__(ccnt)
	composeThr(def_cron, Name).start()

def cdesc_save(conf = None):
	if not conf:
		cdesc = CronDesc.copy()
		for id, (date, ls) in cdesc.items():
			command, instance, ls__, repeat = ls
			if len(repeat) == 2:
				seconds, repeats = repeat
				repeat = (seconds, int(repeats))
			ltype, source, body, disp = ls__
			one, two, three = source
			source = (str(one), two, three)
			ls__ = (ltype, source, body, disp)
			ls = (command, instance, ls__, repeat)
			cdesc[id] = (date, ls)
		cat_file(CronFile, str((cdesc, int(CronCounter))))

expansions[exp_name].funcs_add([def_cron, getDate, add_cron, command_cron, start_cron, cdesc_save])
expansions[exp_name].ls.extend(["CronAnsBase", "CronDesc", "CronCounter"])

command_handler(command_cron, {"RU": "хрон", "EN": "cron"}, 5, exp_name)

handler_register(start_cron, "02si", exp_name)
handler_register(cdesc_save, "03si", exp_name)
