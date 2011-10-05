# coding: utf-8

#  BlackSmith mark.2
exp_name = "turn" # /code.py v.x1
#  Id: 21~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

TableRU = '''ёйцукенгшщзхъфывапролджэячсмитьбю.!"№;%:?*()_+/-=\ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.'''.decode("utf-8")
TableEN = '''`qwertyuiop[]asdfghjkl;'zxcvbnm,./!@#;%^&*()_+.-=\~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>/'''

TurnBase = {}

def command_turn(ltype, source, body, disp):
	
	def Turn(conf, body):
		list_ = {}
		for nick in Chats[conf].get_nicks():
			if Chats[conf].isHereNow(nick):
				for x in (["%s%s" % (nick, Key) for Key in [":",",",">"]] + [nick]):
					if body.count(x):
						Numb = "*%s*" % str(len(list_.keys()) + 1)
						list_[Numb] = x
						body = body.replace(x, Numb)
		Turned = ""
		for x in body:
			if x in TableEN:
				Turned += TableRU[TableEN.index(x)]
			elif x in TableRU:
				Turned += TableEN[TableRU.index(x)]
			else:
				Turned += x
		return sub_desc(Turned, list_)
	
	if Chats.has_key(source[1]):
		if body:
			answer = Turn(source[1], body)
		else:
			source_ = get_source(source[1], source[2])
			if source_ and TurnBase[source[1]].has_key(source_):
				(Time, body) = TurnBase[source[1]].pop(source_)
				body = "Turn\->\n[%s] <%s>: %s" % (Time, source[2], Turn(source[1], body))
				Msend(source[1], body, disp)
			else:
				answer = AnsBase[7]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def collect_turnable(stanza, isConf, ltype, source, body, isToBs, disp):
	if isConf and ltype == Types[1] and source[2]:
		source_ = get_source(source[1], source[2])
		if source_:
			TurnBase[source[1]][source_] = (strTime("%H:%M:%S", False), body)

def init_Turn_Base(conf):
	TurnBase[conf] = {}

def edit_Turn_Base(conf):
	del TurnBase[conf]

expansions[exp_name].funcs_add([command_turn, collect_turnable, init_Turn_Base, edit_Turn_Base])
expansions[exp_name].ls.extend(["TurnBase", "TableRU", "TableEN"])

command_handler(command_turn, {"RU": "турн", "EN": "turn"}, 1, exp_name)

handler_register(init_Turn_Base, "01si", exp_name)
handler_register(edit_Turn_Base, "04si", exp_name)
handler_register(collect_turnable, "01eh", exp_name)
