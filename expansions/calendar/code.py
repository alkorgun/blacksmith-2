# coding: utf-8

#  BlackSmith mark.2
exp_name = "calendar" # /code.py v.x1
#  Id: 24~1a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

import calendar

def command_calendar(ltype, source, body, disp):
	y, z, date = 0, 0, list(time.gmtime())
	if body:
		body = body.split()
		x = body.pop(0)
		if isNumber(x):
			z = int(x)
			if body and isNumber(body[0]):
				y = int(body.pop(0))
	if z not in xrange(1, 13):
		y = date[0]
		z = date[1]
	elif y <= 0:
		y = date[0]
	Ans_1 = "\nCalendar:\n*\n*\tM/Y: %s\n*\n*\t%s\n*\nCurrent Date/Time: %s"
	clndr = ((calendar.month(y, z)).strip()).splitlines()
	Ans_2 = clndr.pop(0)
	Ans_3 = "\n*\t".join(clndr)
	Answer(Ans_1 % (Ans_2, Ans_3, time.asctime()), ltype, source, disp)

expansions[exp_name].funcs_add([command_calendar,])
expansions[exp_name].ls.extend([calendar.__name__])

command_handler(command_calendar, {"RU": "календарь", "EN": "calendar"}, 1, exp_name)
