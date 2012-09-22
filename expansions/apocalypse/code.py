# coding: utf-8

#  BlackSmith mark.2
exp_name = "apocalypse" # /code.py v.x2
#  Id: 0~2b
#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_apocalypse(self, ltype, source, body, disp):
		Time = time.gmtime()
		t1 = (356 - Time.tm_yday)
		if not t1:
			answer = "We all gonna die today!"
		elif t1 == 1:
			answer = "Tomorrow will be the doomsday!"
		elif t1 < 0 or Time.tm_year != 2012:
			answer = "We must be already dead..."
		else:
			answer = "There are %d days left to the Apocalypse." % (t1)
		Answer(answer, ltype, source, disp)

	commands = ((command_apocalypse, "apocalypse", 1,),)
