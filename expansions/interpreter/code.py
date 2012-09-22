# coding: utf-8

#  BlackSmith mark.2
exp_name = "interpreter" # /code.py v.x7
#  Id: 04~5b
#  Code © (2002-2005) by Mike Mintz [mikemintz@gmail.com]
#  Code © (2007) by Als [Als@exploit.in]
#  Code © (2009-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def command_eval(self, ltype, source, body, disp):
		if body:
			try:
				answer = UnicodeType(eval(UnicodeType(body)))
			except:
				answer = "%s - %s" % exc_info()
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_exec(self, ltype, source, body, disp):
		if body:
			if chr(10) in body and body[-1] != chr(10):
				body += chr(10)
			answer = AnsBase[4]
			try:
				exec(UnicodeType(body), globals())
			except:
				answer = "%s - %s" % exc_info()
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_sh(self, ltype, source, body, disp):
		if body:
			if oSlist[1]:
				command = sys_cmds[6] % (body.encode("utf-8"))
			else:
				command = body.encode("cp1251")
			answer = get_pipe(command)
			if answer in ["", None]:
				answer = AnsBase[4]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_calc(self, ltype, source, body, disp):
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
		Answer(answer, ltype, source, disp)

	commands = (
		(command_eval, "eval", 8,),
		(command_exec, "exec", 8,),
		(command_sh, "sh", 8,),
		(command_calc, "calc", 2,)
					)
