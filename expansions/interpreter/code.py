# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "interpreter" # /code.py v.x3
#  Id: 04~1a
#  Code © (2002-2005) by Mike Mintz [mikemintz@gmail.com]
#  Code © (2007) by Als [Als@exploit.in]
#  Code © (2009-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def handler_python_eval(ltype, source, body, disp):
	if body:
		try:
			answer = UnicodeType(eval(UnicodeType(body)))
		except:
			answer = "%s - %s" % exc_info()
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def handler_python_exec(ltype, source, body, disp):
	if body:
		if "\n" in body and body[-1] != "\n":
			body += "\n"
		answer = AnsBase[4]
		try:
			exec UnicodeType(body) in globals()
		except:
			answer = "%s - %s" % exc_info()
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def handler_python_sh(ltype, source, body, disp):
	if body:
		if oSlist[1]:
			command = sys_cmds[6] % (body.encode("utf-8"))
		else:
			command =  body.encode("cp1251")
		answer = read_pipe(command)
		if answer in ["", None]:
			answer = AnsBase[4]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def handler_python_calc(ltype, source, body, disp):
	if body:
		if len(body) <= 24 and not body.count("**"):
			eQ = re_sub("([0123456789]|[\+\-\/\*\^\.])", "", body)
			if not eQ.strip():
				try:
					answer = str(eval(body))
				except:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[2]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([handler_python_eval, handler_python_exec, handler_python_sh, handler_python_calc])

command_handler(handler_python_eval, {"RU": "eval", "EN": "eval"}, 8, exp_name)
command_handler(handler_python_exec, {"RU": "exec", "EN": "exec"}, 8, exp_name)
command_handler(handler_python_sh, {"RU": "sh", "EN": "sh"}, 8, exp_name)
command_handler(handler_python_calc, {"RU": "калк", "EN": "calc"}, 2, exp_name)
