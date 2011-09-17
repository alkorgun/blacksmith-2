# coding: utf-8

#  BlackSmith mark.2
exp_name = "interpreter" # /code.py v.x4
#  Id: 04~2a
#  Code © (2002-2005) by Mike Mintz [mikemintz@gmail.com]
#  Code © (2007) by Als [Als@exploit.in]
#  Code © (2009-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def command_eval(ltype, source, body, disp):
	if body:
		try:
			answer = UnicodeType(eval(UnicodeType(body)))
		except:
			answer = "%s - %s" % exc_info()
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_exec(ltype, source, body, disp):
	if body:
		if chr(10) in body and body[-1] != chr(10):
			body += chr(10)
		answer = AnsBase[4]
		try:
			exec UnicodeType(body) in globals()
		except:
			answer = "%s - %s" % exc_info()
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_sh(ltype, source, body, disp):
	if body:
		if oSlist[1]:
			command = sys_cmds[6] % (body.encode("utf-8"))
		else:
			command =  body.encode("cp1251")
		answer = get_pipe(command)
		if answer in ["", None]:
			answer = AnsBase[4]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_calc(ltype, source, body, disp):
	if body:
		if len(body) <= 24 and not body.count("**"):
			comp = compile__("([0123456789]|[\+\-\/\*\^\.])")
			expr = (not comp.sub("", body).strip())
			if expr:
				try:
					answer = UnicodeType(eval(body))
				except:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[2]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_eval, command_exec, command_sh, command_calc])

command_handler(command_eval, {"RU": "eval", "EN": "eval"}, 8, exp_name)
command_handler(command_exec, {"RU": "exec", "EN": "exec"}, 8, exp_name)
command_handler(command_sh, {"RU": "sh", "EN": "sh"}, 8, exp_name)
command_handler(command_calc, {"RU": "калк", "EN": "calc"}, 2, exp_name)
