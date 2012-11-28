# coding: utf-8

#  BlackSmith mark.2
# exp_name = "interpreter" # /code.py v.x8
#  Id: 04~6c
#  Code © (2002-2005) by Mike Mintz [mikemintz@gmail.com]
#  Code © (2007) by Als [Als@exploit.in]
#  Code © (2009-2012) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_eval(self, stype, source, body, disp):
		if body:
			try:
				answer = UnicodeType(eval(UnicodeType(body)))
				if not answer.strip():
					answer = "None (%s)" % (answer)
			except:
				answer = "%s - %s" % exc_info()
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_exec(self, stype, source, body, disp):
		if body:
			if not body.endswith(chr(10)):
				body += chr(10)
			try:
				exec(UnicodeType(body), globals())
			except:
				answer = "%s - %s" % exc_info()
			else:
				answer = AnsBase[4]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_sh(self, stype, source, body, disp):
		if body:
			if oSlist[1]:
				command = sys_cmds[6] % (body.encode("utf-8"))
			else:
				command = body.encode("cp1251")
			answer = get_pipe(command)
			if not answer.strip():
				answer = AnsBase[4]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_calc(self, stype, source, body, disp):
		if body:
			if not body.count(chr(42)*2) and 32 >= len(body):
				comp = compile__("([0-9]|[\+\-\(\/\*\)\%\^\.])")
				expr = (not comp.sub("", body).strip())
				if expr:
					try:
						answer = UnicodeType(eval(body))
					except ZeroDivisionError:
						answer = "+∞".decode("utf-8")
					except:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	commands = (
		(command_eval, "eval", 8,),
		(command_exec, "exec", 8,),
		(command_sh, "sh", 8,),
		(command_calc, "calc", 2,)
					)
