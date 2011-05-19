# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "clear_stats" # /code.py v.x1
#  Id: 12~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def join_clear(conf, nick, instance, afl, role, disp):
	if instance:
		for user in Chats[conf].get_users():
			if user.source == instance and not user.ishere and user.nick != nick:
				if Chats[conf].isHere(user.nick):
					del Chats[conf].users[user.nick]

def exit_clear(conf, nick, status, scode, disp):
	instance = get_source(conf, nick)
	if instance:
		delete = False
		for user in Chats[conf].get_users():
			if user.source == instance and user.ishere:
				delete = True
				break
		if delete and Chats[conf].isHere(nick):
			del Chats[conf].users[nick]

expansions[exp_name].funcs_add([join_clear, exit_clear])

handler_register(join_clear, "04eh", exp_name)
handler_register(exit_clear, "05eh", exp_name)
