# coding: utf-8

#  BlackSmith mark.2
exp_name = "books" # /code.py v.x5 alpha
#  Id: 29~5b
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	import fb2

	BooksFile, ReadersFile = dynamic % ("books.db"), dynamic % ("readers.db")

	def importFB2(self, path):
		book = get_file(path)
		book_enc = self.fb2.get_enc(book)
		if not book_enc:
			raise SelfExc("Can't get encoding!")
		(desc, body) = self.fb2.get_data(book.decode(book_enc))
		if not desc:
			raise SelfExc("Can't get <description>!")
		if not body:
			raise SelfExc("Can't get <body>!")
		(Name, author, date, genre, seq1, seq2, coverD, annt) = desc
		if not Name:
			raise SelfExc("Can't get <book-title>!")
		a2 = self.getID(Name)
		if not a2:
			raise SelfExc("Can't make book-ID!")
		with database(self.BooksFile) as db:
			db("select * from books where id=?", (a2,))
			db_desc = db.fetchone()
			if not db_desc:
				db("insert into books (id, name, nick, date) values (?,?,?,?)", (a2, Name, "WitcherGeralt", time.asctime()))
				if author:
					db("update books set author=? where id=?", (author, a2))
				if date:
					db("update books set year=? where id=?", (date, a2))
				if genre:
					db("update books set genre=? where id=?", (genre, a2))
				if annt:
					db("update books set annotation=? where id=?", (annt, a2))
				if seq1:
					db("update books set seq1=? where id=?", (seq1, a2))
				if seq2:
					db("update books set seq2=? where id=?", (seq2, a2))
				if coverD:
					c0, cover = coverD
					db("update books set c0=? where id=?", (c0, a2))
					db("update books set cover=? where id=?", (cover, a2))
				db("create table %s (page integer, data text)" % a2)
				ls = []
				Numb = itypes.Number()
				Number = itypes.Number()
				lTotal = itypes.Number()
				for line in body.splitlines():
					line = line.strip()
					ls.append(line)
					if Number.plus(len(line)) >= 2048:
						db("insert into %s values (?,?)" % (a2), (Numb.plus(), str.join(chr(10), ls)))
						lTotal.plus(Number._int())
						ls = []
						Number = itypes.Number()
				if ls:
					lTotal.plus(Number._int())
					db("insert into %s values (?,?)" % (a2), (Numb.plus(), str.join(chr(10), ls)))
				db.commit()
				raise SelfExc("Done. ID - '%s', total pages: %s" % (a2, lTotal._str()))
			else:
				raise SelfExc("A book with the same name is already in the libraly!")

	def getID(self, Name):
		while Name.startswith(("1","2","3","4","5","6","7","8","9","0")):
			Name = Name[1:]
		Name = sub_desc(Name, ((chr(95), chr(32)),)).lower()
		Name = sub_desc(Name, CharCase[3]).strip()
		Name = sub_desc(Name, (chr(32), chr(10), chr(13), chr(9)), chr(95))
		return (Name if Name != "books" else None)

	def command_get_books(self, ltype, source, body, disp):
		if body:
			list = body.split()
			a1 = (list.pop(0)).lower()
			if a1 in ("show", "показать".decode("utf-8")):
				if list:
					a2 = (list.pop(0)).lower()
					if a2 in ("names", "названия".decode("utf-8")):
						with database(self.BooksFile) as db:
							db("select name from books order by name")
							db_desc = db.fetchall()
							if db_desc:
								ls, Numb = ["Books:"], itypes.Number()
								for Name in db_desc:
									ls.append("%d) %s" % (Numb.plus(), Name[0]))
								answer = str.join(chr(10), ls)
							else:
								answer = self.AnsBase[0]
					else:
						a0, ls = a2, "author;genre;seq1".split(";")
						desc = {
							"автор".decode("utf-8"): ls[0],
							"жанр".decode("utf-8"): ls[1],
							"серию".decode("utf-8"): ls[2],
							"cycle": ls[2]
										}
						if desc.has_key(a2):
							a2 = desc.get(a2, None)
						if a2 in ls and list:
							a3 = body[((body.lower()).find(a0) + len(a0)):].strip()
							with database(self.BooksFile) as db:
								if a2 in ("author", "genre"):
									db("select name from books where %s like ? order by name" % (a2), (a3,))
									db_desc = db.fetchall()
									if db_desc:
										ls, Numb = [a3 + ":"], itypes.Number()
										for Name in db_desc:
											ls.append("%d) %s" % (Numb.plus(), Name[0]))
										answer = str.join(chr(10), ls)
									else:
										answer = self.AnsBase[1] % (a0)
								else:
									db("select seq1, seq2, name from books where seq1 like ? order by seq1, seq2", (a3,))
									db_desc = db.fetchall()
									if db_desc:
										ls, Numb = [a3 + ":"], itypes.Number()
										for seq1, seq2, Name in db_desc:
											ls.append("%d) %s #%d - %s" % (Numb.plus(), seq1, seq2, Name))
										answer = str.join(chr(10), ls)
									else:
										answer = self.AnsBase[2]
						else:
							answer = AnsBase[2]
				else:
					with database(self.BooksFile) as db:
						db("select id, author from books order by author, id")
						db_desc = db.fetchall()
					if db_desc:
						ls, Numb = ["Books:"], itypes.Number()
						for id, author in db_desc:
							ls.append("%d) '%s' - %s" % (Numb.plus(), id, author))
						answer = str.join(chr(10), ls)
					else:
						answer = self.AnsBase[0]
			elif a1 in ("info", "инфо".decode("utf-8")):
				if list:
					a2 = body[((body.lower()).find(a1) + len(a1)):].strip()
					a3 = self.getID(a2)
					with database(self.BooksFile) as db:
						db("select * from books where id=? or name like ?", (a3, a2))
						info = db.fetchone()
						if info:
							(id, Name, Author, Year, Genre, seq1, seq2, c0, Cover, Annt, link, Nick, Date) = info
							del c0, Cover, info
							ls = ["Name: %s" % (Name if Name else id)]
							if Year:
								ls.append("Year: %s" % (Year))
							if Genre:
								ls.append("Genre: %s" % (Genre))
							if Author:
								ls.append("Author: %s" % (Author))
							db("select page from %s" % id)
							lines = db.fetchall()
							if lines:
								ls.append("Pages: %d" % max(lines))
								del lines
							if seq1:
								seq3 = "Series: %s" % ("%s #%s" % (seq1, seq2) if seq2 else seq1)
								ls.append(seq3)
							if link:
								ls.append("Link: %s" % (link))
							if Annt:
								ls.append("Annotation:\n\t%s" % (Annt))
							ls.append("\nAdded by: %s (Last Up.: %s)" % (Nick, Date))
							answer = str.join(chr(10), ls)
						else:
							answer = self.AnsBase[3]
				else:
					answer = AnsBase[2]
			elif a1 in ("read", "читать".decode("utf-8")):
				jid = get_source(source[1], source[2])
				if list:
					a2 = (list.pop(0)).lower()
					if a2 in ("next", "далее".decode("utf-8")):
						if jid:
							with database(self.ReadersFile) as db:
								db("select book, page from readers where jid=?", (jid,))
								data = db.fetchone()
								if data:
									book, page = data
									page += 1
								else:
									answer = self.AnsBase[4]
						else:
							answer = self.AnsBase[5]
					elif isNumber(a2):
						book = self.getID(body[((body.lower()).find(a2) + len(a2)):])
						page = int(a2)
					else:
						book = self.getID(body[((body.lower()).find(a1) + len(a1)):])
						page = 1
				else:
					if jid:
						with database(self.ReadersFile) as db:
							db("select book, page from readers where jid=?", (jid,))
							data = db.fetchone()
							if data:
								book, page = data
							else:
								answer = self.AnsBase[4]
					else:
						answer = self.AnsBase[5]
				if locals().has_key("book"):
					with database(self.BooksFile) as db:
						db("select * from books where id=?", (book,))
						data = db.fetchone()
						if data:
							db("select data from %s where page=?" % (book), (page,))
							data = db.fetchone()
							if data:
								if ltype == Types[1]:
									answer = AnsBase[11]
								Msend(source[0], data[0], disp)
								if jid:
									with database(self.ReadersFile) as db:
										db("select * from readers where jid=?", (jid,))
										data = db.fetchone()
										if data:
											db("update readers set book=?, page=? where jid=?", (book, page, jid))
										else:
											db("insert into readers values (?,?,?)", (jid, book, page))
							else:
								db("select page from %s" % book)
								lines = db.fetchall()
								if lines:
									answer = self.AnsBase[6] % max(lines)
								else:
									answer = self.AnsBase[7]
						else:
							answer = self.AnsBase[3]
			else:
				answer = AnsBase[2]
		else:
			with database(self.BooksFile) as db:
				db("select id from books")
				db_desc = db.fetchall()
			if db_desc:
				answer = self.AnsBase[8] % len(db_desc)
			else:
				answer = self.AnsBase[0]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_set_books(self, ltype, source, body, disp):
		if body:
			list = body.split()
			if len(list) >= 2:
				a1 = (list.pop(0)).lower()
				if a1 in ("add", "добавить".decode("utf-8")):
					a2 = (list.pop(0)).lower()
					if a2 in ("file", "fb2", "файл".decode("utf-8")):
						if list:
							Path = body[((body.lower()).find(a2) + len(a2)):].strip()
							try:
								exists = os.path.isfile(Path)
							except:
								exists = False
							if exists:
								try:
									self.importFB2(Path)
								except SelfExc:
									answer = exc_info()[1]
								except:
									collectExc(self.importFB2, "library add fb2 %s" % Path)
									answer = AnsBase[7]
							else:
								answer = self.AnsBase[9]
						else:
							answer = AnsBase[2]
					else:
						Name = body[((body.lower()).find(a1) + len(a1)):].strip()
						a2 = self.getID(Name)
						if a2:
							with database(self.BooksFile) as db:
								db("select * from books where id=?", (a2,))
								db_desc = db.fetchone()
								if db_desc:
									answer = self.AnsBase[10]
								else:
									db("insert into books (id, name, nick, date) values (?,?,?,?)", (a2, Name, source[2].strip(), time.asctime()))
									db("create table %s (page integer, data text)" % a2)
									db.commit()
									answer = self.AnsBase[11] % (a2)
						else:
							answer = self.AnsBase[15]
				elif a1 in ("edit", "править".decode("utf-8")):
					if len(list) >= 4:
						a2 = self.getID(list.pop(0))
						if a2:
							a3 = (list.pop(0)).lower()
							if a3 in ("info", "инфо".decode("utf-8")):
								a4 = (list.pop(0)).lower()
								a0, ls = a4, "author;year;genre;seq1;seq2;cover;annotation;link;name;c0".split(";")
								desc = {
									"автор".decode("utf-8"): ls[0],
									"год".decode("utf-8"): ls[1],
									"жанр".decode("utf-8"): ls[2],
									"серия".decode("utf-8"): ls[3],
									"номер".decode("utf-8"): ls[4],
									"аннотация".decode("utf-8"): ls[6],
									"ссылка".decode("utf-8"): ls[7],
									"название".decode("utf-8"): ls[8],
									"number": ls[4],
									"cover_ext": ls[9],
									"cycle": ls[3]
												}
								if desc.has_key(a4):
									a4 = desc.get(a4, None)
								if a4 in ls:
									a5 = (list.pop(0)).lower()
									if a4 in (ls[1], ls[4]):
										if isNumber(a5):
											a5 = int(a5)
										else:
											a5 = ".0"
									elif a5 in ("clear", "отчистить".decode("utf-8")):
										a5 = None
									else:
										a5 = body[((body.lower()).find(a0) + len(a0)):].strip()
									if a5 != ".0":
										with database(self.BooksFile) as db:
											db("select * from books where id=?", (a2,))
											db_desc = db.fetchone()
											if db_desc:
												db("update books set %s=?, date=? where id=?" % (a4), (a5, time.asctime(), a2))
												db.commit()
												answer = AnsBase[4]
											else:
												answer = self.AnsBase[3]
									else:
										answer = AnsBase[30]
								else:
									answer = self.AnsBase[12]
							elif a3 in ("page", "страница".decode("utf-8")):
								with database(self.BooksFile) as db:
									db("select * from books where id=?", (a2,))
									db_desc = db.fetchone()
									if db_desc:
										db("select page from %s" % a2)
										lines = db.fetchall()
										llens = len(lines)
										a4 = (list.pop(0)).lower()
										if a4 in ("add", "добавить".decode("utf-8")):
											a5 = body[((body.lower()).find(a4) + len(a4)):].strip()
											if llens:
												line = (llens + 1)
											else:
												line = 1
											db("insert into %s values (?,?)" % (a2), (line, a5))
											db("update books set date=? where id=?", (time.asctime(), a2))
											db.commit()
											answer = AnsBase[4]
										elif a4 in ("delete", "удалить".decode("utf-8")):
											a5 = (list.pop(0)).lower()
											if list:
												a6 = list.pop(0)
												if isNumber(a6):
													a6 = int(a6)
													if a5 in ("before", "до".decode("utf-8")):
														if 0 < a6 < llens:
															page = itypes.Number()
															for Numb in xrange(a6, (llens + 1)):
																db("select data from %s where page=?" % (a2), (Numb,))
																data = db.fetchone()
																db("update %s set data=? where page=?" % (a2), (data[0], page.plus()))
															for Numb in xrange(page.plus(), (llens + 1)):
																db("delete from %s where page=?" % (a2), (Numb,))
															db("update books set date=? where id=?", (time.asctime(), a2))
															db.commit()
															answer = AnsBase[4]
														else:
															answer = self.AnsBase[13]
													elif a5 in ("only", "только".decode("utf-8")):
														if 0 < a6 < (llens + 1):
															for Numb in xrange(a6, (llens + 1)):
																db("select data from %s where page=?" % (a2), ((Numb + 1),))
																data = db.fetchone()
																db("update %s set data=? where page=?" % (a2), (data[0], Numb))
															db("delete from %s where page=?" % (a2), (llens,))
															db("update books set date=? where id=?", (time.asctime(), a2))
															db.commit()
															answer = AnsBase[4]
														else:
															answer = self.AnsBase[14]
													elif a5 in ("after", "после".decode("utf-8")):
														if 0 < a6 < (llens - 1):
															for Numb in xrange((a6 + 1), (llens + 1)):
																db("delete from %s where page=?" % (a2), (Numb,))
															db("update books set date=? where id=?", (time.asctime(), a2))
															db.commit()
															answer = AnsBase[4]
														else:
															answer = self.AnsBase[13]
													else:
														answer = AnsBase[2]
												else:
													answer = AnsBase[30]
											else:
												answer = AnsBase[2]
										elif isNumber(a4):
											if llens:
												a5 = body[((body.lower()).find(a4) + len(a4)):].strip()
												a4 = int(a4)
												if 0 < a4 < (llens + 1):
													db("update %s set data=? where page=?" % (a2), (a5, a4))
													db("update books set date=? where id=?", (time.asctime(), a2))
													db.commit()
													answer = AnsBase[4]
												else:
													answer = self.AnsBase[14]
											else:
												answer = self.AnsBase[7]
										else:
											answer = AnsBase[2]
									else:
										answer = self.AnsBase[3]
							else:
								answer = AnsBase[2]
						else:
							answer = self.AnsBase[15]
					else:
						answer = AnsBase[2]
				elif a1 in ("delete", "удалить".decode("utf-8")):
					a2 = self.getID(list.pop(0))
					if a2:
						with database(self.BooksFile) as db:
							db("select * from books where id=?", (a2,))
							db_desc = db.fetchone()
							if db_desc:
								db("drop table %s" % a2)
								db("delete from books where id=?", (a2,))
								db.commit()
								answer = AnsBase[4]
							else:
								answer = self.AnsBase[3]
					else:
						answer = self.AnsBase[15]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def init_books_base(self):
		if not os.path.isfile(self.BooksFile):
			with database(self.BooksFile) as db:
				db("create table books (id text, name text, author text, year integer, genre text, seq1 text, seq2 integer, c0 text, cover text, annotation text, link text, nick text, date text)")
				db.commit()
		if not os.path.isfile(self.ReadersFile):
			with database(self.ReadersFile) as db:
				db("create table readers (jid text, book text, page integer)")
				db.commit()

	commands = (
		(command_get_books, "books", 2,),
		(command_set_books, "library", 7,)
					)

	handlers = ((init_books_base, "00si"),)
