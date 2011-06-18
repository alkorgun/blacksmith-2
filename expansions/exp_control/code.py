# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "exp_control" # /code.py v.x2
#  Id: 09~2a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_expinfo(ltype, source, body, disp):
	get_state = lambda filename: (cexp_answers[1] if os.path.isfile(filename) else cexp_answers[2])
	if body:
		exp_name = body.lower()
		if expansions.has_key(exp_name):
			answer = cexp_answers[0]
			code_file = get_state(expansions[exp_name].file)
			insc_file = get_state(expansions[exp_name].insc)
			answer += "\n%s - %s - %s - %s" % (exp_name, cexp_answers[3], code_file, insc_file)
			if len(expansions[exp_name].cmds):
				answer += cexp_answers[4] % (", ".join(expansions[exp_name].cmds))
			if len(expansions[exp_name].ls):
				answer += cexp_answers[5] % (", ".join(expansions[exp_name].ls))
		else:
			exp = expansion(exp_name)
			if os.path.exists(exp.path):
				answer = cexp_answers[0]
				code_file = get_state(exp.file)
				insc_file = get_state(exp.insc)
				answer += "\n%s - %s - %s - %s" % (exp_name, cexp_answers[6], code_file, insc_file)
			else:
				answer = cexp_answers[7]
	else:
		answer, number = cexp_answers[8], itypes.Number()
		for exp_name in expansions.keys():
			code_file = get_state(expansions[exp_name].file)
			insc_file = get_state(expansions[exp_name].insc)
			answer += "\n%d) %s - %s - %s" % (number.plus(), exp_name, code_file, insc_file)
		elexps = []
		for exp_name in sorted(os.listdir(PlugsDir)):
			if (".svn") == (exp_name) or expansions.has_key(exp_name):
				continue
			if os.path.isdir(os.path.join(PlugsDir, exp_name)):
				exp = expansion(exp_name)
				code_file = get_state(exp.file)
				insc_file = get_state(exp.insc)
				elexps.append("%d) %s - %s - %s" % (number.plus(), exp_name, code_file, insc_file))
		elexps_len = len(elexps)
		if elexps_len:
			answer += cexp_answers[9] % (elexps_len, "\n".join(elexps))
	Answer(answer, ltype, source, disp)

def command_expload(ltype, source, body, disp):
	if body:
		exp_name = body.lower()
		if expansions.has_key(exp_name):
			if os.path.isfile(expansions[exp_name].file):
				with Semph:
					loaded = expansions[exp_name].load()
					if loaded[1]:
						expansions[exp_name].initialize_all()
						answer = cexp_answers[10] % (loaded[0])
					else:
						expansions[exp_name].dels(True)
						answer = cexp_answers[11] % (loaded[0], "\n\t* %s: %s") % (loaded[2])
			else:
				answer = cexp_answers[12]
		else:
			exp = expansion(exp_name)
			if exp.isExp:
				with Semph:
					loaded = exp.load()
					if loaded[1] and expansions.has_key(exp_name):
						expansions[exp_name].initialize_all()
						answer = cexp_answers[10] % (loaded[0])
					else:
						exp.dels(True)
						if loaded[2]:
							answer = cexp_answers[11] % (loaded[0], "\n\t* %s: %s") % (loaded[2])
						else:
							answer = cexp_answers[13] % (loaded[0])
			else:
				answer = cexp_answers[7]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_expunload(ltype, source, body, disp):
	if body:
		body = body.split()
		exp_name = body[0].lower()
		if expansions.has_key(exp_name):
			if len(body) >= 2:
				handler, func_name_ = None, body[1]
				for instance in expansions[exp_name].hnds.keys():
					if func_name_ == instance.func_name:
						handler = instance
				if handler:
					with Semph:
						expansions[exp_name].funcs_del(handler)
					answer = AnsBase[4]
				else:
					exp_funcs = expansions[exp_name].hnds.keys()
					if exp_funcs:
						list = [x.func_name for x in exp_funcs]
						answer = cexp_answers[14] % (", ".join(sorted(list)))
					else:
						answer = cexp_answers[15] % (exp_name)
			else:
				with Semph:
					expansions[exp_name].dels(True)
				answer = AnsBase[4]
		else:
			answer = cexp_answers[7]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_states(ltype, source, body, disp):
	if body:
		list = body.split()
		cmd = list[0].lower()
		if Cmds.has_key(cmd):
			if len(list) >= 2:
				body = list[1].lower()
				if body in ["off", "выкл".decode("utf-8")]:
					if Cmds[cmd].isAvalable:
						if Cmds[cmd].handler:
							Cmds[cmd].isAvalable = False
							answer = AnsBase[4]
						else:
							answer = AnsBase[19] % (cmd)
					else:
						answer = cexp_answers[16] % (cmd)
				elif body in ["on", "вкл".decode("utf-8")]:
					if not Cmds[cmd].isAvalable:
						if Cmds[cmd].handler:
							Cmds[cmd].isAvalable = True
							answer = AnsBase[4]
						else:
							answer = AnsBase[19] % (cmd)
					else:
						answer = cexp_answers[17] % (cmd)
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
expansions[exp_name].ls.extend(["cexp_answers"])

command_handler(command_expinfo, {"RU": "плагинфо", "EN": "expinfo"}, 7, exp_name)
command_handler(command_expload, {"RU": "подгрузи", "EN": "expload"}, 8, exp_name)
command_handler(command_expunload, {"RU": "выгрузи", "EN": "unload"}, 8, exp_name)
command_handler(command_states, {"RU": "командa", "EN": "command"}, 8, exp_name)
