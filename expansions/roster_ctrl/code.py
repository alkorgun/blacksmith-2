# coding: utf-8

#  BlackSmith mark.2
exp_name = "roster_ctrl" # /code.py v.x2
#  Id: 23~2b
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	RosterFile = dynamic % ("roster.db")

	def command_roster(self, ltype, source, body, disp):
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
									answer = self.AnsBase[0]
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
						answer = self.AnsBase[1]
			else:
				answer = self.AnsBase[2]
		else:
			answer = enumerated_list(cls)
		Answer(answer, ltype, source, disp)

	def init_roster_state(self):
		if initialize_file(self.RosterFile, str(True)):
			Roster["on"] = eval(get_file(self.RosterFile))

	commands = (
		(command_roster, "roster", 7,),
#		(command_roster_state, "roster2", 7,)
					)

#	handlers = ((init_roster_state, "00si"),)
