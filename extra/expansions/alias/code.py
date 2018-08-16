# coding: utf-8

#  BlackSmith mark.2
# exp_name = "alias" # /code.py v.x4 alpha
#  Id: 35~4c
#  Code © (2012-2014) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		check_sqlite()
		expansion.__init__(self, name)

	On = True

	AliasFile = dynamic % ("alias.db")
	ChatAliasFile = "alias.db"
	MacroHelpBase = dynamic % ("macro.db")
	ChatMacroHelpBase = "macro.db"
	HelpFile = "alias.%s.app"

	alias, macro, command, set, message, null = "alias", "macro", "command", "set", "message", "null" # important keywords

	Template = {
		"macro": {},
		"message": {},
		"/me": {},
		"subject": {},
		"join": {},
		"version": {},
		"leave": {},
		"ban": {},
		"kick": {},
		"nick": {},
		"role": {},
		"status": {}
	}

	AliasDesc = Template.copy()
	ChatAliasDesc = {}

	Taboo = {}

	Cache = {}

	conds = {
		"null": None,
		"is": lambda attr, clause: (clause == attr),
		"is_not": lambda attr, clause: (clause != attr),
		"starts": lambda attr, clause: attr.startswith(clause),
		"not_starts": lambda attr, clause: not attr.startswith(clause),
		"ends": lambda attr, clause: attr.endswith(clause),
		"not_ends": lambda attr, clause: not attr.endswith(clause),
		"cont": lambda attr, clause: (clause in attr),
		"not_cont": lambda attr, clause: (clause not in attr),
		"in": lambda attr, clause: (attr in clause),
		"not_in": lambda attr, clause: (attr not in clause),
		"len_more": lambda attr, clause: (len(attr) > clause),
		"len_less": lambda attr, clause: (len(attr) < clause),
		"re": lambda attr, clause: clause.search(attr)
	}

	funcs = {
		"outcast": (sConf.outcast, sBase[11]),
		"none": (sConf.none, sBase[11]),
		"member": (sConf.member, sBase[11]),
		"admin": (sConf.admin, sBase[11]),
		"owner": (sConf.owner, sBase[11]),
		"kick": (sConf.kick, sBase[12]),
		"visitor": (sConf.visitor, sBase[12]),
		"participant": (sConf.participant, sBase[12]),
		"moder": (sConf.moder, sBase[12])
	}

	flags = ("strip", "lower", "layout")

	compile_rand = compile__("\$rand\((\d+?),\s*(\d+?)\)")
	compile_rand_user = compile__("\$rand_user")
	compile_rand_choice = compile__("\$rand\(\[(.+?)\]\)", 16)

	rand_user = "$rand_user"
	sep = chr(124)*2

	def sub_rand(self, obj):
		try:
			number = str(randrange(*[int(numb) for numb in obj.groups()]))
		except Exception:
			number = "0"
		return number

	sub_rand_choice = lambda self, obj: choice((obj.group(1)).split(self.sep))

	def rand(self, chat, body):
		body = self.compile_rand_choice.sub(self.sub_rand_choice, body)
		body = self.compile_rand.sub(self.sub_rand, body)
		if chat and self.rand_user in body:
			ls = chat.get_nicks()
			body = self.compile_rand_user.sub(lambda obj: choice(ls), body)
		return body

	def four_args(self, ls, args):
		while len(args) < 4:
			args.append(ls.pop())
		return args

	def execute_macro(self, chat, isConf, command, body, access, args):
		stype, source, nick, args, disp = args
		source = (source, chat, nick)
		if enough_access(chat, nick, access):
			cmd = Cmds[command]
			if cmd.isAvalable and cmd.handler:
				if isConf:
					user = Chats[chat].get_user(nick)
					(aff, role), jid = user.role, user.source
				else:
					(aff, role), jid = ("none",)*2, None
				arg0, arg1, arg2, arg3 = self.four_args([role, aff, stype, chat], args.split(None, 3))
				body = self.rand(Chats[chat] if isConf else None, body % vars())
				Info["cmd"].plus()
				cmd.handler(cmd.exp, stype, source, body, disp)
				cmd.numb.plus()
				if jid:
					cmd.desc.add(jid)
			else:
				answer = AnsBase[19] % (self.name)
		else:
			answer = AnsBase[10]
		if locals().has_key(sBase[6]):
			Answer(answer, stype, source, disp)

	def __call__(self, chat, isConf, macro, *args):
		desc = self.AliasDesc[self.macro].get(macro)
		if not desc and isConf:
			desc = self.ChatAliasDesc[chat][self.macro].get(macro)
		if desc:
			command, body, access = desc
			if command in Cmds:
				if not isConf or (command not in Chats[chat].oCmds and \
									macro not in self.Taboo[chat]):
					sThread(self.macro, self.execute_macro, (chat, isConf, command, body, access, args), macro)
				xmpp_raise()

	__contains__ = lambda self, ls: (ls[0] in self.AliasDesc[self.macro] or (ls[1] in self.ChatAliasDesc and ls[0] in self.ChatAliasDesc[ls[1]][self.macro]))

	risky = ("outcast", "kick", "visitor")

	def execute(self, chat, desc, Vars):
		atype, func, body = desc
		body = self.rand(chat, body % Vars)
		if atype == self.command:
			if func in Cmds and not func in chat.oCmds:
				cmd = Cmds[func]
				if cmd.isAvalable and cmd.handler:
					source = ("%s/%s" % (chat.name, chat.nick), chat.name, chat.nick)
					Info["cmd"].plus()
					sThread(self.alias, cmd.handler, (cmd.exp, Vars.get("stype", sBase[1]), source, body, chat.disp), cmd.name)
					cmd.numb.plus()
		elif atype == self.message:
			if func == sBase[0]:
				source = chat.name
			else:
				source = "%s/%s" % (chat.name, Vars["nick"])
			Message(source, body, chat.disp)
		elif self.funcs.has_key(func):
			access = get_access(chat.name, Vars["nick"])
			if access != 6 and (access < 7 or func not in self.risky):
				func, attr = self.funcs[func]
				attr = Vars.get(attr)
				if attr:
					func(chat, attr, body)

	CharsCY = "етуоранкхсвм".decode("utf-8")
	CharsLA = "etyopahkxcbm"

	eqMap = tuple([(CharsCY[numb], char) for numb, char in enumerate(CharsLA)])

	del CharsCY, CharsLA

	eqFuncs = {
		flags[0]: unicode.strip,
		flags[1]: unicode.lower,
		flags[2]: (lambda attr, map = eqMap: sub_desc(attr.lower(), map))
	}

	def prepare(self, attr, flags):
		if not flags:
			return attr
		attr = unicode(attr)
		for flag in flags:
			attr = self.eqFuncs[flag](attr)
		return attr

	def checkConds(self, chat, event, alias, conds, Vars):
		for attr, cond, clause, flags in conds:
			if cond == self.null:
				continue
			attr = Vars.get(attr)
			if not attr:
				return False
			if cond == "re":
				id = str.join(chr(47), (chat, event, alias))
				if id in self.Cache:
					clause = self.Cache[id]
				else:
					clause = self.Cache[id] = compile__(clause)
			else:
				attr = self.prepare(attr, flags)
			if not self.conds[cond](attr, clause):
				return False
		return True

	def extract(self, chat, event, alias, desc, Vars):
		conds, desc = desc
		if self.checkConds(chat.name, event, alias, conds, Vars):
			self.execute(chat, desc, Vars)

	def process(self, chat, event, Vars):
		iterator = self.ChatAliasDesc[chat][event].iteritems()
		chat = Chats[chat]
		for alias, desc in self.AliasDesc[event].iteritems():
			self.extract(chat, event, alias, desc, Vars)
		for alias, desc in iterator:
			self.extract(chat, event, alias, desc, Vars)

	def alias_01eh(self, stanza, isConf, stype, source, body, isToBs, disp):
		if not isConf:
			return None
		if isToBs and stype == sBase[1]:
			body = body.split(None, 1)
			if len(body) > 1:
				body = body[1]
			else:
				body = None
		if body:
			chat, nick = source[1:]
			user = Chats[chat].get_user(nick)
			if user:
				role, jid = "%s/%s" % user.role, user.source
			else:
				role, jid = None, None
			if body.startswith("/me") and len(body) > 3 and stype == sBase[0]:
				body = body[3:].lstrip()
				event = "/me"
			else:
				event = "message"
			self.process(chat, event, locals())

	def alias_09eh(self, chat, nick, subject, body, disp):
		if nick and nick != get_nick(chat):
			body = subject
			self.process(chat, "subject", locals())

	def alias_04eh(self, chat, nick, jid, role, stanza, disp):
		if (time.time() - Chats[chat].sdate) >= 30 and nick != get_nick(chat):
			if not jid:
				jid = None
			role = "%s/%s" % role
			caps = stanza.getTag("c", namespace = xmpp.NS_CAPS)
			if caps:
				caps_ver = caps.getAttr("ver")
				caps = caps.getAttr("node")
			else:
				caps_ver = None
			show = stanza.getShow()
			status = stanza.getStatus()
			iq = xmpp.Iq(sBase[10], to = "%s/%s" % (chat, nick))
			iq.addChild(sBase[18], namespace = xmpp.NS_VERSION)
			iq.setID("Bs-i%d" % Info["outiq"].plus())
			CallForResponse(disp, iq, self.alias_vhandler, {"chat": chat, "nick": nick, "jid": jid, "role": role})
			self.process(chat, "join", locals())

	def alias_vhandler(self, disp, stanza, chat, nick, jid, role):
		if chat in Chats and xmpp.isResultNode(stanza):
			os, name, version = None, None, None
			for node in stanza.getQueryChildren() or ():
				node_name = node.getName()
				if node_name == "name":
					name = node.getData()
				elif node_name == "version":
					version = node.getData()
				elif node_name == "os":
					os = node.getData()
			self.process(chat, "version", locals())

	def alias_05eh(self, chat, nick, reason, scode, disp):
		if nick != get_nick(chat):
			user = Chats[chat].get_user(nick)
			if user:
				role, jid = "%s/%s" % user.role, user.source
			else:
				role, jid = None, None
			if scode == sCodes[0]:
				event = "ban"
			elif scode == sCodes[2]:
				event = "kick"
			else:
				event = "leave"
			self.process(chat, event, locals())

	def alias_06eh(self, chat, old_nick, nick, disp):
		if nick != get_nick(chat):
			user = Chats[chat].get_user(nick)
			if user:
				role, jid = "%s/%s" % user.role, user.source
			else:
				role, jid = None, None
			self.process(chat, "nick", locals())

	def alias_07eh(self, chat, nick, role, disp):
		if nick != get_nick(chat):
			jid = get_source(chat, nick)
			role = "%s/%s" % role
			self.process(chat, "role", locals())

	def alias_08eh(self, chat, nick, stanza, disp):
		if nick != get_nick(chat):
			user = Chats[chat].get_user(nick)
			if user:
				role, jid = "%s/%s" % user.role, user.source
			else:
				role, jid = None, None
			show = stanza.getShow()
			status = stanza.getStatus()
			self.process(chat, "status", locals())

	compile_quote = compile__("<!--(.*?)-->", 16)

	attrsDesc = {
		"message": ("body", "jid", "nick", "role", "stype"),
		"/me": ("body", "jid", "nick", "role"),
		"subject": ("body", "nick"),
		"join": ("caps", "caps_ver", "jid", "nick", "role", "show", "status"),
		"version": ("jid", "name", "nick", "os", "role", "version"),
		"leave": ("jid", "nick", "role", "reason"),
		"ban": ("jid", "nick", "role", "reason"),
		"kick": ("jid", "nick", "role", "reason"),
		"nick": ("jid", "nick", "old_nick", "role"),
		"role": ("jid", "nick", "role"),
		"status": ("jid", "nick", "role", "show", "status")
	}

	validDesc = {
		"alias": ("\t", "\n", "\r", " ", "(chat)s", "(nick)s"),
		"macro": ("(aff)s", "(arg0)s", "(arg1)s", "(arg2)s", "(arg3)s", "(args)s", "(jid)s", "(role)s", "(stype)s"),
		"message": ("(body)s", "(jid)s", "(role)s"),
		"/me": ("(body)s", "(jid)s", "(role)s"),
		"subject": ("(body)s",),
		"join": ("(caps)s", "(caps_ver)s", "(jid)s", "(role)s", "(show)s", "(status)s"),
		"version": ("(jid)s", "(name)s", "(os)s", "(role)s", "(version)s"),
		"leave": ("(jid)s", "(role)s", "(reason)s"),
		"ban": ("(jid)s", "(role)s", "(reason)s"),
		"kick": ("(jid)s", "(role)s", "(reason)s"),
		"nick": ("(jid)s", "(old_nick)s", "(role)s"),
		"role": ("(jid)s", "(role)s"),
		"status": ("(jid)s", "(role)s", "(show)s", "(status)s")
	}

	def checkAttr(self, event, attr, cond):
		if cond == self.null:
			return True
		return (attr in self.attrsDesc[event])

	def checkParameters(self, body, event):
		if not body:
			return True
		attrs = (self.validDesc[self.alias] + self.validDesc[event])
		for numb, symbol in enumerate(body, 1):
			if symbol == "%":
				temp = body[numb:]
				if temp and not temp.startswith(attrs):
					return False
		return True

	def processFlags(self, flags, cond, ls = ("null", "len_more", "len_less", "re")):
		if cond in ls:
			flags = ()
		else:
			flags = [flag for flag in flags.split(chr(38)) if flag in self.flags]
			if all([(flag in flags) for flag in self.flags[-2:]]):
				flags.remove(self.flags[1])
			flags = tuple(set(flags))
		return flags

	def unpack(self, conditions):
		attrs = []
		conds = []
		clauses = []
		flags = []
		for attr, cond, clause, flags_ in conditions:
			attrs.append(attr)
			conds.append(cond)
			clauses.append("<!--%s-->" % clause)
			flags.append(str.join(chr(38), flags_) or self.null)
		attrs = str.join(chr(47), attrs)
		conds = str.join(chr(47), conds)
		clauses = "".join(clauses)
		flags = str.join(chr(47), flags)
		return attrs, conds, clauses, flags

	cmd_names = ()

	def get_names(self):
		if self.cmd_names:
			return self.cmd_names
		try:
			cmds = eval(get_file(os.path.join(self.path, "alias.name")).decode("utf-8")).values()
		except Exception:
			cmds = []
		cmds = set([cmd.decode("utf-8") for cmd in cmds] + [self.alias])
		self.cmd_names = cmds
		return cmds

	def save_alias(self, glob, chat):
		if glob:
			file = self.AliasFile
			data = str((self.On, self.AliasDesc))
		else:
			file = chat_file(chat, self.ChatAliasFile)
			data = str((self.Taboo[chat], self.ChatAliasDesc[chat]))
		cat_file(file, data)

	def command_alias(self, stype, source, body, disp):
		if body:
			ls = body.split(None, 1)
			glob = ((ls.pop(0)).lower() == "global")
		else:
			glob = False
		if glob or not self.ChatAliasDesc.has_key(source[1]):
			if enough_access(source[1], source[2], 7):
				desc = self.AliasDesc
				if not glob:
					glob = True
				elif ls:
					body = ls[0]
				else:
					body = ""
			else:
				body = ""
				answer = AnsBase[10]
		else:
			desc = self.ChatAliasDesc[source[1]]
		arg0 = body.lower()
		if arg0 == "help":
			if DefLANG in ("RU", "UA"):
				file = self.HelpFile % ("ru")
			else:
				file = self.HelpFile % ("en")
			answer = get_file(os.path.join(self.path, file)).decode("utf-8")
		elif arg0 == "state":
			answer = self.AnsBase[int(self.On)]
		elif arg0 == "enable":
			if enough_access(source[1], source[2], 8):
				if self.On:
					answer = self.AnsBase[2]
				else:
					self.On = True
					self.save_alias(True, source[1])
					for chat in Chats.keys():
						self.alias_01si(chat)
					Macro.__call__ = self.__call__
					Macro.__contains__ = self.__contains__
					for inst, ls in self.handlers:
						self.handler_register(getattr(self, inst.__name__), ls)
					answer = AnsBase[4]
			else:
				answer = AnsBase[10]
		elif arg0 == "disable":
			if enough_access(source[1], source[2], 8):
				if self.On:
					self.On = False
					self.save_alias(True, source[1])
					self.clear_handlers(); self.auto_clear()
					answer = AnsBase[4]
				else:
					answer = self.AnsBase[3]
			else:
				answer = AnsBase[10]
		elif arg0 == "bold":
			ls, cmds = [], []
			for event, aliases in desc.iteritems():
				if event == self.macro:
					for name, (command, body, access) in sorted(aliases.items()):
						cmds.append(str.join(chr(32), (name, command, body)).rstrip())
					continue
				for alias, (conditions, (atype, func, body)) in sorted(aliases.items()):
					attrs, conds, clauses, flags = self.unpack(conditions)
					ls.append(str.join(chr(32), (alias, event, attrs, conds, clauses, flags, atype, func, body)).rstrip())
			if ls:
				ls = "\->\n\n" + enumerated_list(ls)
			if cmds:
				cmds = "Macro:\n\n" + enumerated_list(cmds)
			if ls or cmds:
				answer = str.join(chr(10)*2, ((ls or ""), (cmds or "")))
			else:
				answer = self.AnsBase[4]
		elif body:
			body = body.split(None, 3)
			if len(body) >= 3:
				arg0 = (body.pop(0)).lower()
				alias = (body.pop(0)).lower()
				event = (body.pop(0)).lower()
				if len(alias) <= 16:
					if arg0 == "show":
						if event in self.Template:
							if alias in desc[event]:
								bold = (body and body[0].lower() == "bold")
								if event == self.macro:
									command, body, access = desc[self.macro][alias]
									if bold:
										answer = str.join(chr(32), (alias, command, body)).rstrip()
									else:
										answer = self.AnsBase[5] % (alias, access, command, body or self.null)
								else:
									conditions, (atype, func, body) = desc[event][alias]
									if bold:
										attrs, conds, clauses, flags = self.unpack(conditions)
										answer = str.join(chr(32), (alias, event, attrs, conds, clauses, flags, atype, func, body)).rstrip()
									else:
										answer = self.AnsBase[6] % (alias,
											event,
											enumerated_list("%s %s '%s'\n\tflags: %s" % (attr, cond, clause or self.null, ", ".join(flags) or self.null) for attr, cond, clause, flags in conditions),
											" -> ".join((atype, func, body or self.null)))
							else:
								answer = self.AnsBase[7]
						else:
							answer = AnsBase[2]
					elif arg0 == "add":
						if body:
							body = body[0]
							if event == self.macro:
								if alias not in Cmds:
									body = body.split(None, 1)
									command = (body.pop(0)).lower()
									if command in Cmds:
										if enough_access(source[1], source[2], (8 if command in self.get_names() else Cmds[command].access)):
											if glob or alias not in self.AliasDesc[self.macro]:
												if body:
													body = body[0]
												else:
													body = ""
												if 1536 >= len(body):
													if self.checkParameters(body, self.macro):
														access = get_access(source[1], source[2])
														if access < 8:
															cmds = [temp.name for temp in Cmds.itervalues() if temp.access > access]
														if access < 8 and any([temp in cmds or temp in self.get_names() for temp in (body.lower()).split()]):
															answer = self.AnsBase[27]
														else:
															desc[self.macro][alias] = (command, body, Cmds[command].access)
															self.save_alias(glob, source[1])
															answer = AnsBase[4]
													else:
														answer = self.AnsBase[8]
												else:
													answer = AnsBase[5]
											else:
												answer = self.AnsBase[9]
										else:
											answer = AnsBase[10]
									else:
										answer = AnsBase[6]
								else:
									answer = self.AnsBase[17] % (alias)
							elif event in self.Template:
								clauses = self.compile_quote.findall(body)
								if clauses:
									body = self.compile_quote.sub(chr(32), body)
									body = body.split(None, 5)
									alen = len(body)
									if alen >= 5:
										attrs, conds, flags, atype, func = (args.lower() for args in body[:5])
										if (atype == self.command and func in Cmds) or (atype == self.set and func in self.funcs) or (atype == self.message and func in ("chat", "private")):
											if (atype != self.command) or enough_access(source[1], source[2], (8 if func in self.get_names() else Cmds[func].access)):
												if alen == 6:
													body = body[-1]
												else:
													body = ""
												if 1024 >= len(body):
													if self.checkParameters(body, event):
														access = get_access(source[1], source[2])
														if atype == self.command and access < 8:
															cmds = [temp.name for temp in Cmds.itervalues() if temp.access > access]
														else:
															cmds = None
														if cmds and any([temp in cmds or temp in self.get_names() for temp in (body.lower()).split()]):
															answer = self.AnsBase[27]
														else:
															conds = [cond for cond in conds.split(chr(47)) if cond in self.conds]
															if ("re" not in conds) or enough_access(source[1], source[2], 8):
																if len(conds) <= 8:
																	attrs = attrs.split(chr(47))
																	flags = flags.split(chr(47))
																	if len(attrs) == len(conds) == len(clauses) == len(flags):
																		attrs = [self.null if conds[numb] == self.null else attr for numb, attr in enumerate(attrs) if self.checkAttr(event, attr, conds[numb])]
																		clauses = [int(clause) if conds[numb].startswith("len") else clause for numb, clause in enumerate(clauses) \
																							if not conds[numb].startswith("len") or (isNumber(clause) and 3 < int(clause) < 10241)]
																		if len(attrs) == len(conds) == len(clauses):
																			limit = (192 if enough_access(source[1], source[2], 8) else 64)
																			if all([(isinstance(clause, int) or (len(clause) <= 64)) for clause in clauses]):
																				if conds[len(conds) - 1] == self.null or all(clauses):
																					for numb, clause in enumerate(clauses):
																						if conds[numb] == "re":
																							try:
																								compile__(clause)
																							except Exception:
																								answer = self.AnsBase[10]
																								break
																					else:
																						flags = [self.processFlags(flags, conds[numb]) for numb, flags in enumerate(flags)]
																						clauses = ["" if conds[numb] == self.null else self.prepare(clause, flags[numb]) for numb, clause in enumerate(clauses)]
																						conds = zip(attrs, conds, clauses, flags)
																						desc[event][alias] = (conds, (atype, func, body))
																						self.save_alias(glob, source[1])
																						answer = self.AnsBase[6] % (alias,
																							event,
																							enumerated_list("%s %s '%s'\n\tflags: %s" % (attr, cond, clause or self.null, ", ".join(flags) or self.null) for attr, cond, clause, flags in conds),
																							" -> ".join((atype, func, body or self.null)))
																				else:
																					answer = self.AnsBase[11]
																			else:
																				answer = self.AnsBase[12] % (limit)
																		else:
																			answer = self.AnsBase[13]
																	else:
																		answer = self.AnsBase[14]
																else:
																	answer = self.AnsBase[15]
															else:
																answer = self.AnsBase[16]
													else:
														answer = self.AnsBase[8]
												else:
													answer = AnsBase[5]
											else:
												answer = AnsBase[10]
										elif atype == self.command:
											answer = AnsBase[6]
										elif atype == self.set:
											answer = self.AnsBase[18]
										else:
											answer = self.AnsBase[19]
									else:
										answer = AnsBase[2]
								else:
									answer = self.AnsBase[20]
							else:
								answer = AnsBase[2]
						else:
							answer = AnsBase[2]
					elif arg0 == "access":
						if isNumber(event):
							access = int(event)
							user_access = get_access(source[1], source[2])
							if 0 < access < (user_access + 1):
								if alias in desc[self.macro]:
									(command, body, temp) = desc[self.macro][alias]
									if enough_access(source[1], source[2], temp):
										desc[self.macro][alias] = (command, body, access)
										self.save_alias(glob, source[1])
										answer = AnsBase[4]
									else:
										answer = AnsBase[10]
								else:
									answer = self.AnsBase[7]
							else:
								answer = self.AnsBase[21] % (user_access)
						else:
							answer = AnsBase[30]
					elif arg0 == "help":
						if glob:
							base = (self.MacroHelpBase)
						else:
							base = cefile(chat_file(source[1], self.ChatMacroHelpBase))
						with database(base) as db:
							db("select * from macro where name=?", (alias,))
							help = db.fetchone()
							if event == "clear":
								if help:
									db("delete from macro where name=?", (alias,))
									db.commit()
									answer = AnsBase[4]
								else:
									answer = self.AnsBase[23]
							elif body:
								if alias in desc[self.macro]:
									body = body[0]
									if help:
										db("update macro set help=? where name=?", (body, alias))
									else:
										db("insert into macro values (?,?)", (alias, body))
									db.commit()
									answer = AnsBase[4]
								else:
									answer = self.AnsBase[7]
							else:
								answer = AnsBase[2]
					elif arg0 == "del":
						if event in self.Template:
							if alias in desc[event]:
								del desc[event][alias]
								self.save_alias(glob, source[1])
								if event == self.macro:
									if glob:
										base = (self.MacroHelpBase)
									else:
										base = cefile(chat_file(source[1], self.ChatMacroHelpBase))
									with database(base) as db:
										db("select * from macro where name=?", (alias,))
										help = db.fetchone()
										if help:
											db("delete from macro where name=?", (alias,))
											db.commit()
								answer = AnsBase[4]
							else:
								answer = self.AnsBase[7]
						else:
							answer = AnsBase[2]
					else:
						answer = AnsBase[2]
				else:
					answer = self.AnsBase[22]
			else:
				answer = AnsBase[2]
		elif not locals().has_key(sBase[6]):
			ls, cmds = [], []
			for event, aliases in desc.iteritems():
				if event == self.macro:
					for name, (command, body, access) in sorted(aliases.items()):
						cmds.append(self.AnsBase[5] % (name, access, command, body or self.null))
					continue
				for alias, (conds, (atype, func, body)) in sorted(aliases.items()):
					ls.append(self.AnsBase[6] % (alias,
						event,
						enumerated_list("%s %s '%s'\n\tflags: %s" % (attr, cond, clause or self.null, ", ".join(flags) or self.null) for attr, cond, clause, flags in conds),
						" -> ".join((atype, func, body or self.null))))
			if ls:
				ls = "\->\n\n" + str.join(chr(10)*2, ("#{0:02} - {1}".format(numb, line) for numb, line in enumerate(ls, 1)))
			if cmds:
				cmds = "Macro:\n\n" + enumerated_list(cmds)
			if ls or cmds:
				answer = str.join(chr(10)*2, ((ls or ""), (cmds or "")))
			else:
				answer = self.AnsBase[4]
		Answer(answer, stype, source, disp)

	def command_macro(self, stype, source, body, disp):
		if body:
			ls = body.split()
			arg0 = (ls.pop(0)).lower()
			if arg0 in ("taboo", "табу".decode("utf-8")):
				if Chats.has_key(source[1]):
					oCmds = self.Taboo[source[1]]
					if ls:
						if enough_access(source[1], source[2], 6):
							command = (ls.pop(0)).lower()
							desc = self.AliasDesc[self.macro].get(command) or self.ChatAliasDesc[source[1]][self.macro].get(command)
							if desc:
								if enough_access(source[1], source[2], desc[2]):
									if command in oCmds:
										oCmds.remove(command)
										answer = self.AnsBase[28] % (command)
									else:
										oCmds.append(command)
										answer = self.AnsBase[29] % (command)
									self.save_alias(False, source[1])
								else:
									answer = AnsBase[10]
							elif command in oCmds:
								oCmds.remove(command)
								answer = AnsBase[4]
								self.save_alias(False, source[1])
							else:
								answer = self.AnsBase[7]
						else:
							answer = AnsBase[10]
					elif oCmds:
						answer = ", ".join(oCmds)
					else:
						answer = self.AnsBase[30]
				else:
					answer = AnsBase[0]
			elif ls and arg0 in ("help", "хелп".decode("utf-8")):
				command = (ls.pop(0)).lower()
				desc = self.AliasDesc[self.macro].get(command)
				if desc:
					base = (self.MacroHelpBase)
					cmd, args, access = desc
				elif self.ChatAliasDesc.has_key(source[1]):
					desc = self.ChatAliasDesc[source[1]][self.macro].get(command)
					if desc:
						base = cefile(chat_file(source[1], self.ChatMacroHelpBase))
						cmd, args, access = desc
				if desc:
					with database(base) as db:
						db("select help from macro where name=?", (command,))
						help = db.fetchone()
					if help:
						answer = self.AnsBase[25] % (help[0], access)
					else:
						answer = self.AnsBase[26]
				else:
					answer = self.AnsBase[7]
			else:
				answer = AnsBase[2]
		elif self.On:
			desc = {}
			for name, (command, body, access) in sorted(self.AliasDesc[self.macro].items()):
				if access not in desc:
					desc[access] = []
				desc[access].append(name)
			if self.ChatAliasDesc.has_key(source[1]):
				for name, (command, body, access) in sorted(self.ChatAliasDesc[source[1]][self.macro].items()):
					if access not in desc:
						desc[access] = []
					desc[access].append(name)
			if desc:
				ls = [self.AnsBase[24]]
				for access, cmds in sorted(desc.items(), reverse = True):
					ls.append("# Access %d (total - %d):\n%s" % (access, len(cmds), ", ".join(sorted(cmds))))
				answer = str.join(chr(10)*2, ls)
			else:
				answer = self.AnsBase[4]
		else:
			answer = self.AnsBase[0]
		Answer(answer, stype, source, disp)

	def alias_00si(self):
		if initialize_file(self.AliasFile, str((True, self.Template))):
			self.On, self.AliasDesc = eval(get_file(self.AliasFile))
			if self.On:
				Macro.__call__ = self.__call__
				Macro.__contains__ = self.__contains__
			else:
				self.clear_handlers()
		if not os.path.isfile(self.MacroHelpBase):
			with database(self.MacroHelpBase) as db:
				db("create table macro (name text, help text)")
				db.commit()

	def alias_01si(self, chat):
		file = chat_file(chat, self.ChatAliasFile)
		if initialize_file(file, str(([], self.Template))):
			oCmds, desc = eval(get_file(file))
		else:
			oCmds, desc = [], Template.copy()
		self.ChatAliasDesc[chat] = desc
		self.Taboo[chat] = oCmds
		filename = cefile(chat_file(chat, self.ChatMacroHelpBase))
		if not os.path.isfile(filename):
			with database(filename) as db:
				db("create table macro (name text, help text)")
				db.commit()

	def alias_04si(self, chat):
		del self.ChatAliasDesc[chat]
		del self.Taboo[chat]

	def auto_clear(self):
		Macro.__call__, Macro.__contains__ = lambda *args: None, lambda args: False

	commands = (
		(command_alias, alias, 6,),
		(command_macro, macro, 1,)
	)

	handlers = (
		(alias_00si, "00si"),
		(alias_01si, "01si"),
		(alias_04si, "04si"),
		(alias_01eh, "01eh"),
		(alias_09eh, "09eh"),
		(alias_04eh, "04eh"),
		(alias_05eh, "05eh"),
		(alias_06eh, "06eh"),
		(alias_07eh, "07eh"),
		(alias_08eh, "08eh")
	)
