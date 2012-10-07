# coding: utf-8

#  BlackSmith mark.2
exp_name = "exp_control" # /code.py v.x6
#  Id: 09~6b
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_expinfo(self, ltype, source, body, disp):
		get_state = lambda filename: (self.AnsBase[1] if os.path.isfile(filename) else self.AnsBase[2])
		if body:
			exp_name = body.lower()
			if check_nosimbols(exp_name):
				if expansions.has_key(exp_name):
					answer = self.AnsBase[0]
					code_file = get_state(expansions[exp_name].file)
					insc_file = get_state(expansions[exp_name].insc)
					answer += "\n%s - %s - %s - %s" % (exp_name, self.AnsBase[3], code_file, insc_file)
					if expansions[exp_name].cmds:
						answer += self.AnsBase[4] % (", ".join(expansions[exp_name].cmds))
					if expansions[exp_name].desc:
						answer += self.AnsBase[5] % ("; ".join(["%s: (%s)" % (eh, ", ".join([inst.func_name for inst in ls])) for eh, ls in sorted(expansions[exp_name].desc.items())]))
				else:
					exp = expansion(exp_name)
					if os.path.exists(exp.path):
						answer = self.AnsBase[0]
						code_file = get_state(exp.file)
						insc_file = get_state(exp.insc)
						answer += "\n%s - %s - %s - %s" % (exp_name, self.AnsBase[6], code_file, insc_file)
					else:
						answer = self.AnsBase[7]
			else:
				answer = self.AnsBase[7]
		else:
			answer, Number = self.AnsBase[8], itypes.Number()
			for exp_name in sorted(expansions.keys()):
				code_file = get_state(expansions[exp_name].file)
				insc_file = get_state(expansions[exp_name].insc)
				answer += "\n%d) %s - %s - %s" % (Number.plus(), exp_name, code_file, insc_file)
			elexps = []
			for exp_name in sorted(os.listdir(ExpsDir)):
				if (".svn") == (exp_name) or expansions.has_key(exp_name):
					continue
				if os.path.isdir(os.path.join(ExpsDir, exp_name)):
					exp = expansion(exp_name)
					code_file = get_state(exp.file)
					insc_file = get_state(exp.insc)
					elexps.append("%d) %s - %s - %s" % (Number.plus(), exp_name, code_file, insc_file))
			elexps_len = len(elexps)
			if elexps_len:
				answer += self.AnsBase[9] % (elexps_len, chr(10).join(elexps))
		Answer(answer, ltype, source, disp)

	ReloadSemaphore = iThr.Semaphore()

	def command_expload(self, ltype, source, body, disp):
		if body:
			exp_name = body.lower()
			if check_nosimbols(exp_name):
				if expansions.has_key(exp_name):
					if os.path.isfile(expansions[exp_name].file):
						with self.ReloadSemaphore:
							rslt = expansions[exp_name].load()
							if rslt[1]:
								exp = expansion_temp(exp_name)
								exp.initialize_exp()
								exp.initialize_all()
								answer = self.AnsBase[10] % (rslt[0])
							else:
								expansions[exp_name].dels(True)
								answer = self.AnsBase[11] % (rslt[0], "\n\t* %s: %s") % (rslt[2])
					else:
						answer = self.AnsBase[12]
				else:
					expansions[exp_name] = exp = expansion(exp_name)
					if exp.isExp:
						with self.ReloadSemaphore:
							rslt = exp.load()
							if rslt[1] and expansions.has_key(exp_name):
								exp = expansion_temp(exp_name)
								exp.initialize_exp()
								exp.initialize_all()
								answer = self.AnsBase[10] % (rslt[0])
							else:
								exp.dels(True)
								if rslt[2]:
									answer = self.AnsBase[11] % (rslt[0], "\n\t* %s: %s") % (rslt[2])
								else:
									answer = self.AnsBase[13] % (rslt[0])
					else:
						exp.dels(True)
						answer = self.AnsBase[7]
			else:
				answer = self.AnsBase[7]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_expunload(self, ltype, source, body, disp):
		if body:
			body = body.split()
			exp_name = (body.pop(0)).lower()
			if expansions.has_key(exp_name):
				if body:
					handler, Name = None, body.pop(0)
					list = []
					for ls in expansions[exp_name].desc.values():
						for instance in ls:
							inst = instance.func_name
							list.append(inst)
							if inst == Name:
								handler = instance
								break
					if handler:
						with self.ReloadSemaphore:
							expansions[exp_name].funcs_del(handler)
						answer = AnsBase[4]
					elif list:
						answer = self.AnsBase[14] % (", ".join(sorted(list)))
					else:
						answer = self.AnsBase[15] % (exp_name)
				else:
					with self.ReloadSemaphore:
						expansions[exp_name].dels(True)
					answer = AnsBase[4]
			else:
				answer = self.AnsBase[7]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_states(self, ltype, source, body, disp):
		if body:
			ls = body.split()
			command = (ls.pop(0)).lower()
			if Cmds.has_key(command):
				if ls:
					body = (ls.pop(0)).lower()
					if body in ("on", "вкл".decode("utf-8")):
						if not Cmds[command].isAvalable:
							if Cmds[command].handler:
								Cmds[command].isAvalable = True
								answer = AnsBase[4]
							else:
								answer = AnsBase[19] % (command)
						else:
							answer = self.AnsBase[16] % (command)
					elif body in ("off", "выкл".decode("utf-8")):
						if Cmds[command].isAvalable:
							if Cmds[command].handler:
								Cmds[command].isAvalable = False
								answer = AnsBase[4]
							else:
								answer = AnsBase[19] % (command)
						else:
							answer = self.AnsBase[17] % (command)
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[6]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	commands = (
		(command_expinfo, "expinfo", 7,),
		(command_expload, "expload", 8,),
		(command_expunload, "expunload", 8,),
		(command_states, "command", 8,)
					)
