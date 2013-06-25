# coding: utf-8

#  BlackSmith mark.2
# exp_name = "wtf" # /code.py v.x4
#  Id: 28~4c
#  Code © (2012-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		check_sqlite()
		expansion.__init__(self, name)

	Base = dynamic % ("wtf.db")
	ChatBase = "wtf.db"

	def command_wtf(self, stype, source, body, disp):
		if body:
			ls = body.split(None, 1)
			arg0 = (ls.pop(0)).lower()
			if arg0 in ("all", "всё".decode("utf-8")):
				ls = []
				with database(self.Base) as db:
					db("select name from wtf order by name")
					defs = db.fetchall()
				if defs:
					ls.append(self.AnsBase[0] % (len(defs), enumerated_list([name[0].title() for name in defs])))
				if Chats.has_key(source[1]):
					with database(cefile(chat_file(source[1], self.ChatBase))) as db:
						db("select name from wtf order by name")
						defs = db.fetchall()
					if defs:
						ls.append(self.AnsBase[1] % (len(defs), source[1], enumerated_list([name[0].title() for name in defs])))
				if ls:
					answer = self.AnsBase[-1] + str.join(chr(10)*2, ls)
				else:
					answer = self.AnsBase[2]
			elif arg0 in ("search", "искать".decode("utf-8")):
				if ls:
					body = ls[0].lower()
					ls = []
					with database(self.Base) as db:
						db("select name, data from wtf order by name")
						desc = db.fetchall()
					if desc:
						for name, data in desc:
							data = data.lower()
							numb = data.count(body)
							if numb or body in name or name in body:
								ls.append(self.AnsBase[3] % (name.title(), numb))
					if Chats.has_key(source[1]):
						with database(cefile(chat_file(source[1], self.ChatBase))) as db:
							db("select name, data from wtf order by name")
							desc = db.fetchall()
						if desc:
							for name, data in desc:
								data = data.lower()
								numb = data.count(body)
								if numb or body in name or name in body:
									ls.append(self.AnsBase[3] % (name.title(), numb))
					if ls:
						answer = self.AnsBase[-1] + enumerated_list(ls)
					else:
						answer = self.AnsBase[4]
			else:
				body = body.lower()
				answer = None
				with database(self.Base) as db:
					db("select * from wtf where name=?", (body,))
					desc = db.fetchone()
				if desc:
					name, data, nick, date = desc
					answer = self.AnsBase[5] % (name.title(), data, nick, date)
				if Chats.has_key(source[1]) and not answer:
					with database(cefile(chat_file(source[1], self.ChatBase))) as db:
						db("select * from wtf where name=?", (body,))
						desc = db.fetchone()
					if desc:
						name, data, nick, date = desc
						answer = self.AnsBase[5] % (name.title(), data, nick, date)
				if not answer:
					answer = self.AnsBase[6] % (body)
		else:
			ls = []
			with database(self.Base) as db:
				db("select name from wtf order by name")
				defs = db.fetchall()
			if defs:
				ls.append(self.AnsBase[7] % len(defs))
			if Chats.has_key(source[1]):
				with database(cefile(chat_file(source[1], self.ChatBase))) as db:
					db("select name from wtf order by name")
					defs = db.fetchall()
				if defs:
					ls.append(self.AnsBase[8] % (len(defs), source[1]))
			if ls:
				answer = self.AnsBase[-1] + str.join(chr(10), ls)
			else:
				answer = self.AnsBase[2]
		Answer(answer, stype, source, disp)

	sep = chr(61)

	def addDef(self, base, name, data, nick):
		with database(base) as db:
			db("select date from wtf where name=?", (name,))
			date = db.fetchone()
			if data:
				if date:
					db("update wtf set data=?, nick=?, date=? where name=?", (data, nick, time.asctime(), name))
				else:
					db("insert into wtf values (?,?,?,?)", (name, data, nick, time.asctime()))
				db.commit()
				answer = AnsBase[4]
			elif date:
				db("delete from wtf where name=?", (name,))
				db.commit()
				answer = AnsBase[4]
			else:
				answer = self.AnsBase[6] % (name)
		return answer

	def command_def(self, stype, source, body, disp):
		if body:
			ls = body.split(None, 1)
			arg0 = (ls.pop(0)).lower()
			if arg0 in ("globally", "глобально".decode("utf-8")):
				if enough_access(source[1], source[2], 7):
					if ls and self.sep in ls[0]:
						ls = ls[0].split(self.sep, 1)
						name, data = ls
						name, data = (name.rstrip()).lower(), data.lstrip()
						if name and len(name) <= 64:
							answer = self.addDef(self.Base, name, data, source[2])
						else:
							answer = AnsBase[2]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[10]
			elif Chats.has_key(source[1]):
				if self.sep in body:
					ls = body.split(self.sep, 1)
					name, data = ls
					name, data = (name.rstrip()).lower(), data.lstrip()
					if name and len(name) <= 64:
						with database(self.Base) as db:
							db("select date from wtf where name=?", (name,))
							date = db.fetchone()
						if date and data:
							answer = self.AnsBase[9] % (name)
						else:
							answer = self.addDef(cefile(chat_file(source[1], self.ChatBase)), name, data, source[2])
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				answer = self.AnsBase[10]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def init_wtf_base(self):
		if not os.path.isfile(self.Base):
			with database(self.Base) as db:
				db("create table wtf (name text, data text, nick text, date text)")
				db.commit()

	def init_local_wtf_base(self, conf):
		filename = cefile(chat_file(conf, self.ChatBase))
		if not os.path.isfile(filename):
			with database(filename) as db:
				db("create table wtf (name text, data text, nick text, date text)")
				db.commit()

	commands = (
		(command_wtf, "wtf", 2,),
		(command_def, "def", 4,)
					)

	handlers = (
		(init_wtf_base, "00si"),
		(init_local_wtf_base, "01si")
					)
