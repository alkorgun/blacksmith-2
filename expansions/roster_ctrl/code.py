# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "roster_ctrl" # /code.py v.x1
#  Id: 24~1a
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
		elif check_number(x):
			number = (int(x) - 1)
			if number >= 0 and number <= len(cls):
				cl_name = cls[number]
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
								Nick = list.pop(0)
								if list and ["admin", "админ".decode("utf-8")].count((list.pop(0)).lower()):
									Clients[cl_name].Roster.setItem(jid, Nick, ["Admins"])
								else:
									Clients[cl_name].Roster.setItem(jid, Nick, ["Users"])
							else:
								Clients[cl_name].Roster.setItem(jid, (jid.split("@"))[0], ["Users"])
							answer = AnsBase[4]
						elif body == "-":
							if jid in Clients[cl_name].Roster.keys():
								Clients[cl_name].Roster.Unsubscribe(jid)
								Clients[cl_name].Roster.delItem(jid)
								answer = AnsBase[4]
							else:
								answer = roster_answers[0]
						else:
							answer = AnsBase[2]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				jids = Clients[cl_name].Roster.keys()
				if jids:
					for x in jids:
						if x.count("@conference."):
							jids.remove(x)
					answer = enumerated_list(sorted(jids))
				else:
					answer = roster_answers[1]
		else:
			answer = roster_answers[2]
	else:
		answer = enumerated_list(cls)
	Answer(answer, ltype, source, disp)

def init_roster_state():
	if initialize_file(RosterFile, str(True)):
		Roster["on"] = eval(get_file(RosterFile))

expansions[exp_name].funcs_add([command_roster, init_roster_state])
expansions[exp_name].ls.extend(["roster_answers", "RosterFile"])

command_handler(command_roster, {"RU": "ростер", "EN": "roster"}, 7, exp_name)
#command_handler(command_roster_state, {"RU": "ростер*", "EN": "roster*"}, 7, exp_name)

#handler_register(init_roster_state, "00si", exp_name)
