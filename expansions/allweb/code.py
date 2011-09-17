# coding: utf-8

#  BlackSmith mark.2
exp_name = "allweb" # /code.py v.x5
#  Id: 25~5a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

import htmlentitydefs, json

UserAgent = ("User-Agent", "%s/%s" % (ProdName[:10], CapsVer))

UserAgent_Moz = (UserAgent[0], "Mozilla/5.0 (X11; U; Linux i686; cs-CZ; rv:1.7.9) Gecko/20050929")

edefs = dict()

for Name, Numb in htmlentitydefs.name2codepoint.iteritems():
	edefs[Name] = unichr(Numb)

del Name, Numb

Web.Opener.addheaders = [UserAgent_Moz]

REP_desc = {
	"<br>": chr(10),
	"< /br>": chr(10)
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
			comp = compile__("<font color.+?>(.+?)</font></a><br>(.+?)<br><font color.+?>(.+?)</font>", 16)
			list = comp.findall(data)
			if list:
				Number = itypes.Number()
				ls = []
				for JID, Name, Desc in list:
					JID = JID.strip()
					Name = Name.strip()
					Desc = Desc.strip()
					ls.append("%d) %s\n%s\n%s" % (Number.plus(), JID, Name, Desc))
				answer = chr(10) + decodeHTML(str.join(chr(10)*2, ls))
			else:
				answer = AllwebAnsBase[5]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

gCache = []

def command_google(ltype, source, body, disp):
	if body:
		if body == "*":
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
					ls.append(chr(10))
					ls.append(desc.get("unescapedUrl", ""))
					answer = decodeHTML(str.join("", ls))
					if list:
						gCache.append((source_, list))
						answer += AllwebAnsBase[4] % len(list)
				else:
					answer = AllwebAnsBase[2]
			else:
				answer = AllwebAnsBase[3]
		else:
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
						ls.append(chr(10))
						ls.append(desc.get("unescapedUrl", ""))
						answer = decodeHTML(str.join("", ls))
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
						answer = AllwebAnsBase[1]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_cinema(ltype, source, body, disp):
	if body:
		Search = True
		if (body.split()[0]) == chr(42):
			body = body[2:].lstrip()
		elif body.isdigit():
			Search = False
		if Search:
			Req = body.encode("cp1251")
			Req = Web("http://m.kinopoisk.ru/search/%s" % Web.One.quote_plus(Req))
			try:
				data = Req.get_page(UserAgent)
			except:
				answer = AllwebAnsBase[0]
			else:
				data = data.decode("cp1251")
				comp = compile__('<a href="http://m.kinopoisk.ru/movie/(\d+?)/">(.+?)</a>')
				list = comp.findall(data)
				if list:
					Number = itypes.Number()
					ls = ["\n[#] [Name, Year] (#id)"]
					for Numb, Name in list:
						ls.append("%d) %s (#%s)" % (Number.plus(), sub_ehtmls(Name), Numb))
					answer = str.join(chr(10), ls)
				else:
					answer = AllwebAnsBase[1]
		else:
			Req = Web("http://m.kinopoisk.ru/movie/%s" % (body))
			try:
				data = Req.get_page(UserAgent)
			except:
				answer = AllwebAnsBase[0]
			else:
				data = data.decode("cp1251")
				data = get_text(data, '<p class="title">', "</div>")
				if data:
					data = decodeHTML(data)
					ls = []
					for line in data.splitlines():
						line = line.strip()
						if line:
							if line[0].islower():
								line = "%s%s" % (line[0].upper(), line[1:])
							ls.append(line)
					answer = str.join(chr(10), ls)
				else:
					answer = AllwebAnsBase[1]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([sub_ehtmls, e_sb, decodeHTML, command_jc, command_google, command_cinema])
expansions[exp_name].ls.extend([
						htmlentitydefs.__name__,
						json.__name__,
						"AllwebAnsBase",
						"UserAgent",
						"UserAgent_Moz",
						"edefs",
						"XML_ls",
						"REP_desc",
						"compile_st",
						"compile_ehtmls",
						"gCache"
								])

command_handler(command_jc, {"RU": "рейтинг", "EN": "jc"}, 2, exp_name)
command_handler(command_google, {"RU": "гугл", "EN": "google"}, 2, exp_name)
command_handler(command_cinema, {"RU": "кино", "EN": "cinema"}, 2, exp_name)
