# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "note" # /code.py v.x2
#  Id: 23~1a
#  Code © (2010-2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

NoteFile = dynamic % ("notepad.db")

def command_note(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		source_ = get_source(source[1], source[2])
		if source_:
			if body:
				list = body.split()
				x = (list.pop(0)).lower()
				if x in ["clear", "чисть".decode("utf-8")]:
					base = sqlite3.connect(NoteFile, timeout = 8)
					cu = base.cursor()
					base_data = cu.execute("select * from note where jid=?", (source_,)).fetchone()
					if base_data:
						cu.execute("delete from note where jid=?", (source_,))
						base.commit()
						answer = AnsBase[4]
					else:
						answer = note_answers[0]
					base.close()
				elif list:
					if x == "+":
						body = body[(body.find("+") + 2):].strip()
						if len(body) <= 512:
							date = strTime(local = False)
							base = sqlite3.connect(NoteFile, timeout = 8)
							cu = base.cursor()
							base_data = cu.execute("select * from note where jid=?", (source_,)).fetchone()
							if base_data:
								Numb, Added = itypes.Number(), False
								for line in base_data:
									if not line:
										cu.execute("update note set line_%s=? where jid=?" % (Numb._str()), ("[%s] %s" % (date, body), source_))
										base.commit()
										Added = True
										break
									Numb.plus()
								if Added:
									answer = note_answers[7] % (Numb._str())
								else:
									answer = note_answers[3]
							else:
								cu.execute("insert into note values (%s)" % (",".join(["?" for x in range(17)])), (source_, "[%s] %s" % (date, body), "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))
								base.commit()
								answer = AnsBase[4]
							base.close()
						else:
							answer = note_answers[1]
					elif x in ["-", "*"]:
						if check_number(list[0]):
							Numb = int(list.pop(0))
							if Numb in range(1, 17):
								base = sqlite3.connect(NoteFile, timeout = 8)
								cu = base.cursor()
								base_data = cu.execute("select * from note where jid=?", (source_,)).fetchone()
								if base_data:
									if x == "*":
										if base_data[Numb]:
											answer = base_data[Numb]
										else:
											answer = note_answers[5]
									elif not base_data[Numb]:
										answer = note_answers[8]
									else:
										cu.execute("update note set line_%d=? where jid=?" % (Numb), ("", source_))
										base.commit()
										answer = AnsBase[4]
								else:
									answer = note_answers[0]
								base.close()
							else:
								answer = note_answers[4]
						else:
							answer = AnsBase[30]
					else:
						answer = AnsBase[3]
				else:
					answer = AnsBase[2]
			else:
				base = sqlite3.connect(NoteFile, timeout = 8)
				cu = base.cursor()
				base_data = cu.execute("select * from note where jid=?", (source_,)).fetchone()
				if base_data:
					Numb, Notes = 0, ""
					for line in base_data:
						if not Numb:
							Numb += 1
							continue
						if line:
							Notes += "\nLine[%d] %s" % (Numb, line)
						Numb += 1
					if Notes:
						Notes = (note_answers[6] % (Notes))
						if ltype == Types[1]:
							Answer(AnsBase[11], ltype, source, disp)
						Msend(source[0], Notes, disp)
					else:
						cu.execute("delete from note where jid=?", (source_,))
						base.commit()
						answer = note_answers[0]
				else:
					answer = note_answers[0]
				base.close()
		else:
			answer = note_answers[2]
	else:
		answer = AnsBase[0]
	if locals().has_key(Types[23]):
		Answer(answer, ltype, source, disp)

def init_note_file():
	if not os.path.isfile(NoteFile):
		base = sqlite3.connect(NoteFile)
		cu = base.cursor()
		cu.execute("create table note (jid text, %s)" % (", ".join(["line_%s text" % (Numb) for Numb in range(1, 17)])))
		base.commit()
		base.close()

expansions[exp_name].funcs_add([command_note, init_note_file])
expansions[exp_name].ls.extend(["note_answers", "NoteFile"])

command_handler(command_note, {"RU": "блокнот", "EN": "note"}, 2, exp_name)

handler_register(init_note_file, "00si", exp_name)
