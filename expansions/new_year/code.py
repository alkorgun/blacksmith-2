# coding: utf-8

#  BlackSmith mark.2
exp_name = "new_year" # /code.py v.x4
#  Id: 02~3b
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_new_year(self, ltype, source, body, disp):
		list = ["Until the New Year (UTC) left:"]
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

	commands = ((command_new_year, "new_year", 1,),)
