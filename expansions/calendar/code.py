# coding: utf-8

#  BlackSmith mark.2
exp_name = "calendar" # /code.py v.x2
#  Id: 24~2a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

import calendar

def command_calendar(ltype, source, body, disp):
	date = time.gmtime()
	y, z = 0, 0
	if body:
		body = body.split()
		x = body.pop(0)
		if isNumber(x):
			z = int(x)
			if body and isNumber(body[0]):
				y = int(body.pop(0))
	if z not in xrange(1, 13):
		y = (date.tm_year)
		z = (date.tm_mon)
	elif y <= 0:
		y = (date.tm_year)
	Ans_1 = "\nCalendar:\n*\n*\tM/Y: %s\n*\n*\t%s\n*\nCurrent Date/Time: %s"
	clndr = ((calendar.month(y, z)).strip()).splitlines()
	Ans_2 = clndr.pop(0)
	Ans_3 = "\n*\t".join(clndr)
	Answer(Ans_1 % (Ans_2, Ans_3, time.asctime(date)), ltype, source, disp)

expansions[exp_name].ls.extend([calendar.__name__, command_calendar.func_name])

command_handler(command_calendar, {"RU": "календарь", "EN": "calendar"}, 1, exp_name)
