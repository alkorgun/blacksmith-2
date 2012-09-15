# coding: utf-8

#  BlackSmith mark.2
exp_name = "apocalypse" # /code.py v.x1
#  Id: 0~1a
#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

def command_apocalypse(ltype, source, body, disp):
	Time = time.gmtime()
	t1 = (356 - Time.tm_yday)
	if not t1:
		answer = "We all gonna die today!"
	elif t1 == 1:
		answer = "Tomorrow will be the doomday!"
	elif t1 < 0 or Time.tm_year != 2012:
		answer = "We must be already dead..."
	else:
		answer = "There are %d days left to the Apocalypse." % (t1)
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_apocalypse])

command_handler(command_apocalypse, {"RU": "апокалипсис", "EN": "apocalypse"}, 1, exp_name)
