# coding: utf-8

#  BlackSmith mark.2
# exp_name = "interpreter" # /code.py v.x12
#  Id: 04~10c
#  Idea © (2002-2005) by Mike Mintz [mikemintz@gmail.com]
#  Idea © (2007) by Als [Als@exploit.in]
#  Code © (2009-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	opts =  ("-l", "-r", "-s")

	opt_locals = opts[0]
	opt_result = opts[1]
	opt_silent = opts[2]

	def command_eval(self, stype, source, body, disp):
		silent = False
		if body:
			args = body.split(None, 1)
			if len(args) == 2:
				if self.opt_silent == (args.pop(0)).lower():
					silent = True
					body = args.pop()
			try:
				answer = unicode(eval(unicode(body)))
				if not answer.strip():
					answer = `answer`
			except Exception, exc:
				answer = exc_str(exc)
		else:
			answer = AnsBase[1]
		if not silent:
			Answer(answer, stype, source, disp)

	def command_exec(self, stype, source, body, disp):
		silent = False
		if body:
			opts = set()
			while len(opts) < 3:
				args = body.split(None, 1)
				if len(args) != 2:
					break
				temp = (args.pop(0)).lower()
				if (temp not in self.opts):
					break
				opts.add(temp)
				body = args.pop()
			if not all([(temp in opts) for temp in self.opts[-2:]]):
				if self.opt_silent in opts:
					silent = True
				try:
					exec(unicode(body + chr(10)), (locals if self.opt_locals in opts else globals)())
				except:
					answer = "%s - %s" % exc_info()
				else:
					try:
						answer = unicode(result) if self.opt_result in opts else AnsBase[4]
					except Exception, exc:
						answer = exc_str(exc)
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		if not silent:
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

	taboo = chr(42)*2

	compile_math = compile__("([0-9]|[\+\-\(\/\*\)\%\^\.])")

	def command_calc(self, stype, source, body, disp):
		if body:
			if self.taboo not in body and 32 >= len(body):
				if not self.compile_math.sub("", body).strip():
					try:
						answer = unicode(eval(body))
					except ZeroDivisionError:
						answer = "+\xe2\x88\x9e"
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
