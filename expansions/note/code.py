# coding: utf-8

#  BlackSmith mark.2
# exp_name = "note" # /code.py v.x8
#  Id: 22~7c
#  Code © (2010-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		check_sqlite()
		expansion.__init__(self, name)

	NoteFile = dynamic % ("notepad.db")

	def command_note(self, stype, source, body, disp):
		source_ = get_source(source[1], source[2])
		if source_:
			if body:
				ls = body.split()
				arg0 = (ls.pop(0)).lower()
				if arg0 in ("clear", "чисть".decode("utf-8")):
					with database(self.NoteFile) as db:
						db("select * from note where jid=?", (source_,))
						db_desc = db.fetchone()
						if db_desc:
							db("delete from note where jid=?", (source_,))
							db.commit()
							answer = AnsBase[4]
						else:
							answer = self.AnsBase[0]
				elif ls:
					if arg0 == "+":
						body = body[2:].lstrip()
						if len(body) <= 512 or enough_access(source[1], source[2], 7):
							date = strfTime(local = False)
							with database(self.NoteFile) as db:
								db("select * from note where jid=?", (source_,))
								db_desc = db.fetchone()
								if db_desc:
									numb = itypes.Number()
									for line in db_desc:
										if not line:
											db("update note set line_%s=? where jid=?" % (numb._str()), ("[%s] %s" % (date, body), source_))
											db.commit()
											answer = self.AnsBase[7] % (numb._str())
											break
										numb.plus()
									else:
										answer = self.AnsBase[3]
								else:
									db("insert into note values (%s)" % (",".join(["?" for x in xrange(17)])), (source_, "[%s] %s" % (date, body), "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))
									db.commit()
									answer = AnsBase[4]
						else:
							answer = self.AnsBase[1]
					elif arg0 in ("-", "*"):
						numb = ls.pop(0)
						if isNumber(numb):
							numb = int(numb)
							if numb in xrange(1, 17):
								with database(self.NoteFile) as db:
									db("select * from note where jid=?", (source_,))
									db_desc = db.fetchone()
									if db_desc:
										if arg0 == "*":
											if db_desc[numb]:
												answer = db_desc[numb]
											else:
												answer = self.AnsBase[5]
										elif not db_desc[numb]:
											answer = self.AnsBase[8]
										else:
											db("update note set line_%d=? where jid=?" % (numb), ("", source_))
											db.commit()
											answer = AnsBase[4]
									else:
										answer = self.AnsBase[0]
							else:
								answer = self.AnsBase[4]
						else:
							answer = AnsBase[30]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				with database(self.NoteFile) as db:
					db("select * from note where jid=?", (source_,))
					db_desc = db.fetchone()
				if db_desc:
					notes = []
					for numb, line in enumerate(db_desc):
						if numb and line:
							notes.append("Line[%s] %s" % (numb, line))
					if notes:
						answer = self.AnsBase[6] + str.join(chr(10), notes)
						if stype == sBase[1]:
							Message(source[0], answer, disp)
							answer = AnsBase[11]
					else:
						with database(self.NoteFile) as db:
							db("delete from note where jid=?", (source_,))
							db.commit()
						answer = self.AnsBase[0]
				else:
					answer = self.AnsBase[0]
		else:
			answer = self.AnsBase[2]
		Answer(answer, stype, source, disp)

	def init_note_file(self):
		if not os.path.isfile(self.NoteFile):
			with database(self.NoteFile) as db:
				db("create table note (jid text, %s)" % (", ".join(["line_%s text" % (numb) for numb in xrange(1, 17)])))
				db.commit()

	commands = ((command_note, "note", 2,),)

	handlers = ((init_note_file, "00si"),)
