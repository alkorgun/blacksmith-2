# coding: utf-8

#  BlackSmith mark.2
exp_name = "new_year" # /code.py v.x3
#  Id: 02~2a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_new_year(ltype, source, body, disp):
	list = ["Until the New Year (GMT) left:"]
	Time = time.gmtime()
	dr = lambda Numb: (Numb, ("s" if Numb >= 2 else ""))
	t0 = (365 if (Time.tm_year%4) else 366)
	t1 = (t0 - Time.tm_yday)
	t2 = (23 - Time.tm_hour)
	t3 = (59 - Time.tm_min)
	t4 = (59 - Time.tm_sec)
	if t1:
		list.append("%d Day%s" % dr(t1))
	if t2:
		list.append("%d Hour%s" % dr(t2))
	if t3:
		list.append("%d Minute%s" % dr(t3))
	if t4:
		list.append("%d Second%s" % dr(t4))
	if len(list) == 1:
		list = ["Happy New Year!"]
	Answer(str.join(chr(32), list), ltype, source, disp)

expansions[exp_name].funcs_add([command_new_year])

command_handler(command_new_year, {"RU": "нг", "EN": "new_year"}, 1, exp_name)
