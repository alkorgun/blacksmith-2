# coding: utf-8

#  BlackSmith mark.2
# exp_name = "search" # /code.py v.x2
#  Id: 33~2c
#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	busy = False
	date = 0

	CharsCY = "етуоранкхсвм".decode("utf-8")
	CharsLA = "etyopahkxcbm"

	eqMap = tuple([(CharsCY[numb], char) for numb, char in enumerate(CharsLA)])

	del CharsCY, CharsLA

	XEPs.add(xmpp.NS_DISCO_ITEMS)

	def command_disco_search(self, stype, source, body, disp):
		if body:
			body = body.lower()
			body = body.split(None, 1)
			if len(body) == 2:
				if not self.busy:
					self.busy = True
					self.date = time.time()
					Answer(self.AnsBase[0], stype, source, disp)
					server, body = body
					chats = itypes.Number()
					count = []
					iq = xmpp.Iq(sBase[10], to = server)
					iq.addChild(sBase[18], namespace = xmpp.NS_DISCO_ITEMS)
					iq.setID("Bs-i%d" % Info["outiq"].plus())
					CallForResponse(disp, iq, self.answer_disco_search_start, {"chats": chats, "count": count, "stype": stype, "source": source, "body": sub_desc(body, self.eqMap)})
					for x in xrange(400):
						sleep(0.2)
						if not self.busy:
							answer = self.AnsBase[1] % server
							break
					else:
						self.busy = False
						if count:
							Message(source[0], self.AnsBase[2] % (chats._str(), len(count), enumerated_list(sorted(count)[:96])), disp)
						else:
							answer = self.AnsBase[3] % chats._str()
				else:
					answer = self.AnsBase[4] % Time2Text(80 - (time.time() - self.date))
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		if locals().has_key(sBase[6]):
			Answer(answer, stype, source, disp)

	def answer_disco_search_start(self, disp, stanza, chats, count, stype, source, body):
		if xmpp.isResultNode(stanza):
			cls = [dr for dr in Clients.values() if dr.isConnected()] or [disp]
			cllen = len(cls)
			control = lambda numb: (numb if numb < cllen else 0)
			iters = 0
			for node in stanza.getQueryChildren() or ():
				if not self.busy:
					break
				if node and node != "None":
					chat = node.getAttr("jid")
					if chat:
						iq = xmpp.Iq(sBase[10], to = chat)
						iq.addChild(sBase[18], namespace = xmpp.NS_DISCO_ITEMS)
						iq.setID("Bs-i%d" % Info["outiq"].plus())
						iters = control(iters + 1)
						CallForResponse(cls[iters], iq, self.answer_disco_search, {"chats": chats, "count": count, "chat": chat, "body": body})
						sleep(0.12)
		else:
			self.busy = False

	def answer_disco_search(self, disp, stanza, chats, count, chat, body):
		if self.busy and xmpp.isResultNode(stanza):
			chats.plus()
			for node in stanza.getQueryChildren() or ():
				if node and node != "None":
					name = node.getAttr("name")
					if name:
						name = name.strip()
						if body in sub_desc(name.lower(), self.eqMap):
							count.append("%s (%s)" % (chat, name))

	commands = ((command_disco_search, "find", 2,),)
