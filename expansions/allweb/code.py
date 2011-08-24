# -*- coding: utf-8 -*-

#  BlackSmith mark.2
exp_name = "allweb" # /code.py v.x2
#  Id: 28~2a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

import json

UserAgent = ("User-agent", "%s/%s" % (ProdName[:10], CapsVer))

UserAgent_Moz = (UserAgent[0], "Mozilla/5.0")

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

def command_jc(ltype, source, body, disp):
	if Chats.has_key(source[1]):
		if body:
			cName = body.lower()
			if cName.count("@conf"):
				cName = (cName.split("@conf"))[0]
		else:
			cName = (source[1].split("@conf"))[0]
		link = "http://jc.jabber.ru/search.html?%s" % quote_({"search": cName.encode('utf-8')})
		try:
			data = read_url(link, UserAgent)
		except:
			answer = allweb_answers[0]
		else:
			x = re_comp('<div align="left">').search(data)
			if x:
				data = data[x.end():].strip()
				if data.count('<font color="blue">'):
					answer, Var = "\n", itypes.Number()
					while True:
						x = re_comp('<font color="blue">').search(data)
						if not x:
							break
						data = data[x.end():].strip()
						x = re_comp("</font><br><br>").search(data)
						if x:
							body = data[:x.start()].strip()
							body = replace_all(body, ["\r", '<font color="gray">', "</font>"] + _html_ls_ + _xml_.items()).strip()
							while body.count("\n\n"):
								body = body.replace("\n\n", "\n")
							answer += '%d) %s\n\n' % (Var.plus(), body)
				else:
					x = re_comp("</div>").search(data)
					if x:
						answer = replace_all(data[:x.start()], ["\r"] + _html_ls_ + _xml_.items()).strip()
					else:
						answer = AnsBase[7]
			else:
				answer = AnsBase[7]
	else:
		answer = AnsBase[0]
	if not answer.strip():
		answer = allweb_answers[1]
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
			link = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s" % quote_({"q": body.encode('utf-8')})
			try:
				data = read_url(link, UserAgent)
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

expansions[exp_name].funcs_add([command_jc, command_google])
expansions[exp_name].ls.extend([json.__name__, "allweb_answers", "UserAgent", "UserAgent_Moz", "_xml_", "_html_ls_", "GoogleCache"])

command_handler(command_jc, {"RU": "рейтинг", "EN": "jc"}, 2, exp_name)
command_handler(command_google, {"RU": "гугл", "EN": "google"}, 2, exp_name)
