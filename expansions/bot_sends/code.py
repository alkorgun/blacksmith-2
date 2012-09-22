# coding: utf-8

#  BlackSmith mark.2
exp_name = "bot_sends" # /code.py v.x6
#  Id: 18~5b
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_clear(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if ChatsAttrs[source[1]]["dirt"]:
				ChatsAttrs[source[1]]["dirt"] = None
				if ltype == Types[1]:
					s1_buckup = Chats[source[1]].state
					s2_buckup = Chats[source[1]].status
					Chats[source[1]].change_status(sList[2], self.AnsBase[0])
				zero = xmpp.Message(to = source[1], typ = Types[1])
				for Numb in xrange(24):
					if not Chats.has_key(source[1]):
						raise SelfExc("exit")
					Sender(disp, zero); Info["omsg"].plus()
					if (Numb != 23):
						time.sleep(1.4)
				if ltype == Types[1]:
					Chats[source[1]].change_status(s1_buckup, s2_buckup)
				ChatsAttrs[source[1]]["dirt"] = True
			else:
				answer = self.AnsBase[9]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_test(self, ltype, source, body, disp):
		errors = len(VarCache["errors"])
		if not errors:
			answer = self.AnsBase[1]
		elif errors < (len(Clients.keys())*3):
			answer = self.AnsBase[2] % (get_self_nick(source[1]), errors)
		else:
			answer = self.AnsBase[3] % (errors)
		Answer(answer, ltype, source, disp)

	def command_sendall(self, ltype, source, body, disp):
		if body:
			for conf in Chats.keys():
				Msend(conf, self.AnsBase[5] % (source[2], body))
			answer = AnsBase[4]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_more(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if Chats[source[1]].more:
				body = "[&&] %s" % (Chats[source[1]].more)
				Chats[source[1]].more = ""
				Msend(source[1], body, disp)
		else:
			Answer(AnsBase[0], ltype, source, disp)

	def command_send(self, ltype, source, body, disp):
		if body:
			list = body.split()
			if len(list) >= 2:
				sTo = list[0]
				if isSource(sTo):
					conf = (sTo.split(chr(47)))[0].lower()
					if Chats.has_key(conf) or not conf.count("@conf"):
						Msend(sTo, self.AnsBase[5] % (source[2], body[(body.find(sTo) + (len(sTo) + 1)):].strip()))
						answer = AnsBase[4]
					else:
						answer = AnsBase[8]
				else:
					answer = self.AnsBase[4]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_adelivery(self, ltype, source, body, disp):
		if body:
			if PrivLimit >= len(body):
				instance = get_source(source[1], source[2])
				delivery(self.AnsBase[5] % ((source[2] if not instance else "%s (%s)" % (source[2], instance)), body))
				answer = AnsBase[4]
			else:
				answer = AnsBase[5]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_say(self, ltype, source, body, disp):
		if body:
			if ConfLimit >= len(body):
				Msend(source[1], body, disp)
			else:
				Msend(source[1], body[:ConfLimit], disp)
		else:
			Answer(AnsBase[1], ltype, source, disp)

	def command_invite(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				timer = (726 if enough_access(source[1], source[2], 7) else (time.time() - ChatsAttrs[source[1]]["intr"]))
				if timer >= 720:
					source_, jid_ = None, (body.split()[0])
					if Chats[source[1]].isHere(body):
						if Chats[source[1]].isHereTS(body):
							Answer(self.AnsBase[6] % (body), ltype, source, disp)
							raise iThr.ThrKill("exit")
						source_ = get_source(source[1], body)
					elif isSource(jid_):
						source_ = jid_.lower()
					if source_:
						ChatsAttrs[source[1]]["intr"] = time.time()
						invite = xmpp.Message(to = source[1])
						x = xmpp.Node("x")
						x.setNamespace(xmpp.NS_MUC_USER)
						x_child = x.addChild("invite", {"to": source_})
						x_child.setTagData("reason", source[2])
						invite.addChild(node = x)
						Info["omsg"].plus()
						Sender(disp, invite)
						answer = AnsBase[4]
					else:
						answer = self.AnsBase[7]
				else:
					answer = self.AnsBase[8] % Time2Text(720 - timer)
			else:
				answer = AnsBase[1]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	def init_bot_sender(self, conf):
		if not ChatsAttrs.has_key(conf):
			ChatsAttrs[conf] = {}
		ChatsAttrs[conf]["intr"] = 0
		ChatsAttrs[conf]["dirt"] = True

	commands = (
		(command_clear, "clear", 3,),
		(command_test, "test", 1, False),
		(command_sendall, "sendall", 8,),
		(command_more, "more", 1,),
		(command_send, "send", 8,),
		(command_adelivery, "toadmin", 1,),
		(command_say, "say", 7,),
		(command_invite, "invite", 4,)
					)

	handlers = ((init_bot_sender, "01si"),)
