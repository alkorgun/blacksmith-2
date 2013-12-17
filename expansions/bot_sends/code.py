# coding: utf-8

#  BlackSmith mark.2
# exp_name = "bot_sends" # /code.py v.x10
#  Id: 18~9c
#  Code © (2010-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_clear(self, stype, source, body, disp):
		conf = source[1]
		if conf in Chats:
			if ChatsAttrs[conf]["dirt"]:
				ChatsAttrs[conf]["dirt"] = None
				if stype == sBase[1]:
					s1_backup = Chats[conf].state
					s2_backup = Chats[conf].status
					Chats[conf].change_status(sList[2], self.AnsBase[0])
				zero = xmpp.Message(conf, typ = sBase[1])
				zero.setBody("")
				for Numb in xrange(24):
					if conf not in Chats:
						raise SelfExc("exit")
					Sender(disp, zero); Info["omsg"].plus()
					if (Numb != 23):
						sleep(1.4)
				if stype == sBase[1]:
					Chats[conf].change_status(s1_backup, s2_backup)
				ChatsAttrs[conf]["dirt"] = True
			else:
				answer = self.AnsBase[9]
		else:
			answer = AnsBase[0]
		if locals().has_key(sBase[6]):
			Answer(answer, stype, source, disp)

	def command_test(self, stype, source, body, disp):
		errors = len(VarCache["errors"])
		if not errors:
			answer = self.AnsBase[1]
		elif errors < (len(Clients.keys())*3):
			answer = self.AnsBase[2] % (get_nick(source[1]), errors)
		else:
			answer = self.AnsBase[3] % (errors)
		Answer(answer, stype, source, disp)

	def command_sendall(self, stype, source, body, disp):
		if body:
			for conf in Chats.keys():
				Message(conf, self.AnsBase[5] % (source[2], body))
			answer = AnsBase[4]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_more(self, stype, source, body, disp):
		Chat = Chats.get(source[1])
		if not Chat:
			return Answer(AnsBase[0], stype, source, disp)
		if Chat.more:
			body = "[&&] %s" % (Chat.more)
			Chat.more = ""
			Message(Chat.name, body, disp)

	compile_chat = compile__("^[^\s'\"@<>&]+?@(?:conference|muc|conf|chat|group)\.[\w-]+?\.[\.\w-]+?$")

	def command_send(self, stype, source, body, disp):
		if body:
			body = body.split(None, 1)
			if len(body) == 2:
				sTo, body = body
				if isSource(sTo):
					conf = (sTo.split(chr(47)))[0].lower()
					if conf in Chats or not self.compile_chat.match(conf):
						Message(sTo, self.AnsBase[5] % (source[2], body))
						answer = AnsBase[4]
					else:
						answer = AnsBase[8]
				else:
					answer = self.AnsBase[4]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_toadmin(self, stype, source, body, disp):
		if body:
			if PrivLimit >= len(body):
				instance = get_source(source[1], source[2])
				delivery(self.AnsBase[5] % ((source[2] if not instance else "%s (%s)" % (source[2], instance)), body))
				answer = AnsBase[4]
			else:
				answer = AnsBase[5]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_echo(self, stype, source, body, disp):
		if not body:
			return Answer(AnsBase[1], stype, source, disp)
		if ConfLimit >= len(body):
			Message(source[1], body, disp)
		else:
			Message(source[1], body[:ConfLimit], disp)

	def command_invite(self, stype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				Time, admin = time.time(), enough_access(source[1], source[2], 7)
				timer = (720 if admin else (Time - ChatsAttrs[source[1]]["intr"]))
				if timer >= 720:
					source_, arg0 = None, body.split()[0]
					if Chats[source[1]].isHere(body):
						if Chats[source[1]].isHereTS(body):
							return Answer(self.AnsBase[6] % (body), stype, source, disp)
						source_ = get_source(source[1], body)
					elif isSource(arg0):
						source_ = arg0.lower()
					if source_:
						if not admin:
							ChatsAttrs[source[1]]["intr"] = Time
						invite = xmpp.Message(to = source[1])
						node = xmpp.Node("x")
						node.setNamespace(xmpp.NS_MUC_USER)
						x_child = node.addChild("invite", {"to": source_})
						x_child.setTagData("reason", source[2])
						invite.addChild(node = node)
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
		Answer(answer, stype, source, disp)

	def init_bot_sender(self, chat):
		desc = ChatsAttrs.setdefault(chat, {})
		desc["intr"] = 0
		desc["dirt"] = True

	commands = (
		(command_clear, "clear", 3,),
		(command_test, "test", 1, False),
		(command_sendall, "sendall", 8,),
		(command_more, "more", 1,),
		(command_send, "send", 8,),
		(command_toadmin, "toadmin", 1,),
		(command_echo, "echo", 6,),
		(command_invite, "invite", 4,)
	)

	handlers = ((init_bot_sender, "01si"),)
