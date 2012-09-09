# coding: utf-8

#  BlackSmith mark.2
exp_name = "allweb" # /code.py v.x12
#  Id: 25~12a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

import htmlentitydefs, json

UserAgent = ("User-Agent", "%s/%s" % (ProdName[:10], CapsVer))

UserAgent_Moz = (UserAgent[0], "Mozilla/5.0 (X11; U; Linux i686; {0}; rv:1.7.12) Gecko/20050929".format(UserAgents.get(DefLANG, "en-US")))

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

def e_sb(co):
	co = co.groups()[0]
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
			Char = edefs.get(Char, "&%s;" % co)
	else:
		Char = edefs.get(co, "&%s;" % co)
	return Char

def sub_ehtmls(data):
	if data.count("&"):
		data = compile_ehtmls.sub(e_sb, data)
	return data

def decodeHTML(data):
	data = sub_desc(data, REP_desc)
	data = compile_st.sub("", data)
	data = sub_ehtmls(data)
	return data.strip()

def command_jc(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			cName = body.lower()
			if cName.count("@conf"):
				cName = (cName.split("@conf"))[0]
		else:
			cName = (source[1].split("@conf"))[0]
		Req = Web("http://jc.jabber.ru/search.html?", [("search", cName.encode("utf-8"))])
		try:
			data = Req.get_page(UserAgent)
		except:
			answer = AllwebAnsBase[0]
		else:
			comp = compile__("<li>((?:.|\s)+?)</li>", 16)
			list = comp.findall(data)
			if list:
				Number = itypes.Number()
				ls = []
				for line in list:
					line = line.strip()
					ls.append("%d) %s" % (Number.plus(), line))
				answer = (chr(10) + decodeHTML(str.join(chr(10)*2, ls)))
			else:
				answer = AllwebAnsBase[5]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

gCache = []

def command_google(ltype, source, body, disp):
	if body:
		if (chr(42) != body):
			Req = Web("http://ajax.googleapis.com/ajax/services/search/web?", [("v", "1.0"), ("q", body.encode("utf-8"))])
			try:
				data = Req.get_page(UserAgent)
			except:
				answer = AllwebAnsBase[0]
			else:
				try:
					data = json.loads(data)
				except:
					answer = AllwebAnsBase[1]
				else:
					data = data.get("responseData", {"results": []})
					list = data.get("results", [])
					if list:
						desc = list.pop(0)
						ls = []
						ls.append(desc.get("title", ""))
						ls.append(desc.get("content", ""))
						ls.append(desc.get("unescapedUrl", ""))
						answer = decodeHTML(str.join(chr(10), ls))
						if list:
							source_ = get_source(source[1], source[2])
							if source_:
								for ls in gCache:
									if ls[0] == source_:
										gCache.pop(gCache.index(ls))
										break
								Numb = (len(Clients.keys())*4)
								while len(gCache) >= Numb:
									gCache.pop(0)
								gCache.append((source_, list))
								answer += AllwebAnsBase[4] % len(list)
					else:
						answer = AllwebAnsBase[5]
		else:
			source_ = get_source(source[1], source[2])
			if source_:
				list = []
				for ls in gCache:
					if ls[0] == source_:
						list = gCache.pop(gCache.index(ls))[1]
						break
				if list:
					desc = list.pop(0)
					ls = []
					ls.append(desc.get("title", ""))
					ls.append(desc.get("content", ""))
					ls.append(desc.get("unescapedUrl", ""))
					answer = decodeHTML(str.join(chr(10), ls))
					if list:
						gCache.append((source_, list))
						answer += AllwebAnsBase[4] % len(list)
				else:
					answer = AllwebAnsBase[2]
			else:
				answer = AllwebAnsBase[3]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_kino(ltype, source, body, disp):
	if body:
		ls = body.split()
		c1st = (ls.pop(0)).lower()
		c3op = "СЗоР"
	#	if c1st in ("top250", "топ250".decode("utf-8")):
	#		if ls:
	#			limit = exec_(int, (ls.pop(0),))
	#			if limit <= 5:
	#				limit = 5
	#		else:
	#			limit = None
	#		Req = Web("http://www.kinopoisk.ru/level/20/")
	#		try:
	#			data = Req.get_page(UserAgent_Moz)
	#		except:
	#			answer = AllwebAnsBase[0]
	#		else:
	#			data = data.decode("cp1251")
	#			list = get_text(data, "<table.+?>", "</table>")
	#			if list:
	#				comp = compile__('<a href="/level/1/film/\d+?/" class="all">(.+?)</a>.+' \
	#								'?<a href="/level/83/film/\d+?/" class="continue">(.+?)</a>.+' \
	#								'?<div.+?>(.+?)</div>', 16)
	#				list = comp.findall(list)
	#			if list:
	#				Number = itypes.Number()
	#				ls = ["\n[#] [Name, Year] [Rating] (Votes)"]
	#				for Name, Numb, Numb_ in list:
	#					ls.append("%d) %s - %s (%s)" % (Number.plus(), sub_ehtmls(Name), Numb, sub_desc(Numb, ["&nbsp;"])))
	#					if limit and limit <= Number._int():
	#						break
	#				if not limit or limit > 25:
	#					if ltype == Types[1]:
	#						Answer(AnsBase[11], ltype, source, disp)
	#					Top250 = str.join(chr(10), ls)
	#					Msend(source[0], Top250, disp)
	#				else:
	#					answer = str.join(chr(10), ls)
	#			elif data.count(c3op):
	#				answer = AllwebAnsBase[-1]
	#			else:
	#				answer = AllwebAnsBase[1]
		if isNumber(body):
			Req = Web("http://m.kinopoisk.ru/movie/%s" % (body))
			try:
				data = Req.get_page(UserAgent_Moz)
			except:
				answer = AllwebAnsBase[0]
			else:
				data = data.decode("cp1251")
				relt = get_text(data, "<p class=\"title\">", "</div>")
				if relt:
					relt = decodeHTML(relt)
					ls = ["\->"]
					for line in relt.splitlines():
						line = line.strip()
						if line:
							if line[0].islower():
								line = "{1}{0}".format(line[1:], line[0].upper())
							ls.append(line)
					answer = str.join(chr(10), ls)
				elif data.count(c3op):
					answer = AllwebAnsBase[-1]
				else:
					answer = AllwebAnsBase[5]
		else:
			Req = (body if chr(42) != c1st else body[2:].strip())
			Req = Req.encode("cp1251")
			Req = Web("http://m.kinopoisk.ru/search/%s" % Web.One.quote_plus(Req))
			try:
				data = Req.get_page(UserAgent_Moz)
			except:
				answer = AllwebAnsBase[0]
			else:
				data = data.decode("cp1251")
				comp = compile__("<a href=\"http://m.kinopoisk.ru/movie/(\d+?)/\">(.+?)</a>")
				list = comp.findall(data)
				if list:
					Number = itypes.Number()
					ls = ["\n[#] [Name, Year] (#id)"]
					for Numb, Name in list:
						ls.append("%d) %s (#%s)" % (Number.plus(), sub_ehtmls(Name), Numb))
					answer = str.join(chr(10), ls)
				elif data.count(c3op):
					answer = AllwebAnsBase[-1]
				else:
					answer = AllwebAnsBase[5]
	else:
		answer = AnsBase[1]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_imdb(ltype, source, body, disp):
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
				data = Req.get_page(UserAgent_Moz)
			except:
				answer = AllwebAnsBase[0]
			else:
				list = get_text(data, '<div id="main">', "</div>")
				if list:
					comp = compile__('<td align="center">%s((?:\d+\.\d)+|\d+?)</font></td><td>%s<a href="/title/tt\d+?/">' \
									'(.+?)</a>(.+?)</font></td><td align="right">%s(.+?)</font>' \
									'</td>' % (('<font face="Arial, Helvetica, sans-serif" size="-1">',)*3), 16)
					list = comp.findall(list)
				if list:
					Number = itypes.Number()
					ls = ["\n[#] [Name, Year] [Rating] (Votes)"]
					for Numb, Name, Year, Numb_ in list:
						ls.append("%s) %s %s - %s (%s)" % (Number.plus(), sub_ehtmls(Name), Year.strip(), Numb, Numb_))
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
					answer = AllwebAnsBase[1]
		elif isNumber(body):
			Req = Web("http://www.imdb.com/title/tt%s/" % (body))
			try:
				data = Req.get_page(UserAgent_Moz)
			except:
				answer = AllwebAnsBase[0]
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
							data = decodeHTML(ln)
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
						answer = AllwebAnsBase[1]
				else:
					answer = AllwebAnsBase[1]
		else:
			Req = (body if chr(42) != c1st else body[2:].strip())
			Req = Req.encode("utf-8")
			Req = Web("http://www.imdb.com/find?", [("s", "tt"), ("q", Req)])
			try:
				data = Req.get_page(UserAgent_Moz)
			except:
				answer = AllwebAnsBase[0]
			else:
				list = get_text(data, "<table>", "</table>")
				if list:
					comp = compile__("/find-title-\d+?/title_.+?/images/b.gif\?link=/title/tt(\d+?)/';\">(.+?)</a> (.+?)<", 16)
					list = comp.findall(list)
				if list:
					Number = itypes.Number()
					ls = ["\n[#] [Name, Year] (#id)"]
					for Numb, Name, Year in list:
						ls.append("%d) %s %s (#%s)" % (Number.plus(), sub_ehtmls(Name), Year.strip(), Numb))
					answer = str.join(chr(10), ls)
				else:
					answer = AllwebAnsBase[5]
	else:
		answer = AnsBase[1]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_python(ltype, source, body, disp):
	Req = Web("http://python.org/")
	try:
		data = Req.get_page(UserAgent)
	except:
		answer = AllwebAnsBase[0]
	else:
		data = data.decode("koi8-r")
		data = get_text(data, "<h2 class=\"news\">", "</div>")
		if data:
			data = decodeHTML(data)
			ls = []
			for line in data.splitlines():
				if line.strip():
					ls.append(line)
			answer = str.join(chr(10), ls)
		else:
			answer = AllwebAnsBase[1]
	Answer(answer, ltype, source, disp)

def command_currency(ltype, source, body, disp):
	if body:
		ls = body.split()
		Code = (ls.pop(0)).lower()
		if Code in ("code", "аббревиатура".decode("utf-8")):
			if ls:
				Code = (ls.pop(0)).upper()
				if Currency_desc.has_key(Code):
					answer = Currency_desc[Code].decode("utf-8")
				else:
					answer = AllwebAnsBase[1]
			else:
				answer = AnsBase[2]
		elif Code in ("list", "список".decode("utf-8")):
			if ltype == Types[1]:
				Answer(AnsBase[11], ltype, source, disp)
			Curls = ["\->"] + ["%s: %s" % desc for desc in sorted(Currency_desc.items())]
			Msend(source[0], str.join(chr(10), Curls), disp)
		elif Code in ("calc", "перевести".decode("utf-8")):
			if len(ls) >= 2:
				Number = ls.pop(0)
				if isNumber(Number) and ls[0].isalpha():
					Number = int(Number)
					Code = (ls.pop(0)).upper()
					if (Code == "RUB"):
						answer = "%d %s" % (Number, Code)
					elif Currency_desc.has_key(Code):
						Req = Web("http://www.cbr.ru/scripts/XML_daily.asp")
						try:
							data = Req.get_page(UserAgent)
						except:
							answer = AllwebAnsBase[0]
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
								answer = AllwebAnsBase[1]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				answer = AnsBase[2]
		elif (Code != "rub") and Code.isalpha():
			Code = Code.upper()
			if Currency_desc.has_key(Code):
				Req = Web("http://www.cbr.ru/scripts/XML_daily.asp")
				try:
					data = Req.get_page(UserAgent)
				except:
					answer = AllwebAnsBase[0]
				else:
					data = data.decode("cp1251")
					comp = compile__("<CharCode>%s</CharCode>\s+?<Nominal>(.+?)</Nominal>\s+?<Name>.+?</Name>\s+?<Value>(.+?)</Value>" % (Code), 16)
					data = comp.search(data)
					if data:
						No, Numb = data.groups()
						answer = "%s/RUB - %s/%s" % (Code, No, Numb)
					else:
						answer = AllwebAnsBase[1]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[2]
	else:
		Req = Web("http://www.cbr.ru/scripts/XML_daily.asp")
		try:
			data = Req.get_page(UserAgent)
		except:
			answer = AllwebAnsBase[0]
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
				answer = AllwebAnsBase[1]
	if locals().has_key(Types[12]):
		Answer(answer, ltype, source, disp)

def command_jquote(ltype, source, body, disp):
	if body and isNumber(body):
		Req = Web("http://jabber-quotes.ru/api/read/?id=%d" % int(body))
	else:
		Req = Web("http://jabber-quotes.ru/api/read/?id=random")
	try:
		data = Req.get_page(UserAgent)
	except:
		answer = AllwebAnsBase[0]
	else:
		data = data.decode("utf-8")
		comp = compile__("<id>(\d+?)</id>\s+?<author>(.+?)</author>\s+?<quote>(.+?)</quote>", 16)
		data = comp.search(data)
		if data:
			Numb, Name, Quote = data.groups()
			lt = chr(10)*3
			answer = decodeHTML("Quote: #%s | by %s\n%s" % (Numb, Name, Quote))
			while answer.count(lt):
				answer = answer.replace(lt, lt[:2])
		else:
			answer = AllwebAnsBase[1]
	Answer(answer, ltype, source, disp)

def command_chuck(ltype, source, body, disp):
	if body and isNumber(body):
		Req = Web("http://chucknorrisfacts.ru/quote/%d" % int(body))
	else:
		Req = Web("http://chucknorrisfacts.ru/random")
	try:
		data = Req.get_page(UserAgent)
	except:
		answer = AllwebAnsBase[0]
	else:
		data = data.decode("cp1251")
		comp = compile__("<a href=/quote/(\d+?)>.+?<blockquote>(.+?)</blockquote>", 16)
		data = comp.search(data)
		if data:
			answer = decodeHTML("Fact: #%s\n%s" % data.groups())
		else:
			answer = AllwebAnsBase[1]
	Answer(answer, ltype, source, disp)

def command_gismeteo(ltype, source, body, disp):
	if body:
		ls = body.split()
		Numb = ls.pop(0)
		if ls and isNumber(Numb):
			City = body[(body.find(Numb) + len(Numb) + 1):].strip()
			Numb = int(Numb)
		else:
			City = body
			Numb = None
		if -1 < Numb < 13 or not Numb:
			Req = Web("http://m.gismeteo.ru/citysearch/by_name/?", [("gis_search", City.encode("utf-8"))])
			try:
				data = Req.get_page(UserAgent)
			except:
				answer = AllwebAnsBase[0]
			else:
				data = data.decode("utf-8")
				data = get_text(data, "<a href=\"/weather/", "/(1/)*?\">", "\d+")
				if data:
					if Numb != None:
						data = str.join(chr(47), [data, str(Numb) if Numb != 0 else "weekly"])
					Req = Web("http://m.gismeteo.ru/weather/%s/" % data)
					try:
						data = Req.get_page(UserAgent)
					except:
						answer = AllwebAnsBase[0]
					else:
						data = data.decode("utf-8")
						mark = get_text(data, "<th colspan=\"2\">", "</th>")
						if Numb != 0:
							comp = compile__('<tr class="tbody">\s+?<th.*?>(.+?)</th>\s+?<td.+?/></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>\s+?</tr>\s+?<tr class="dl">\s+?<td>&nbsp;</td>\s+?<td class="clpersp"><p>(.+?)</p></td>\s+?</tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl bottom"><td class="left">(.+?)</td><td>(.+?)</td></tr>', 16)
							list = comp.findall(data)
							if list:
								ls = [(decodeHTML(mark) if mark else "\->")]
								for data in list:
									ls.append("{0}:\n\t{2}, {1}\n\t{3} {4}\n\t{5} {6}\n\t{7} {8}".format(*data))
								ls.append(AllwebAnsBase[-2])
								answer = decodeHTML(str.join(chr(10), ls))
							else:
								answer = AllwebAnsBase[1]
						else:
							comp = compile__('<tr class="tbody">\s+?<td class="date" colspan="3"><a.+?>(.+?)</a></td>\s+?</tr>\s+?<tr>\s+?<td rowspan="2"><a.+?/></a></td>\s+?<td class="clpersp"><p>(.+?)</p></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>', 16)
							list = comp.findall(data)
							if list:
								ls = [(decodeHTML(mark) if mark else "\->")]
								for data in list:
									ls.append("%s:\n\t%s, %s" % (data))
								ls.append(AllwebAnsBase[-2])
								answer = decodeHTML(str.join(chr(10), ls))
							else:
								answer = AllwebAnsBase[1]
				else:
					answer = AllwebAnsBase[5]
		else:
			answer = AnsBase[2]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([sub_ehtmls, e_sb, decodeHTML, command_jc, command_google, command_imdb, command_python])
expansions[exp_name].ls.extend([
						htmlentitydefs.__name__,
						json.__name__,
						"AllwebAnsBase",
						"UserAgent",
						"UserAgent_Moz",
						"edefs",
						"REP_desc",
						"XML_ls",
						"UserAgents",
						"compile_st",
						"compile_ehtmls",
						"gCache"
								])

command_handler(command_jc, {"RU": "рейтинг", "EN": "jc"}, 2, exp_name)
command_handler(command_google, {"RU": "гугл", "EN": "google"}, 2, exp_name)

if DefLANG in ("RU", "UA"):

	expansions[exp_name].funcs_add([command_kino, command_currency, command_jquote, command_chuck, command_gismeteo])
	expansions[exp_name].ls.extend(["Currency_desc"])

	command_handler(command_kino, {"RU": "кино", "EN": "kino"}, 2, exp_name)
	command_handler(command_currency, {"RU": "валюты", "EN": "currency"}, 2, exp_name)
	command_handler(command_jquote, {"RU": "цитата", "EN": "jquote"}, 2, exp_name)
	command_handler(command_chuck, {"RU": "чак", "EN": "chuck"}, 2, exp_name)
	command_handler(command_gismeteo, {"RU": "погода", "EN": "gismeteo"}, 2, exp_name)
else:
	del command_kino, command_currency, command_jquote, command_chuck, command_gismeteo

command_handler(command_imdb, {"RU": "imdb", "EN": "imdb"}, 2, exp_name)
command_handler(command_python, {"RU": "питон", "EN": "python"}, 2, exp_name)
