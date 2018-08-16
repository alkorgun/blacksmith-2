# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Внимание! %s (%s) загнал меня в → '%s'", # 0
		"I'm %s → XMPP BOT. Пришел по приказу %s" # 1
	)])
else:
	AnsBase_temp = (
		"Attention! %s (%s) sent me in to -> '%s'", # 0
		"I'm %s -> XMPP BOT. Joined by order from %s" # 1
	)