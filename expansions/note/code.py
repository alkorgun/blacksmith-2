# coding: utf-8

#  BlackSmith mark.2
exp_name = "note" # /code.py v.x4
#  Id: 22~3a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

NoteFile = dynamic % ("notepad.db")

def command_note(ltype, source, body, disp):
	source_ = get_source(source[1], source[2])
	if source_:
		if body:
			list_ = body.split()
			x = (list_.pop(0)).lower()
			if x in ["clear", "чисть".decode("utf-8")]:
				with database(NoteFile) as db:
					db.execute("select * from note where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						db.execute("delete from note where jid=?", (source_,))
						db.commit()
						answer = AnsBase[4]
					else:
						answer = NoteAnsBase[0]
			elif list_:
				if x == "+":
					body = body[2:].lstrip()
					if len(body) <= 512:
						date = strTime(local = False)
						with database(NoteFile) as db:
							db.execute("select * from note where jid=?", (source_,))
							db_desc = db.fetchone()
							if db_desc:
								Numb, Added = itypes.Number(), False
								for line in db_desc:
									if not line:
										db.execute("update note set line_%s=? where jid=?" % (Numb._str()), ("[%s] %s" % (date, body), source_))
										db.commit()
										Added = True
										break
									Numb.plus()
								if Added:
									answer = NoteAnsBase[7] % (Numb._str())
								else:
									answer = NoteAnsBase[3]
							else:
								db.execute("insert into note values (%s)" % (",".join(["?" for x in range(17)])), (source_, "[%s] %s" % (date, body), "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))
								db.commit()
								answer = AnsBase[4]
					else:
						answer = NoteAnsBase[1]
				elif x in ["-", "*"]:
					Numb = list_.pop(0)
					if isNumber(Numb):
						Numb = int(Numb)
						if Numb in range(1, 17):
							with database(NoteFile) as db:
								db.execute("select * from note where jid=?", (source_,))
								db_desc = db.fetchone()
								if db_desc:
									if x == "*":
										if db_desc[Numb]:
											answer = db_desc[Numb]
										else:
											answer = NoteAnsBase[5]
									elif not db_desc[Numb]:
										answer = NoteAnsBase[8]
									else:
										db.execute("update note set line_%d=? where jid=?" % (Numb), ("", source_))
										db.commit()
										answer = AnsBase[4]
								else:
									answer = NoteAnsBase[0]
						else:
							answer = NoteAnsBase[4]
					else:
						answer = AnsBase[30]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			with database(NoteFile) as db:
				db.execute("select * from note where jid=?", (source_,))
				db_desc = db.fetchone()
				if db_desc:
					Notes, Numb = str(), itypes.Number()
					for line in db_desc:
						if not Numb._int():
							Numb.plus()
							continue
						if line:
							Notes += "\nLine[%s] %s" % (Numb._str(), line)
						Numb.plus()
					if Notes:
						Notes = (NoteAnsBase[6] % (Notes))
						if ltype == Types[1]:
							Answer(AnsBase[11], ltype, source, disp)
						Msend(source[0], Notes, disp)
					else:
						db.execute("delete from note where jid=?", (source_,))
						db.commit()
						answer = NoteAnsBase[0]
				else:
					answer = NoteAnsBase[0]
	else:
		answer = NoteAnsBase[2]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def init_note_file():
	if not os.path.isfile(NoteFile):
		with database(NoteFile) as db:
			db.execute("create table note (jid text, %s)" % (", ".join(["line_%s text" % (Numb) for Numb in range(1, 17)])))
			db.commit()

expansions[exp_name].funcs_add([command_note, init_note_file])
expansions[exp_name].ls.extend(["NoteAnsBase", "NoteFile"])

command_handler(command_note, {"RU": "блокнот", "EN": "note"}, 2, exp_name)

handler_register(init_note_file, "00si", exp_name)
