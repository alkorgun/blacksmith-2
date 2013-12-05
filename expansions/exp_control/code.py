# coding: utf-8

#  BlackSmith mark.2
# exp_name = "exp_control" # /code.py v.x9
#  Id: 09~9c
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_expinfo(self, stype, source, body, disp):
		get_state = lambda filename: (self.AnsBase[1] if filename and os.path.isfile(filename) else self.AnsBase[2])
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
						answer += self.AnsBase[5] % ("; ".join(["%s: (%s)" % (eh, ", ".join([inst.__name__ for inst in ls])) for eh, ls in sorted(expansions[exp_name].desc.items())]))
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
				if (".svn" == exp_name) or expansions.has_key(exp_name):
					continue
				if os.path.isdir(os.path.join(ExpsDir, exp_name)):
					exp = expansion(exp_name)
					code_file = get_state(exp.file)
					insc_file = get_state(exp.insc)
					elexps.append("%d) %s - %s - %s" % (Number.plus(), exp_name, code_file, insc_file))
			elexps_len = len(elexps)
			if elexps_len:
				answer += self.AnsBase[9] % (elexps_len, chr(10).join(elexps))
		Answer(answer, stype, source, disp)

	ReloadSemaphore = ithr.Semaphore()

	def command_expload(self, stype, source, body, disp):
		if body:
			exp_name = body.strip("\\/").lower()
			if check_nosimbols(exp_name):
				exp = expansion(exp_name)
				if exp.isExp:
					backup = expansions.get(exp_name)
					with self.ReloadSemaphore:
						exp, exc = exp.load()
						if exp:
							try:
								exp.initialize_exp()
							except:
								exc = exc_info()
								exp.dels(True)
								answer = self.AnsBase[11] % (exp_name, "\n\t* %s: %s" % exc)
								if backup:
									backup.initialize_exp()
									backup.initialize_all()
									answer += self.AnsBase[13]
							else:
								exp.initialize_all()
								answer = self.AnsBase[10] % (exp_name)
						else:
							answer = self.AnsBase[11] % (exp_name, "\n\t* %s: %s" % exc)
							if backup:
								backup.initialize_exp()
								backup.initialize_all()
								answer += self.AnsBase[13]
				else:
					answer = self.AnsBase[7]
			else:
				answer = self.AnsBase[7]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_expunload(self, stype, source, body, disp):
		if body:
			body = body.split()
			exp_name = (body.pop(0)).lower()
			if expansions.has_key(exp_name):
				if body:
					handler, Name = None, body.pop(0)
					list = []
					for ls in expansions[exp_name].desc.values():
						for instance in ls:
							inst = instance.__name__
							list.append(inst)
							if inst == Name:
								handler = instance
								break
					if handler:
						with self.ReloadSemaphore:
							expansions[exp_name].clear_handlers(handler)
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
		Answer(answer, stype, source, disp)

	def command_tumbler(self, stype, source, body, disp):
		if body:
			ls = body.split()
			command = (ls.pop(0)).lower()
			if Cmds.has_key(command):
				cmd = Cmds.get(command)
				if ls:
					body = (ls.pop(0)).lower()
					if body in ("on", "1", "вкл".decode("utf-8")):
						if not cmd.isAvalable:
							if cmd.handler:
								cmd.isAvalable = True
								answer = AnsBase[4]
							else:
								answer = AnsBase[19] % (command)
						else:
							answer = self.AnsBase[16] % (command)
					elif body in ("off", "0", "выкл".decode("utf-8")):
						if cmd.isAvalable:
							if cmd.handler:
								cmd.isAvalable = False
								answer = AnsBase[4]
							else:
								answer = AnsBase[19] % (command)
						else:
							answer = self.AnsBase[17] % (command)
					else:
						answer = AnsBase[2]
				else:
					answer = self.AnsBase[16 if cmd.isAvalable else 17] % (command)
			else:
				answer = AnsBase[6]
		else:
			oCmds = [cmd_str for cmd_str, cmd in Cmds.iteritems() if not cmd.isAvalable]
			if oCmds:
				answer = ", ".join(oCmds)
			else:
				answer = self.AnsBase[18]
		Answer(answer, stype, source, disp)

	commands = (
		(command_expinfo, "expinfo", 7,),
		(command_expload, "expload", 8,),
		(command_expunload, "expunload", 8,),
		(command_tumbler, "tumbler", 8,)
	)
