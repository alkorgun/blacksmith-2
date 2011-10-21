# coding: utf-8

#  BlackSmith mark.2
exp_name = "exp_control" # /code.py v.x3
#  Id: 09~3a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_expinfo(ltype, source, body, disp):
	get_state = lambda filename: (CexpAnsBase[1] if os.path.isfile(filename) else CexpAnsBase[2])
	if body:
		exp_name = body.lower()
		if check_nosimbols(exp_name):
			if expansions.has_key(exp_name):
				answer = CexpAnsBase[0]
				code_file = get_state(expansions[exp_name].file)
				insc_file = get_state(expansions[exp_name].insc)
				answer += "\n%s - %s - %s - %s" % (exp_name, CexpAnsBase[3], code_file, insc_file)
				if len(expansions[exp_name].cmds):
					answer += CexpAnsBase[4] % (", ".join(expansions[exp_name].cmds))
				if len(expansions[exp_name].ls):
					answer += CexpAnsBase[5] % (", ".join(expansions[exp_name].ls))
			else:
				exp = expansion(exp_name)
				if os.path.exists(exp.path):
					answer = CexpAnsBase[0]
					code_file = get_state(exp.file)
					insc_file = get_state(exp.insc)
					answer += "\n%s - %s - %s - %s" % (exp_name, CexpAnsBase[6], code_file, insc_file)
				else:
					answer = CexpAnsBase[7]
		else:
			answer = CexpAnsBase[7]
	else:
		answer, Number = CexpAnsBase[8], itypes.Number()
		for exp_name in expansions.keys():
			code_file = get_state(expansions[exp_name].file)
			insc_file = get_state(expansions[exp_name].insc)
			answer += "\n%d) %s - %s - %s" % (Number.plus(), exp_name, code_file, insc_file)
		elexps = []
		for exp_name in sorted(os.listdir(PlugsDir)):
			if (".svn") == (exp_name) or expansions.has_key(exp_name):
				continue
			if os.path.isdir(os.path.join(PlugsDir, exp_name)):
				exp = expansion(exp_name)
				code_file = get_state(exp.file)
				insc_file = get_state(exp.insc)
				elexps.append("%d) %s - %s - %s" % (Number.plus(), exp_name, code_file, insc_file))
		elexps_len = len(elexps)
		if elexps_len:
			answer += CexpAnsBase[9] % (elexps_len, chr(10).join(elexps))
	Answer(answer, ltype, source, disp)

ReloadSemaphore = iThr.Semaphore()

def command_expload(ltype, source, body, disp):
	if body:
		exp_name = body.lower()
		if check_nosimbols(exp_name):
			if expansions.has_key(exp_name):
				if os.path.isfile(expansions[exp_name].file):
					with ReloadSemaphore:
						loaded = expansions[exp_name].load()
						if loaded[1]:
							expansions[exp_name].initialize_all()
							answer = CexpAnsBase[10] % (loaded[0])
						else:
							expansions[exp_name].dels(True)
							answer = CexpAnsBase[11] % (loaded[0], "\n\t* %s: %s") % (loaded[2])
				else:
					answer = CexpAnsBase[12]
			else:
				exp = expansion(exp_name)
				if exp.isExp:
					with ReloadSemaphore:
						loaded = exp.load()
						if loaded[1] and expansions.has_key(exp_name):
							expansions[exp_name].initialize_all()
							answer = CexpAnsBase[10] % (loaded[0])
						else:
							exp.dels(True)
							if loaded[2]:
								answer = CexpAnsBase[11] % (loaded[0], "\n\t* %s: %s") % (loaded[2])
							else:
								answer = CexpAnsBase[13] % (loaded[0])
				else:
					answer = CexpAnsBase[7]
		else:
			answer = CexpAnsBase[7]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_expunload(ltype, source, body, disp):
	if body:
		body = body.split()
		exp_name = (list_.pop(0)).lower()
		if expansions.has_key(exp_name):
			if body:
				handler, func_name_ = None, body.pop(0)
				for instance in expansions[exp_name].hnds.keys():
					if func_name_ == instance.func_name:
						handler = instance
				if handler:
					with ReloadSemaphore:
						expansions[exp_name].funcs_del(handler)
					answer = AnsBase[4]
				else:
					exp_funcs = expansions[exp_name].hnds.keys()
					if exp_funcs:
						list = [x.func_name for x in exp_funcs]
						answer = CexpAnsBase[14] % (", ".join(sorted(list)))
					else:
						answer = CexpAnsBase[15] % (exp_name)
			else:
				with ReloadSemaphore:
					expansions[exp_name].dels(True)
				answer = AnsBase[4]
		else:
			answer = CexpAnsBase[7]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_states(ltype, source, body, disp):
	if body:
		list_ = body.split()
		cmd = (list_.pop(0)).lower()
		if Cmds.has_key(cmd):
			if list_:
				body = (list_.pop(0)).lower()
				if body in ("off", "выкл".decode("utf-8")):
					if Cmds[cmd].isAvalable:
						if Cmds[cmd].handler:
							Cmds[cmd].isAvalable = False
							answer = AnsBase[4]
						else:
							answer = AnsBase[19] % (cmd)
					else:
						answer = CexpAnsBase[16] % (cmd)
				elif body in ("on", "вкл".decode("utf-8")):
					if not Cmds[cmd].isAvalable:
						if Cmds[cmd].handler:
							Cmds[cmd].isAvalable = True
							answer = AnsBase[4]
						else:
							answer = AnsBase[19] % (cmd)
					else:
						answer = CexpAnsBase[17] % (cmd)
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[6]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_expinfo, command_expload, command_expunload, command_states])
expansions[exp_name].ls.extend(["CexpAnsBase", "ReloadSemaphore"])

command_handler(command_expinfo, {"RU": "плагинфо", "EN": "expinfo"}, 7, exp_name)
command_handler(command_expload, {"RU": "подгрузи", "EN": "expload"}, 8, exp_name)
command_handler(command_expunload, {"RU": "выгрузи", "EN": "unload"}, 8, exp_name)
command_handler(command_states, {"RU": "команда", "EN": "command"}, 8, exp_name)
