# coding: utf-8

#  BlackSmith mark.2
# exp_name = "clear_stats" # /code.py v.x4
#  Id: 12~4c
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def join_clear(self, conf, nick, instance, role, stanza, disp):
		if instance:
			for obj in Chats[conf].get_users():
				if obj.source == instance and not obj.ishere and obj.nick != nick:
					if Chats[conf].isHere(obj.nick):
						Chats[conf].desc.pop(obj.nick)

	def exit_clear(self, conf, nick, sbody, scode, disp):
		instance = get_source(conf, nick)
		if instance:
			delete = False
			for obj in Chats[conf].get_users():
				if obj.source == instance and obj.ishere:
					delete = True
					break
			if delete and Chats[conf].isHere(nick):
				Chats[conf].desc.pop(nick)

	handlers = (
		(join_clear, "04eh"),
		(exit_clear, "05eh")
					)
