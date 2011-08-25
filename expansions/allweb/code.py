# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "allweb" # /code.py v.x4
#  Id: 28~4a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

import json

UserAgent = ("User-Agent", "%s/%s" % (ProdName[:10], CapsVer))

UserAgent_Moz = (UserAgent[0], "Mozilla/5.0 (X11; U; Linux i686; cs-CZ; rv:1.7.12) Gecko/20050929")

_xml_ = {
	"&apos;": "'",
	"&quot;": '"',
	"&#39;": "`",
	"&amp;": "&",
	"&lt;": "<",
	"&gt;": ">",
	"&middot;": ";",
	"&nbsp;"*4: "\t",
	"&#0151": "-",
	"&nbsp;": " ",
	"&copy;": "©".decode("utf-8"),
	"&laquo;": "«".decode("utf-8"),
	"&raquo;": "»".decode("utf-8"),
		}

_html_ls_ = [
	("<br>", "\n"),
	"</br>",
	("<b>", "«".decode("utf-8")),
	("</b>", "»".decode("utf-8")),
	"<a>",
	"</a>",
	"<s>",
	"</s>",
	("<p>", "\n"),
	"</p>",
			]

compile__ = re_comp("<[^<>]+>")

def command_jc(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			cName = body.lower()
			if cName.count("@conf"):
				cName = (cName.split("@conf"))[0]
		else:
			cName = (source[1].split("@conf"))[0]
		link = "http://jc.jabber.ru/search.html?%s" % eqlnk({"search": cName.encode("utf-8")})
		try:
			data = get_page(link, UserAgent)
		except:
			answer = allweb_answers[0]
		else:
			compile_ = re_comp('<font color="blue">(.+?)</font></a><br>\n(.+?)<br><font color="gray">(.+?)</font>')
			list = compile_.findall(data)
			if list:
				answer, Var = "\n", itypes.Number()
				for JID, Name, Desc in list:
					body = replace_all("%s\n%s\n%s" % (JID, Name, Desc), ["\r"] + _html_ls_ + _xml_.items())
					answer += '%d) %s\n\n' % (Var.plus(), body.strip())
			else:
				answer = allweb_answers[5]
	else:
		answer = AnsBase[0]
	Answer(answer, ltype, source, disp)

GoogleCache = []

def command_google(ltype, source, body, disp):
	if body:
		if body == "*":
			source_ = get_source(source[1], source[2])
			if source_:
				list = []
				for ls in GoogleCache:
					if ls[0] == source_:
						list = GoogleCache.pop(GoogleCache.index(ls))[1]
						break
				if list:
					ans = list.pop(0)
					while list and not ans.has_key("content"):
						ans = list.pop(0)
					if ans.has_key("content"):
						answer = replace_all(ans.pop("content"), ["\r"] + _html_ls_ + _xml_.items()).strip()
						if ans.has_key("title"):
							qrt_ = replace_all(ans.pop("title"), _html_ls_ + _xml_.items()).strip()
							answer = (qrt_ + answer)
						if ans.has_key("unescapedUrl"):
							answer += "\n%s" % ans.pop("unescapedUrl")
						if list:
							GoogleCache.append((source_, list))
							answer += allweb_answers[4] % len(list)
					else:
						answer = allweb_answers[1]
				else:
					answer = allweb_answers[2]
			else:
				answer = allweb_answers[3]
		else:
			link = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s" % eqlnk({"q": body.encode("utf-8")})
			try:
				data = get_page(link, UserAgent)
			except:
				answer = allweb_answers[0]
			else:
				try:
					data = json.loads(data)
				except:
					answer = allweb_answers[1]
				else:
					data = data.get("responseData", {"results": None})
					list = data.get("results", None)
					if list:
						ans = list.pop(0)
						while list and not ans.has_key("content"):
							ans = list.pop(0)
						if ans.has_key("content"):
							answer = replace_all(ans.pop("content"), ["\r"] + _html_ls_ + _xml_.items()).strip()
							if ans.has_key("title"):
								qrt_ = replace_all(ans.pop("title"), _html_ls_ + _xml_.items()).strip()
								answer = (qrt_ + answer)
							if ans.has_key("unescapedUrl"):
								answer += "\n%s" % ans.pop("unescapedUrl")
							if list:
								source_ = get_source(source[1], source[2])
								if source_:
									for ls in GoogleCache:
										if ls[0] == source_:
											GoogleCache.pop(GoogleCache.index(ls))
											break
									if len(GoogleCache) >= 16:
										GoogleCache.pop(0)
									GoogleCache.append((source_, list))
									answer += allweb_answers[4] % len(list)
						else:
							answer = allweb_answers[1]
					else:
						answer = allweb_answers[1]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

def command_cinema(ltype, source, body, disp):
	if body:
		search = True
		if (body.split()[0]) == "*":
			body = body[2:].lstrip()
		elif check_number(body):
			search = False
		if search:
			link = "http://m.kinopoisk.ru/search/%s" % eqlnk({"s": body.encode("cp1251")})[2:]
			try:
				data = get_page(link, UserAgent)
			except:
				answer = allweb_answers[0]
			else:
				data = data.decode("cp1251")
				compile_ = re_comp('<a href="http://m.kinopoisk.ru/movie/(\d+?)/">(.+?)</a>')
				list = compile_.findall(data)
				if list:
					answer, Number = "\n[#] [Name, Year] (#id)", itypes.Number()
					for Numb, Name in list:
						answer += "\n%d) %s (#%s)" % (Number.plus(), Name, Numb)
				else:
					answer = allweb_answers[1]
		else:
			link = "http://m.kinopoisk.ru/movie/%d" % int(body)
			try:
				data = get_page(link, UserAgent)
			except:
				answer = allweb_answers[0]
			else:
				data = data.decode("cp1251")
				data = get_text(data, '<p class="title">', "</div>")
				if data:
					data = compile__.sub("", replace_all(data, [("<br>", "\n"), "\r"] + _xml_.items())).strip()
					answer = ""
					list = data.splitlines()
					for line in list:
						line = line.strip()
						if line:
							if line[0].islower():
								line = "%s%s" % (line[0].upper(), line[1:])
							answer += ("\n" + line)
				else:
					answer = allweb_answers[1]
	else:
		answer = AnsBase[1]
	Answer(answer, ltype, source, disp)

expansions[exp_name].funcs_add([command_jc, command_google, command_cinema])
expansions[exp_name].ls.extend([json.__name__, "allweb_answers", "UserAgent", "UserAgent_Moz", "_xml_", "_html_ls_", "compile__", "GoogleCache"])

command_handler(command_jc, {"RU": "рейтинг", "EN": "jc"}, 2, exp_name)
command_handler(command_google, {"RU": "гугл", "EN": "google"}, 2, exp_name)
command_handler(command_cinema, {"RU": "кино", "EN": "cinema"}, 2, exp_name)
