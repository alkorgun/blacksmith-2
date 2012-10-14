# coding: utf-8

#  BlackSmith mark.2
exp_name = "allweb" # /code.py v.x14
#  Id: 25~14b
#  Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	UserAgents = UserAgents

	import htmlentitydefs, json

	UserAgent = ("User-Agent", "%s/%s" % (ProdName[:10], CapsVer))

	UserAgent_Moz = (UserAgent[0], "Mozilla/5.0 (Windows NT 6.1; WOW64; {0}) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1".format(UserAgents.get(DefLANG, "en-US")))

	edefs = dict()

	for Name, Numb in htmlentitydefs.name2codepoint.iteritems():
		edefs[Name] = unichr(Numb)

	del Name, Numb

	Web.Opener.addheaders = [UserAgent_Moz]

	REP_desc = {
		"<br>": chr(10),
		"<br />": chr(10)
					}

	XML_ls = [
		("&lt;", "<"),
		("&gt;", ">"),
		("&quot;", '"'),
		("&apos;", "'"),
		("&amp;", "&")
					]

	compile_st = compile__("<[^<>]+?>")
	compile_ehtmls = compile__("&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")

	def sub_ehtmls(self, data):
		if data.count("&"):

			def e_sb(co):
				co = co.group(1)
				if co.startswith("#"):
					if chr(120) == co[1].lower():
						Char, c06 = co[2:], 16
					else:
						Char, c06 = co[1:], 10
					try:
						Numb = int(Char, c06)
						assert (-1 < Numb < 65535)
						Char = unichr(Numb)
					except:
						Char = self.edefs.get(Char, "&%s;" % co)
				else:
					Char = self.edefs.get(co, "&%s;" % co)
				return Char

			data = self.compile_ehtmls.sub(e_sb, data)
		return data

	def decodeHTML(self, data):
		data = sub_desc(data, self.REP_desc)
		data = self.compile_st.sub("", data)
		data = self.sub_ehtmls(data)
		return data.strip()

	def command_jc(self, ltype, source, body, disp):
		if Chats.has_key(source[1]):
			if body:
				cName = body.lower()
				if cName.count("@conf"):
					cName = (cName.split("@conf"))[0]
			else:
				cName = (source[1].split("@conf"))[0]
			Req = Web("http://jc.jabber.ru/search.html?", [("search", cName.encode("utf-8"))])
			try:
				data = Req.get_page(self.UserAgent)
			except:
				answer = self.AnsBase[0]
			else:
				comp = compile__("<li>((?:.|\s)+?)</li>", 16)
				list = comp.findall(data)
				if list:
					Number = itypes.Number()
					ls = []
					for line in list:
						line = line.strip()
						ls.append("%d) %s" % (Number.plus(), line))
					answer = (chr(10) + self.decodeHTML(str.join(chr(10)*2, ls)))
				else:
					answer = self.AnsBase[5]
		else:
			answer = AnsBase[0]
		Answer(answer, ltype, source, disp)

	gCache = []

	def command_google(self, ltype, source, body, disp):
		if body:
			if (chr(42) != body):
				Req = Web("http://ajax.googleapis.com/ajax/services/search/web?", [("v", "1.0"), ("q", body.encode("utf-8"))])
				try:
					data = Req.get_page(self.UserAgent)
				except:
					answer = self.AnsBase[0]
				else:
					try:
						data = self.json.loads(data)
					except:
						answer = self.AnsBase[1]
					else:
						data = data.get("responseData", {"results": []})
						list = data.get("results", [])
						if list:
							desc = list.pop(0)
							ls = []
							ls.append(desc.get("title", ""))
							ls.append(desc.get("content", ""))
							ls.append(desc.get("unescapedUrl", ""))
							answer = self.decodeHTML(str.join(chr(10), ls))
							if list:
								source_ = get_source(source[1], source[2])
								if source_:
									for ls in self.gCache:
										if ls[0] == source_:
											self.gCache.pop(self.gCache.index(ls))
											break
									Numb = (len(Clients.keys())*4)
									while len(self.gCache) >= Numb:
										self.gCache.pop(0)
									self.gCache.append((source_, list))
									answer += self.AnsBase[4] % len(list)
						else:
							answer = self.AnsBase[5]
			else:
				source_ = get_source(source[1], source[2])
				if source_:
					list = []
					for ls in self.gCache:
						if ls[0] == source_:
							list = self.gCache.pop(self.gCache.index(ls))[1]
							break
					if list:
						desc = list.pop(0)
						ls = []
						ls.append(desc.get("title", ""))
						ls.append(desc.get("content", ""))
						ls.append(desc.get("unescapedUrl", ""))
						answer = self.decodeHTML(str.join(chr(10), ls))
						if list:
							self.gCache.append((source_, list))
							answer += self.AnsBase[4] % len(list)
					else:
						answer = self.AnsBase[2]
				else:
					answer = self.AnsBase[3]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_kino(self, ltype, source, body, disp):
		if body:
			ls = body.split()
			c1st = (ls.pop(0)).lower()
			c3op = "СЗоР"
			if c1st in ("top250", "топ250".decode("utf-8")):
				if ls:
					limit = exec_(int, (ls.pop(0),))
					if limit <= 5:
						limit = 5
				else:
					limit = None
				Req = Web("http://www.kinopoisk.ru/level/20/")
				try:
					data = Req.get_page(self.UserAgent_Moz)
				except:
					answer = self.AnsBase[0]
				else:
					data = data.decode("cp1251")
					list = get_text(data, "<tr height=25>", "</table>")
					if list:
						comp = compile__('<a href="/film/\d+?/" class="all">(.+?)</a>(?:.|\s)+' \
										'?<a href="/film/\d+?/votes/" class="continue">(.+?)</a> <span.*?>(.+?)</span>', 16)
						list = comp.findall(list)
					if list:
						Number = itypes.Number()
						ls = ["\n[#] [Name, Year] [Rating] (Votes)"]
						for Name, Numb, Numb_ in list:
							ls.append("%d) %s - %s (%s)" % (Number.plus(), self.sub_ehtmls(Name), Numb, sub_desc(Numb, ["&nbsp;"])))
							if limit and limit <= Number._int():
								break
						if not limit or limit > 25:
							if ltype == Types[1]:
								Answer(AnsBase[11], ltype, source, disp)
							Top250 = str.join(chr(10), ls)
							Msend(source[0], Top250, disp)
						else:
							answer = str.join(chr(10), ls)
					elif data.count(c3op):
						answer = self.AnsBase[-1]
					else:
						answer = self.AnsBase[1]
			elif isNumber(body):
				Req = Web("http://m.kinopoisk.ru/movie/%s" % (body))
				try:
					data = Req.get_page(self.UserAgent_Moz)
				except:
					answer = self.AnsBase[0]
				else:
					data = data.decode("cp1251")
					rslt = get_text(data, "<p class=\"title\">", "</div>")
					if rslt:
						rslt = self.decodeHTML(rslt)
						ls = ["\->"]
						for line in rslt.splitlines():
							line = line.strip()
							if line:
								if line[0].islower():
									line = "{1}{0}".format(line[1:], line[0].upper())
								ls.append(line)
						answer = str.join(chr(10), ls)
					elif data.count(c3op):
						answer = self.AnsBase[-1]
					else:
						answer = self.AnsBase[5]
			else:
				Req = (body if chr(42) != c1st else body[2:].strip())
				Req = Req.encode("cp1251")
				Req = Web("http://m.kinopoisk.ru/search/%s" % Web.One.quote_plus(Req))
				try:
					data = Req.get_page(self.UserAgent_Moz)
				except:
					answer = self.AnsBase[0]
				else:
					data = data.decode("cp1251")
					comp = compile__("<a href=\"http://m.kinopoisk.ru/movie/(\d+?)/\">(.+?)</a>")
					list = comp.findall(data)
					if list:
						Number = itypes.Number()
						ls = ["\n[#] [Name, Year] (#id)"]
						for Numb, Name in list:
							ls.append("%d) %s (#%s)" % (Number.plus(), self.sub_ehtmls(Name), Numb))
						answer = str.join(chr(10), ls)
					elif data.count(c3op):
						answer = self.AnsBase[-1]
					else:
						answer = self.AnsBase[5]
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_imdb(self, ltype, source, body, disp):
		if body:
			ls = body.split()
			c1st = (ls.pop(0)).lower()
			if c1st in ("top250", "топ250".decode("utf-8")):
				if ls:
					limit = exec_(int, (ls.pop(0),))
					if limit <= 5:
						limit = 5
				else:
					limit = None
				Req = Web("http://www.imdb.com/chart/top")
				try:
					data = Req.get_page(self.UserAgent_Moz)
				except:
					answer = self.AnsBase[0]
				else:
					list = get_text(data, '<div id="main">', "</div>")
					if list:
						comp = compile__('<td align="center">%s((?:\d\.\d)+|\d+?)</font></td><td>%s<a href="/title/tt\d+?/">' \
										'(.+?)</a>(.+?)</font></td><td align="right">%s(.+?)</font>' \
										'</td>' % (('<font face="Arial, Helvetica, sans-serif" size="-1">',)*3), 16)
						list = comp.findall(list)
					if list:
						Number = itypes.Number()
						ls = ["\n[#] [Name, Year] [Rating] (Votes)"]
						for Numb, Name, Year, Numb_ in list:
							ls.append("%s) %s %s - %s (%s)" % (Number.plus(), self.sub_ehtmls(Name), Year.strip(), Numb, Numb_))
							if limit and limit <= Number._int():
								break
						if not limit or limit > 25:
							if ltype == Types[1]:
								Answer(AnsBase[11], ltype, source, disp)
							Top250 = str.join(chr(10), ls)
							Msend(source[0], Top250, disp)
						else:
							answer = str.join(chr(10), ls)
					else:
						answer = self.AnsBase[1]
			elif isNumber(body):
				Req = Web("http://www.imdb.com/title/tt%s/" % (body))
				try:
					data = Req.get_page(self.UserAgent_Moz)
				except:
					answer = self.AnsBase[0]
				else:
					Name = get_text(data, '<h1 class="header" itemprop="name">', "<span>")
					if Name:
						ls = ["\->"]
						Year = get_text(data, '<a href="/year/\d+?/">', "</a>", "\d+")
						if Year:
							ls.append("%s (%s)" % (Name, Year))
						else:
							ls.append(Name)
						desc = get_text(data, '<p itemprop="description">', "</p>")
						if desc:
							ls.append(desc)
							desc = ls.index(desc)
						Numb = get_text(data, '<span itemprop="ratingValue">', "</span>")
						UsrV = get_text(data, '<span itemprop="ratingCount">', "</span>")
						if Numb:
							if UsrV:
								Numb = "%s (Votes: %s)" % (Numb, UsrV)
							ls.append("Raiting: %s" % Numb)
						Ttls = (("Director", "\s*Director:\s*"),
								("Stars", "\s*Stars:\s*"),
								("Writers", "\s*Writers:\s*"), ("Writer", "\s*Writer:\s*"))
						for Title in Ttls:
							list = get_text(data, '<h4 class="inline">%s</h4>' % Title[1], "</div>")
							if list:
								comp = compile__(">(.+?)</a>")
								list = comp.findall(list)
								if list:
									ls.append("%s: %s" % (Title[0], str.join(", ", list)))
						if len(ls) >= 2:
							for ln in ls:
								data = self.decodeHTML(ln)
								lines = []
								for line in data.splitlines():
									line = line.strip()
									if line:
										lines.append(line)
								li = ls.index(ln)
								if li == desc:
									lines.append(chr(10))
									lines.insert(0, chr(10))
								ls[li] = str.join(chr(10), lines)
							answer = str.join(chr(10), ls)
						else:
							answer = self.AnsBase[1]
					else:
						answer = self.AnsBase[1]
			else:
				Req = (body if chr(42) != c1st else body[2:].strip())
				Req = Req.encode("utf-8")
				Req = Web("http://www.imdb.com/find?", [("s", "tt"), ("q", Req)])
				try:
					data = Req.get_page(self.UserAgent_Moz)
				except:
					answer = self.AnsBase[0]
				else:
					list = get_text(data, "<table>", "</table>")
					if list:
						comp = compile__("/find-title-\d+?/title_.+?/images/b.gif\?link=/title/tt(\d+?)/';\">(.+?)</a> (.+?)<", 16)
						list = comp.findall(list)
					if list:
						Number = itypes.Number()
						ls = ["\n[#] [Name, Year] (#id)"]
						for Numb, Name, Year in list:
							ls.append("%d) %s %s (#%s)" % (Number.plus(), self.sub_ehtmls(Name), Year.strip(), Numb))
						answer = str.join(chr(10), ls)
					else:
						answer = self.AnsBase[5]
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_python(self, ltype, source, body, disp):
		Req = Web("http://python.org/")
		try:
			data = Req.get_page(self.UserAgent)
		except:
			answer = self.AnsBase[0]
		else:
			data = data.decode("koi8-r")
			data = get_text(data, "<h2 class=\"news\">", "</div>")
			if data:
				data = self.decodeHTML(data)
				ls = []
				for line in data.splitlines():
					if line.strip():
						ls.append(line)
				answer = str.join(chr(10), ls)
			else:
				answer = self.AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_currency(self, ltype, source, body, disp):
		if body:
			ls = body.split()
			Code = (ls.pop(0)).lower()
			if Code in ("code", "аббревиатура".decode("utf-8")):
				if ls:
					Code = (ls.pop(0)).upper()
					if self.Currency_desc.has_key(Code):
						answer = self.Currency_desc[Code].decode("utf-8")
					else:
						answer = self.AnsBase[1]
				else:
					answer = AnsBase[2]
			elif Code in ("list", "список".decode("utf-8")):
				if ltype == Types[1]:
					Answer(AnsBase[11], ltype, source, disp)
				Curls = ["\->"] + ["%s: %s" % desc for desc in sorted(self.Currency_desc.items())]
				Msend(source[0], str.join(chr(10), Curls), disp)
			elif Code in ("calc", "перевести".decode("utf-8")):
				if len(ls) >= 2:
					Number = ls.pop(0)
					if isNumber(Number) and ls[0].isalpha():
						Number = int(Number)
						Code = (ls.pop(0)).upper()
						if (Code == "RUB"):
							answer = "%d %s" % (Number, Code)
						elif self.Currency_desc.has_key(Code):
							Req = Web("http://www.cbr.ru/scripts/XML_daily.asp")
							try:
								data = Req.get_page(self.UserAgent)
							except:
								answer = self.AnsBase[0]
							else:
								data = data.decode("cp1251")
								comp = compile__("<CharCode>%s</CharCode>\s+?<Nominal>(.+?)</Nominal>\s+?<Name>.+?</Name>\s+?<Value>(.+?)</Value>" % (Code), 16)
								data = comp.search(data)
								if data:
									No, Numb = data.groups()
									Numb = Numb.replace(chr(44), chr(46))
									No = No.replace(chr(44), chr(46))
									try:
										Numb = (Number*(float(Numb)/float(No)))
									except:
										answer = AnsBase[7]
									else:
										answer = "%.2f RUB" % (Numb)
								else:
									answer = self.AnsBase[1]
						else:
							answer = AnsBase[2]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			elif (Code != "rub") and Code.isalpha():
				Code = Code.upper()
				if self.Currency_desc.has_key(Code):
					Req = Web("http://www.cbr.ru/scripts/XML_daily.asp")
					try:
						data = Req.get_page(self.UserAgent)
					except:
						answer = self.AnsBase[0]
					else:
						data = data.decode("cp1251")
						comp = compile__("<CharCode>%s</CharCode>\s+?<Nominal>(.+?)</Nominal>\s+?<Name>.+?</Name>\s+?<Value>(.+?)</Value>" % (Code), 16)
						data = comp.search(data)
						if data:
							No, Numb = data.groups()
							answer = "%s/RUB - %s/%s" % (Code, No, Numb)
						else:
							answer = self.AnsBase[1]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		else:
			Req = Web("http://www.cbr.ru/scripts/XML_daily.asp")
			try:
				data = Req.get_page(self.UserAgent)
			except:
				answer = self.AnsBase[0]
			else:
				data = data.decode("cp1251")
				comp = compile__("<CharCode>(.+?)</CharCode>\s+?<Nominal>(.+?)</Nominal>\s+?<Name>.+?</Name>\s+?<Value>(.+?)</Value>", 16)
				list = comp.findall(data)
				if list:
					ls, Number = ["\->"], itypes.Number()
					for Code, No, Numb in sorted(list):
						ls.append("%d) %s/RUB - %s/%s" % (Number.plus(), Code, No, Numb))
					if ltype == Types[1]:
						Answer(AnsBase[11], ltype, source, disp)
					Curls = str.join(chr(10), ls)
					Msend(source[0], Curls, disp)
				else:
					answer = self.AnsBase[1]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def command_jquote(self, ltype, source, body, disp):
		if body and isNumber(body):
			Req = Web("http://jabber-quotes.ru/api/read/?id=%d" % int(body))
		else:
			Req = Web("http://jabber-quotes.ru/api/read/?id=random")
		try:
			data = Req.get_page(self.UserAgent)
		except:
			answer = self.AnsBase[0]
		else:
			data = data.decode("utf-8")
			comp = compile__("<id>(\d+?)</id>\s+?<author>(.+?)</author>\s+?<quote>(.+?)</quote>", 16)
			data = comp.search(data)
			if data:
				Numb, Name, Quote = data.groups()
				lt = chr(10)*3
				answer = self.decodeHTML("Quote: #%s | by %s\n%s" % (Numb, Name, Quote))
				while answer.count(lt):
					answer = answer.replace(lt, lt[:2])
			else:
				answer = self.AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_chuck(self, ltype, source, body, disp):
		if body and isNumber(body):
			Req = Web("http://chucknorrisfacts.ru/quote/%d" % int(body))
		else:
			Req = Web("http://chucknorrisfacts.ru/random")
		try:
			data = Req.get_page(self.UserAgent)
		except:
			answer = self.AnsBase[0]
		else:
			data = data.decode("cp1251")
			comp = compile__("<a href=/quote/(\d+?)>.+?<blockquote>(.+?)</blockquote>", 16)
			data = comp.search(data)
			if data:
				answer = self.decodeHTML("Fact: #%s\n%s" % data.groups())
			else:
				answer = self.AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_ithappens(self, ltype, source, body, disp):
		if body and isNumber(body):
			Req = Web("http://ithappens.ru/story/%d" % int(body))
		else:
			Req = Web("http://ithappens.ru/random")
		try:
			data = Req.get_page(self.UserAgent)
		except:
			answer = self.AnsBase[0]
		else:
			data = data.decode("cp1251")
			data = get_text(data, "<div class=\"text\">", "</p>")
			if data:
				answer = self.decodeHTML(sub_desc(data, {"<p class=\"date\">": chr(32)}))
			else:
				answer = self.AnsBase[1]
		Answer(answer, ltype, source, disp)

	def command_gismeteo(self, ltype, source, body, disp):
		if body:
			ls = body.split()
			Numb = ls.pop(0)
			if ls and isNumber(Numb):
				City = body[(body.find(Numb) + len(Numb)):].strip()
				Numb = int(Numb)
			else:
				City = body
				Numb = None
			if -1 < Numb < 13 or not Numb:
				Req = Web("http://m.gismeteo.ru/citysearch/by_name/?", [("gis_search", City.encode("utf-8"))])
				try:
					data = Req.get_page(self.UserAgent)
				except:
					answer = self.AnsBase[0]
				else:
					data = data.decode("utf-8")
					data = get_text(data, "<a href=\"/weather/", "/(1/)*?\">", "\d+")
					if data:
						if Numb != None:
							data = str.join(chr(47), [data, str(Numb) if Numb != 0 else "weekly"])
						Req = Web("http://m.gismeteo.ru/weather/%s/" % data)
						try:
							data = Req.get_page(self.UserAgent)
						except:
							answer = self.AnsBase[0]
						else:
							data = data.decode("utf-8")
							mark = get_text(data, "<th colspan=\"2\">", "</th>")
							if Numb != 0:
								comp = compile__('<tr class="tbody">\s+?<th.*?>(.+?)</th>\s+?<td.+?/></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>\s+?</tr>\s+?<tr class="dl">\s+?<td>&nbsp;</td>\s+?<td class="clpersp"><p>(.+?)</p></td>\s+?</tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl bottom"><td class="left">(.+?)</td><td>(.+?)</td></tr>', 16)
								list = comp.findall(data)
								if list:
									ls = [(self.decodeHTML(mark) if mark else "\->")]
									for data in list:
										ls.append("{0}:\n\t{2}, {1}\n\t{3} {4}\n\t{5} {6}\n\t{7} {8}".format(*data))
									ls.append(self.AnsBase[-2])
									answer = self.decodeHTML(str.join(chr(10), ls))
								else:
									answer = self.AnsBase[1]
							else:
								comp = compile__('<tr class="tbody">\s+?<td class="date" colspan="3"><a.+?>(.+?)</a></td>\s+?</tr>\s+?<tr>\s+?<td rowspan="2"><a.+?/></a></td>\s+?<td class="clpersp"><p>(.+?)</p></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>', 16)
								list = comp.findall(data)
								if list:
									ls = [(self.decodeHTML(mark) if mark else "\->")]
									for data in list:
										ls.append("%s:\n\t%s, %s" % (data))
									ls.append(self.AnsBase[-2])
									answer = self.decodeHTML(str.join(chr(10), ls))
								else:
									answer = self.AnsBase[1]
					else:
						answer = self.AnsBase[5]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, ltype, source, disp)

	commands = (
		(command_jc, "jc", 2,),
		(command_google, "google", 2,),
		(command_imdb, "imdb", 2,),
		(command_python, "python", 2,)
					)

	if DefLANG in ("RU", "UA"):
		commands = commands.__add__((
			(command_kino, "kino", 2,),
			(command_currency, "currency", 2,),
			(command_jquote, "jquote", 2,),
			(command_chuck, "chuck", 2,),
			(command_ithappens, "ithappens", 2,),
			(command_gismeteo, "gismeteo", 2,)
						))
		Currency_desc = Currency_desc
	else:
		del command_kino, command_currency, command_jquote, command_chuck, command_ithappens, command_gismeteo

if DefLANG in ("RU", "UA"):
	del Currency_desc
del UserAgents
