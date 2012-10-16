# coding: utf-8

#  BlackSmith mark.2
exp_name = "alive_keeper" # /code.py v.x4
#  Id: 16~4b
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def alive_keeper(self):

		def alive_keeper_answer(disp, stanza):
			if stanza:
				Clients[get_disp(disp)].aKeeper = itypes.Number()

		while VarCache["alive"]:
			time.sleep(360)
			ThrIds = iThr.ThrNames()
			for disp in Clients.keys():
				if not hasattr(Clients[disp], "aKeeper"):
					Clients[disp].aKeeper = itypes.Number()
				if Clients[disp].aKeeper._int() >= 3:
					Clients[disp].aKeeper = itypes.Number()
					ThrName = "%s%s" % (Types[13], disp)
					if ThrName in ThrIds:
						for Thr in iThr.enumerate():
							if Thr._Thread__name == ThrName:
								Thr.kill()
					try:
						composeThr(connectAndDispatch, ThrName, (disp,)).start()
					except:
						delivery(AnsBase[28] % (disp))
				elif expansions.has_key(self.name):
					Clients[disp].aKeeper.plus()
					iq = xmpp.Iq(to = "%s/%s" % (disp, GenResource), typ = Types[10])
					iq.addChild(Types[16], {}, [], xmpp.NS_PING)
					iq.setID("Bs-i%d" % Info["outiq"].plus())
					CallForResponse(disp, iq, alive_keeper_answer)
					del iq
				else:
					raise iThr.ThrKill("exit")
			del ThrIds

	def conf_alive_keeper(self):

		def conf_alive_keeper_answer(disp, stanza, conf):
			if Chats.has_key(conf):
				if xmpp.isErrorNode(stanza):
					if eCodes[6] == stanza.getErrorCode():
						Chats[conf].aKeeper = itypes.Number()
				else:
					Chats[conf].aKeeper = itypes.Number()

		while VarCache["alive"]:
			time.sleep(360)
			ThrIds = iThr.ThrNames()
			for conf in Chats.keys():
				if not (online(Chats[conf].disp) and Chats[conf].IamHere):
					continue
				if not hasattr(Chats[conf], "aKeeper"):
					Chats[conf].aKeeper = itypes.Number()
				if Chats[conf].aKeeper._int() >= 3:
					Chats[conf].aKeeper = itypes.Number()
					TimerName = ejoinTimerName(conf)
					if TimerName not in ThrIds:
						try:
							composeTimer(180, ejoinTimer, TimerName, (conf,)).start()
						except:
							pass
				elif expansions.has_key(self.name):
					Chats[conf].aKeeper.plus()
					iq = xmpp.Iq(to = "%s/%s" % (conf, get_self_nick(conf)), typ = Types[10])
					iq.addChild(Types[18], {}, [], xmpp.NS_PING)
					iq.setID("Bs-i%d" % Info["outiq"].plus())
					CallForResponse(Chats[conf].disp, iq, conf_alive_keeper_answer, {"conf": conf})
					del iq
				else:
					raise iThr.ThrKill("exit")
			del ThrIds

	def start_keepers(self):
		Name1 = self.alive_keeper.func_name
		Name2 = self.conf_alive_keeper.func_name
		for Thr in iThr.enumerate():
			ThrName = Thr._Thread__name
			if ThrName.startswith((Name1, Name2)):
				Thr.kill()
		composeThr(self.alive_keeper, Name1).start()
		composeThr(self.conf_alive_keeper, Name2).start()

	handlers = ((start_keepers, "02si"),)
