# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "more" # /code.py v.x1
#  Id: 21~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_more(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if Chats[source[1]].more:
			body = "[&&] %s" % (Chats[source[1]].more)
			Chats[source[1]].more = ""
			Msend(source[1], body, disp)
	else:
		Answer(AnsBase[0], ltype, source, disp)

expansions[exp_name].funcs_add([command_more])

command_handler(command_more, {"RU": "далее", "EN": "more"}, 1, exp_name)
