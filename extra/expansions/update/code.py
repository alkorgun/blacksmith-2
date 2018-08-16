# coding: utf-8

#  BlackSmith mark.2
# exp_name = "update" # /code.py v.x1
#  Id: 37~1c
#  Code © (2012-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	SvnRoot = (Caps + "trunk/")
	SvnBranches = (Caps + "branches/")

	def last_rev(self, answer, link):
		try:
			answer.append(get_text(Web(link).get_page(), "<title>", "</title>"))
		except Exception:
			pass

	compile_svn_links = compile__("<li><a href=\".+?\">(.+?)</a></li>")

	sep = chr(47)

	def update(self, done, errors, link, prefix):
		Opener = Web(link)
		if link.endswith(self.sep):
			try:
				fp = Opener.open()
				data = fp.read()
				fp.close()
			except Web.two.HTTPError as exc:
				errors.append((link, str(exc)))
			except Exception as exc:
				errors.append((link, exc_str(exc)))
			else:
				for li in self.compile_svn_links.findall(data):
					if li != "..":
						self.update(done, errors, link + li, prefix)
		else:
			try:
				fp = Opener.open()
				info = fp.info()
				fp.close()
			except Web.two.HTTPError as exc:
				errors.append((link, str(exc)))
			except Exception as exc:
				errors.append((link, exc_str(exc)))
			else:
				size = int(info.get("Content-Length", -1))
				file = link[prefix:]
				exists = os.path.isfile(file)
				if not exists or size != os.path.getsize(file):
					folder = os.path.dirname(file)
					if folder and not os.path.isdir(folder):
						os.makedirs(folder)
					try:
						filename = Opener.download(file)[0]
					except Web.two.HTTPError as exc:
						errors.append((link, str(exc)))
					except SelfExc as exc:
						errors.append((link, exc[0].capitalize()))
					except Exception as exc:
						errors.append((link, exc_str(exc)))
					else:
						done.append("%s\t%s" % (("U" if exists else "A"), filename))

	def command_update(self, stype, source, body, disp):
		answer = []
		if body:
			body = body.lower()
			if body == "branches":
				link = self.SvnBranches
			elif body == "last":
				self.last_rev(answer, self.SvnRoot)
				answer = (answer[0] if answer else AnsBase[7])
			else:
				answer = AnsBase[2]
		else:
			link = self.SvnRoot
		if not answer:
			self.last_rev(answer, link)
			if not answer:
				answer.append("Unknown Revision: /" + link.split(self.sep)[4])
			errors = []
			try:
				self.update(answer, errors, link, len(link))
			except Exception as exc:
				answer.append(chr(10) + exc_str(exc))
			if errors:
				answer.append("\nSome errors happened:\n")
				for err in errors:
					answer.append("\n\t".join(err))
			answer = str.join(chr(10), answer)
		Answer(answer, stype, source, disp)

	commands = ((command_update, "update", 8,),)
