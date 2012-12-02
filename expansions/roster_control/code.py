# coding: utf-8

#  BlackSmith mark.2
# exp_name = "roster_control" # /code.py v.x3
#  Id: 23~3c
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	RosterFile = dynamic % ("roster.db")

	def command_roster(self, stype, source, body, disp):
		cls = sorted(Clients.keys())
		if body:
			ls = body.split()
			body = (ls.pop(0)).lower()
			if body in cls:
				Name = body
			elif isNumber(body):
				Number = (int(clnt) - 1)
				if Number >= 0 and Number <= len(cls):
					Name = cls[Number]
				else:
					Name = None
			else:
				Name = None
			if Name:
				if ls:
					body = ls.pop(0)
					if ls:
						jid = (ls.pop(0)).lower()
						if jid.count("."):
							if body == "+":
								Clients[Name].Roster.Authorize(jid)
								Clients[Name].Roster.Subscribe(jid)
								if ls:
									Tabe = ("admin", "админ".decode("utf-8"))
									Nick = ls.pop(0)
									if ls and Tabe.count(ls[0].lower()):
										Clients[Name].Roster.setItem(jid, Nick, ["Admins"])
									else:
										Clients[Name].Roster.setItem(jid, Nick, ["Users"])
								else:
									Clients[Name].Roster.setItem(jid, (jid.split("@"))[0], ["Users"])
								answer = AnsBase[4]
							elif body == "-":
								if jid in Clients[Name].Roster.keys():
									Clients[Name].Roster.Unauthorize(jid)
									Clients[Name].Roster.Unsubscribe(jid)
									Clients[Name].Roster.delItem(jid)
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
					Rdsp = getattr(Clients[Name], "Roster")
					if Rdsp:
						jids = Rdsp.keys()
						for jid in jids:
							if jid.count("@conference."):
								jids.remove(jid)
					if Rdsp and jids:
						Groups = {None: []}
						for jid in jids:
							Name = Rdsp.getName(jid)
							Grps = Rdsp.getGroups(jid)
							if Grps:
								Gp = sorted(Grps)[0]
								if not Groups.has_key(Gp):
									Groups[Gp] = []
							else:
								Gp = None
							Groups[Gp].append((jid, Name))
						ls = ["[Group] [#] [JID] (Nick)"]
						Gp = Groups.pop(None)
						for Gp, Items in (sorted(Groups.items()) + [("No Group", Gp)]):
							if Items:
								Numb = itypes.Number()
								ls.append(Gp + ":")
								for jid, Name in sorted(Items):
									if jid in (Name, None):
										ls.append("\t%d) %s" % (Numb.plus(), jid))
									else:
										ls.append("\t%d) %s - %s" % (Numb.plus(), jid, Name))
						answer = str.join(chr(10), ls)
					else:
						answer = self.AnsBase[1]
			else:
				answer = self.AnsBase[2]
		else:
			answer = enumerated_list(cls)
		Answer(answer, stype, source, disp)

	def command_roster_state(self, stype, source, body, disp):
		if body:
			body = (body.split())[0].lower()
			if body in ("on", "1", "вкл".decode("utf-8")):
				if not Roster["on"]:
					Roster["on"] = True
					cat_file(self.RosterFile, str(True))
					answer = AnsBase[4]
				else:
					answer = self.AnsBase[3]
			elif body in ("off", "0", "выкл".decode("utf-8")):
				if Roster["on"]:
					Roster["on"] = False
					cat_file(self.RosterFile, str(False))
					answer = AnsBase[4]
				else:
					answer = self.AnsBase[4]
			else:
				answer = AnsBase[2]
		else:
			answer = (self.AnsBase[3] if Roster["on"] else self.AnsBase[4])
		Answer(answer, stype, source, disp)

	def init_roster_state(self):
		if initialize_file(self.RosterFile, str(True)):
			Roster["on"] = eval(get_file(self.RosterFile))

	commands = (
		(command_roster, "roster", 7,),
		(command_roster_state, "roster2", 7,)
					)

	handlers = ((init_roster_state, "00si"),)
