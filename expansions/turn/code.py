# coding: utf-8

#  BlackSmith mark.2
# exp_name = "turn" # /code.py v.x3
#  Id: 21~3c
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	TableRU = '''ёйцукенгшщзхъфывапролджэячсмитьбю.!"№;%:?*()_+/-=\\ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.'''.decode("utf-8")
	TableFI = '''`qwertyuiopåvasdfghjklöäzxcvbnm,.-½!"#¤%&*()_+.-=\\?QWERTYUIOPÅ^ASDFGHJKLÖÄZXCVBNM;:_'''.decode("utf-8")
	TableEN = '''`qwertyuiop[]asdfghjkl;'zxcvbnm,./!@#;%^&*()_+.-=\\~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''
	TableLA = (TableFI if DefLANG == "FI" else TableEN)

	del TableFI, TableEN

	TurnBase = {}

	def command_turn(self, stype, source, body, disp):
		
		def Turn(conf, body):
			desc = {}
			for user in Chats[conf].get_users():
				if user.ishere:
					for app in ([(user.nick + Key) for Key in (":", ",", ">")] + [user.nick]):
						if app in body:
							Numb = "*%s*" % str(len(desc.keys()) + 1)
							desc[Numb] = app
							body = body.replace(app, Numb)
			Turned = str()
			for smb in body:
				if smb in self.TableLA:
					Turned += self.TableRU[self.TableLA.index(smb)]
				elif smb in self.TableRU:
					Turned += self.TableLA[self.TableRU.index(smb)]
				else:
					Turned += smb
			return sub_desc(Turned, desc)
		
		if Chats.has_key(source[1]):
			if body:
				answer = "Turn\->\n" + Turn(source[1], body)
			else:
				source_ = get_source(source[1], source[2])
				if source_ and self.TurnBase[source[1]].has_key(source_):
					(Time, body) = self.TurnBase[source[1]].pop(source_)
					body = "Turn\->\n[%s] <%s>: %s" % (Time, source[2], Turn(source[1], body))
					Message(source[1], body, disp)
				else:
					answer = AnsBase[7]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[6]):
			Answer(answer, stype, source, disp)

	def collect_turnable(self, stanza, isConf, stype, source, body, isToBs, disp):
		if isConf and stype == Types[1] and source[2]:
			source_ = get_source(source[1], source[2])
			if source_:
				self.TurnBase[source[1]][source_] = (strfTime("%H:%M:%S", False), body)

	def init_turn_base(self, conf):
		self.TurnBase[conf] = {}

	def edit_turn_base(self, conf):
		del self.TurnBase[conf]

	commands = ((command_turn, "turn", 1,),)

	handlers = (
		(init_turn_base, "01si"),
		(edit_turn_base, "04si"),
		(collect_turnable, "01eh")
					)
