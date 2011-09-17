# coding: utf-8

#  BlackSmith mark.2
exp_name = "roster_ctrl" # /code.py v.x1
#  Id: 23~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

RosterFile = dynamic % ("roster.db")

def command_roster(ltype, source, body, disp):
	cls = sorted(Clients.keys())
	if body:
		list = body.split()
		x = (list.pop(0)).lower()
		if x in cls:
			cl_name = x
		elif isNumber(x):
			Number = (int(x) - 1)
			if Number >= 0 and Number <= len(cls):
				cl_name = cls[Number]
			else:
				cl_name = False
		else:
			cl_name = False
		if cl_name:
			if list:
				body = list.pop(0)
				if list:
					jid = (list.pop(0)).lower()
					if jid.count("."):
						if body == "+":
							Clients[cl_name].Roster.Authorize(jid)
							Clients[cl_name].Roster.Subscribe(jid)
							if list:
								Tabe = ("admin", "админ".decode("utf-8"))
								Nick = list.pop(0)
								if list and Tabe.count(list[0].lower()):
									Clients[cl_name].Roster.setItem(jid, Nick, ["Admins"])
								else:
									Clients[cl_name].Roster.setItem(jid, Nick, ["Users"])
							else:
								Clients[cl_name].Roster.setItem(jid, (jid.split("@"))[0], ["Users"])
							answer = AnsBase[4]
						elif body == "-":
							if jid in Clients[cl_name].Roster.keys():
								Clients[cl_name].Roster.Unauthorize(jid)
								Clients[cl_name].Roster.Unsubscribe(jid)
								Clients[cl_name].Roster.delItem(jid)
								answer = AnsBase[4]
							else:
								answer = RosterAnsBase[0]
						else:
							answer = AnsBase[2]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				Rdsp = getattr(Clients[cl_name], "Roster")
				if Rdsp:
					jids = Rdsp.keys()
					for jx in jids:
						if jx.count("@conference."):
							jids.remove(jx)
				if Rdsp and jids:
#					Numb = itypes.Number()
#					answer = "[#] [JID] [Nick] (Group)"
#					Gpoups = []
#					for jx in jids:
#						Name = Rdsp.getName(jx)
#						Grps = Rdsp.getGroups(jx)
#						if Grps:
#							
#						else:
#							
#						if Groups:
#							answer += "\n%d) %s - %s (%s)" % (Numb.plus(), Name, Groups[0])
#						else:
#							answer += "\n%d) %s - %s" % (Numb.plus(), Name)
					answer = enumerated_list(sorted(jids))
				else:
					answer = RosterAnsBase[1]
		else:
			answer = RosterAnsBase[2]
	else:
		answer = enumerated_list(cls)
	Answer(answer, ltype, source, disp)

def init_roster_state():
	if initialize_file(RosterFile, str(True)):
		Roster["on"] = eval(get_file(RosterFile))

expansions[exp_name].funcs_add([command_roster, init_roster_state])
expansions[exp_name].ls.extend(["RosterAnsBase", "RosterFile"])

command_handler(command_roster, {"RU": "ростер", "EN": "roster"}, 7, exp_name)
#command_handler(command_roster_state, {"RU": "ростер*", "EN": "roster2"}, 7, exp_name)

#handler_register(init_roster_state, "00si", exp_name)
