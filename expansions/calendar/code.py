# coding: utf-8

#  BlackSmith mark.2
exp_name = "calendar" # /code.py v.x3
#  Id: 24~3b
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	import calendar

	def command_calendar(self, ltype, source, body, disp):
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
		clndr = ((self.calendar.month(y, z)).strip()).splitlines()
		Ans_2 = clndr.pop(0)
		Ans_3 = "\n*\t".join(clndr)
		Answer(Ans_1 % (Ans_2, Ans_3, time.asctime(date)), ltype, source, disp)

	commands = ((command_calendar, "calendar", 1,),)
