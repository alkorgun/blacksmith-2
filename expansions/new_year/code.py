# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "new_year" # /code.py v.x2
#  Id: 02~1a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

ny_answers = ["До нового года (по GMT) осталось - ", "дн", "час", "мин", "сек"] if DefLANG in ["RU", "UA"] else ["Until the new year (GMT) left - ", "days", "hours", "minutes", "seconds"]

def command_new_year(ltype, source, body, disp):
	months = {"01": 0, "02": 31, "03": 59, "04": 90, "05": 120, "06": 151, "07": 181, "08": 212, "09": 243, "10": 273, "11": 304, "12": 334}
	time_list = strTime("%m/%d/%H/%M/%S", False).split("/")
	answer = ny_answers[0]
	days = 365 - (months[time_list[0]] + int(time_list[1]))
	if days:
		answer += "%s %s " % (str(days), ny_answers[1])
	hours = 23 - int(time_list[2])
	if hours:
		answer += "%s %s " % (str(hours), ny_answers[2])
	minutes = 59 - int(time_list[3])
	if minutes:
		answer += "%s %s " % (str(minutes), ny_answers[3])
	seconds = (59 - int(time_list[4])) + 1
	if seconds:
		answer += "%s %s" % (str(seconds), ny_answers[4])
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_new_year])
expansions[exp_name].ls.extend(["ny_answers"])

command_handler(command_new_year, {"RU": "нг", "EN": "new_year"}, 1, exp_name)
