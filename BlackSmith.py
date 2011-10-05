#!/usr/bin/python
# coding: utf-8

# BlackSmith's core mark.2
# BlackSmith.py

# Code © (2010-2011) by WitcherGeralt (alkorgun@gmail.com)

# imports

from types import NoneType, UnicodeType, InstanceType
from traceback import print_exc as exc_info__
from random import shuffle, randint, choice
from re import compile as compile__

import sys, os, gc, time, ConfigParser

BsCore2 = __file__
LibsDir = "librarys.zip"
BsDir = os.path.dirname(BsCore2)
if BsDir:
	os.chdir(BsDir)
sys.path.append(LibsDir)

from enconf import *

import xmpp, iThr, itypes

# Cache & Statistics

eColors = xmpp.debug.colors_enabled # Unix colors

color0 = chr(27) + "[0m" # none
color1 = chr(27) + "[33m" # yellow
color2 = chr(27) + "[31;1m" # red
color3 = chr(27) + "[32m" # green
color4 = chr(27) + "[34;1m" # blue

sys_cmds = [
	"ps -o rss -p %d", # 0
	'TASKLIST /FI "PID eq %d"', # 1
	"COLOR F0", # 2
	"Title", # 3
	"TASKKILL /PID %d /T /f", # 4
	"Ver", # 5
	'sh -c "%s" 2>&1' # 6
			]

Types = [
	"chat", # 0
	"groupchat", # 1
	"normal", # 2
	"available", # 3
	"unavailable", # 4
	"subscribe", # 5
	"private", # 6
	"error", # 7
	"result", # 8
	"set", # 9
	"get", # 10
	"received", # 11
	"answer", # 12
	"dispatch-", # 13
	"чат".decode("utf-8"), # 14
	"приват".decode("utf-8"), # 15
	"ping", # 16
	"time", # 17
	"query", # 18
	"jid", # 19
	"nick", # 20
	"can't start new thread", # 21
	"request" # 22
		]

AflRoles = [
	"affiliation", # 0
	"outcast", # 1
	"none", # 2
	"member", # 3
	"admin", # 4
	"owner", # 5
	"role", # 6
	"visitor", # 7
	"participant", # 8
	"moderator" # 9
			]

sList = [
	"chat", # готов поболтать
	"away", # отошел
	"xa", # не беспокоить
	"dnd" # недоступен
		]

aDesc = {
	"owner": 3,
	"moderator": 3,
	"admin": 2,
	"participant": 1,
	"member": 1
		}

sCodesDesc = {
	"301": "has-been-banned", # 0
	"303": "nick-changed", # 1
	"307": "has-been-kicked", # 2
	"407": "members-only" # 3
			}

sCodes = sorted(sCodesDesc.keys())

eCodesDesc = {
	"302": "redirect", # 0
	"400": "unexpected-request", # 1
	"401": "not-authorized", # 2
	"402": "payment-required", # 3
	"403": "forbidden", # 4
	"404": "remote-server-not-found", # 5
	"405": "not-allowed", # 6
	"406": "not-acceptable", # 7
	"407": "subscription-required", # 8
	"409": "conflict", # 9
	"500": "undefined-condition", # 10
	"501": "feature-not-implemented", # 11
	"503": "service-unavailable", # 12
	"504": "remote-server-timeout" # 13
			}

eCodes = sorted(eCodesDesc.keys())

Features = [
	xmpp.NS_VERSION, # 0
	xmpp.NS_PING, # 1
	xmpp.NS_TIME, # 2
	xmpp.NS_URN_TIME, # 3
	xmpp.NS_LAST, # 4
	xmpp.NS_DISCO_INFO # 5
			]

aFeatures = Features + [
	xmpp.NS_DISCO_ITEMS,
	xmpp.NS_MUC,
	xmpp.NS_PRIVACY,
	xmpp.NS_ROSTER,
	xmpp.NS_DATA,
	xmpp.NS_RECEIPTS
			]

IsJID = compile__("\w+?@\w+?\.\w+?", 32)

VarCache = {
	"idle": 0.24,
	"alive": True,
	"errors": [],
	"action": "# %s %s &" % (os.path.split(sys.executable)[1], BsCore2)
			}

Info = {
	"cmd": itypes.Number(),		"sess": time.time(),
	"msg": itypes.Number(),		"alls": [],
	"cfw": itypes.Number(),		"up": 1.24,
	"prs": itypes.Number(),		"iq": itypes.Number(),
	"errors": itypes.Number(),
	"omsg": itypes.Number(),	"outiq": itypes.Number()
		}

# frienly handlers

class SelfExc(Exception):
	pass

def exc_info():
	exc = sys.exc_info()
	return (exc[0].__name__, str(exc[1]))

def exc_info_(fp = None):
	try:
		exc_info__(None, fp)
	except:
		pass

database = (itypes.Database)

def get_exc():
	try:
		exc = iThr.get_exc()
	except:
		exc = "(...)"
	return exc

def exec_(instance, list = ()):
	try:
		code = instance(*list)
	except:
		code = None
	return code

def try_body(body, color):
	try:
		body = UnicodeType(body)
	except:
		color = False
	return (body, color)

def text_color(text, color):
	if eColors:
		text = color+text+color0
	return text

def Print(text, color = False):
	try:
		if color:
			text = text_color(text, color)
		print text
	except:
		pass

def try_sleep(slp):
	try:
		time.sleep(slp)
	except KeyboardInterrupt:
		os._exit(0)
	except:
		pass

def Exit(text, exit, slp):
	Print(text, color2); try_sleep(slp)
	if exit:
		os._exit(0)
	else:
		os.execl(sys.executable, sys.executable, BsCore2)

try:
	reload(sys)
	sys.setdefaultencoding("utf-8")
except:
	Print("\n\nError: can't set default encoding!", color2)

# Global Names

dynamic = "current/%s"
static = "static/%s"
PlugsDir = "expansions"
SvnCache = ".svn/entries"
FeilDir = "feillog"
PidFile = "sessions.db"
GenCrash = "dispatcher.crash"
InscrFile = static % ("insc.py")
GenConFile = static % ("config.ini")
ConDispFile = static % ("clients.ini")
ChatsFile = dynamic % ("chats.db")

(BsMark, BsVer, BsRev) = (2, 16, 0)

if os.access(SvnCache, os.R_OK):
	BsRev = open(SvnCache).readlines()[3].strip()

ProdName = "BlackSmith mark.%d" % (BsMark)
ProdVer = "%d (r.%s)" % (BsVer, BsRev)
Caps = "http://blacksmith-2.googlecode.com/svn/"
CapsVer = "%d.%d" % (BsMark, BsVer)
FullName = "HellDev's %s CoreVer.%s (%s)" % (ProdName, ProdVer, Caps)

BotOs, BsPid = os.name, os.getpid()

oSlist = [(BotOs == ("nt")), (BotOs == ("posix"))]

def client_config(config, section):
	serv = config.get(section, "serv").lower()
	port = config.get(section, "port")
	if not port.isdigit():
		port = 5222
	user = config.get(section, "user").lower()
	host = config.get(section, "host").lower()
	code = config.get(section, "pass")
	jid = "%s@%s" % (user, host)
	return (jid, (serv, port, host, user, code))

try:
	GenCon = ConfigParser.ConfigParser()
	GenCon.read(GenConFile)
	Gen_disp, Instance = client_config(GenCon, "CLIENT")
	InstansesDesc = {Gen_disp: Instance}
	ConTls = eval(GenCon.get("STATES", "TLS"))
	Mserve = eval(GenCon.get("STATES", "MSERVE"))
	GetExc = eval(GenCon.get("STATES", "GETEXC"))
	DefLANG = GenCon.get("STATES", "LANG").upper()[0:2]
	GodName = GenCon.get("CONFIG", "ADMIN").lower()
	DefNick = GenCon.get("CONFIG", "NICK").split()[0]
	DefStatus = GenCon.get("CONFIG", "STATUS")
	GenResource = GenCon.get("CONFIG", "RESOURCE")
	IncLimit = int(GenCon.get("LIMITS", "INCOMING"))
	PrivLimit = int(GenCon.get("LIMITS", "PRIVATE"))
	ConfLimit = int(GenCon.get("LIMITS", "CHAT"))
	MaxMemory = int(GenCon.get("LIMITS", "MEMORY"))*1024
	ConDisp = ConfigParser.ConfigParser()
	if os.path.isfile(ConDispFile):
		ConDisp.read(ConDispFile)
		for block in ConDisp.sections():
			Instance, desc = client_config(ConDisp, block)
			InstansesDesc[Instance] = desc
except:
	Exit("\n\nOne of config files is corrupted!", 1, 30)

MaxMemory = (32768 if (MaxMemory and MaxMemory <= 32768) else MaxMemory)

try:
	execfile(InscrFile)
except:
	Exit("\n\nError: inscript is damaged!", 1, 30)

if oSlist[0]:
	os.system(sys_cmds[2])
	os.system("%s %s" % (sys_cmds[3], FullName))

# lists & clients

expansions = {}
Cmds = {}
cPrefs = ("!","@","#",".","*")
sCmds = []
Chats = {}
Flood = {}
Galist = {GodName: 8}
Roster = {"on": True}
Clients = {}
ChatsAttrs = {}
Handlers = {
	"01eh": [], "02eh": [],
	"03eh": [], "04eh": [],
	"05eh": [], "00si": [],
	"01si": [], "02si": [],
	"03si": [], "04si": []
			}

Sequeque = iThr.Semaphore(len(InstansesDesc.keys())*15)
Sequence = iThr.Semaphore()

# call & execut Threads & handlers

def execute_handler(handler_instance, list = (), command = None):
	try:
		handler_instance(*list)
	except KeyboardInterrupt:
		pass
	except iThr.ThrKill:
		pass
	except SelfExc:
		pass
	except:
		lytic_crashlog(handler_instance, command)

def call_sfunctions(ls, list = ()):
	for handler in Handlers[ls]:
		execute_handler(handler, list)

def composeTimer(cors, handler, Name = False, list = (), command = None):
	if not Name:
		Name = "iTimer-%d" % (iThr.aCounter._int())
	Timer_ = iThr.Timer(cors, execute_handler, (handler, list, command,))
	Timer_.name = Name
	return Timer_

def composeThr(handler, Name, list = (), command = None):
	if not Name.startswith(Types[13]):
		Name = "%s-%d" % (Name, iThr.aCounter._int())
	return iThr.KThread(execute_handler, Name, (handler, list, command,))

def Try_Thr(Thr, Number = 0):
	if Number >= 4:
		raise RuntimeError("exit")
	try:
		Thr.start()
	except:
		Try_Thr(Thr, (Number + 1))

def sThread_Run(Thr, handler, command = None):
	try:
		Thr.start()
	except iThr.ThrFail:
		if (exc_info()[1] == Types[21]):
			try:
				Try_Thr(Thr)
			except RuntimeError:
				try:
					Thr._run_backup()
				except KeyboardInterrupt:
					raise KeyboardInterrupt("Interrupt (Ctrl+C)")
				except:
					lytic_crashlog(handler, command)
		else:
			lytic_crashlog(sThread_Run, command)
	except:
		lytic_crashlog(sThread_Run, command)

def sThread(name, handler, list = (), command = None):
	with Sequeque:
		sThread_Run(composeThr(handler, name, list, command), handler, command)

def call_functions(ls, list = ()):
	for handler in Handlers[ls]:
		sThread(ls, handler, list)

# exceptions, register handlers & commands

class expansion(object):

	def __init__(self, object):
		self.name = object
		self.path = "%s/%s" % (PlugsDir, self.name)
		self.file = "%s/code.py" % (self.path)
		self.isExp = os.path.isfile(self.file)
		self.insc = "%s/insc.py" % (self.path)
		self.hnds, self.cmds, self.ls = {}, [], []

	def dels(self, full = False):
		while len(self.cmds):
			cmd = self.cmds.pop()
			if Cmds.has_key(cmd):
				Cmds[cmd].off()
		self.funcs_del()
		while len(self.ls):
			Name = self.ls.pop()
			if globals().has_key(Name):
				del globals()[Name]
		if full and expansions.has_key(self.name):
			del expansions[self.name]

	def funcs_del(self, handler = False):

		def del_(handler):
			ls = self.hnds[handler]
			if ls == "03si":
				execute_handler(handler)
			Handler_del(ls, handler)
			del self.hnds[handler]

		if not handler:
			for handler in self.hnds.keys():
				del_(handler)
		elif self.hnds.has_key(handler):
			del_(handler)

	def initialize_all(self):
		for handler in self.hnds.keys():
			ls = self.hnds[handler]
			if ls in ["00si", "02si"]:
				execute_handler(handler)
			elif ls == "01si":
				for conf in Chats.keys():
					execute_handler(handler, (conf,))

	def func_add(self, handler, base):
		self.hnds[handler] = base

	def funcs_add(self, handlers):
		for handler in handlers:
			self.ls.append(handler.func_name)

	def load(self):
		try:
			execfile(self.file, globals())
		except:
			return (self.name, False, exc_info())
		return (self.name, True, False)

	def load_insc(self):
		if os.path.isfile(self.insc):
			execfile(self.insc, globals())

def Handler_add(ls, handler):
	if handler not in Handlers[ls]:
		Handlers[ls].append(handler)

def Handler_del(ls, handler):
	if handler in Handlers[ls]:
		Handlers[ls].remove(handler)

def expansion_register(name):
	if expansions.has_key(name):
		expansions[name].dels()
	else:
		expansions[name] = expansion(name)
	expansions[name].load_insc()

def handler_register(handler, ls, name):
	iname = handler.func_name
	for instance in Handlers[ls]:
		if iname == instance.func_name:
			Handlers[ls].remove(instance)
	Handler_add(ls, handler)
	expansions[name].func_add(handler, ls)

class Command(object):

	def __init__(self, inst, name, access, help, exp):
		self.exp = exp
		self.numb = itypes.Number()
		self.name = name
		self.isAvalable = True
		self.help = help
		self.handler = inst
		self.users = []
		self.access = access

	def reload(self, inst, access, help, exp):
		self.exp = exp
		self.isAvalable = True
		self.handler = inst
		self.help = help
		self.access = access

	def off(self):
		self.isAvalable = False
		self.handler = None

	def execute(self, ltype, source, body, disp):
		if enough_access(source[1], source[2], self.access):
			if self.isAvalable and self.handler:
				Info["cmd"].plus()
				sThread("command", self.handler, (ltype, source, body, disp), self.name)
				self.numb.plus()
				source = get_source(source[1], source[2])
				if source and source not in self.users:
					self.users.append(source)
			else:
				Answer(AnsBase[19] % (self.name), ltype, source, disp)
		else:
			Answer(AnsBase[10], ltype, source, disp)

def command_handler(handler, commands, access, name, pfx = True):
	if DefLANG in commands.keys():
		help = "%s/%s/%s.%s" % (PlugsDir, name, commands["EN"], DefLANG.lower())
		command = commands[DefLANG].decode("utf-8")
	else:
		help = "%s/%s/%s.en" % (PlugsDir, name, commands["EN"])
		command = commands["EN"]
	if Cmds.has_key(command):
		Cmds[command].reload(handler, access, help, name)
	else:
		Cmds[command] = Command(handler, command, access, help, name)
	if not pfx and command not in sCmds:
		sCmds.append(command)
	expansions[name].cmds.append(command)

# Chats, Users & other

class sUser:

	def __init__(self, nick, role, source, access = None):
		self.nick = nick
		self.source = source
		self.role = role
		self.ishere = True
		self.date = (time.time(), Yday(), time.asctime())
		self.access = access
		if not access and access != 0:
			self.calc_acc()

	def aroles(self, role):
		if self.role != role:
			self.role = role
			return True
		return False

	def calc_acc(self):
		self.access = (aDesc.get(self.role[0], 0) + aDesc.get(self.role[1], 0))

class sConf:

	def __init__(self, name, disp, code = None, cPref = None, nick = DefNick, added = False):
		self.name = name
		self.disp = disp
		self.nick = nick
		self.code = code
		self.more = ""
		self.IamHere = None
		self.isModer = True
		self.alist = {}
		self.oCmds = []
		self.users = {}
		self.sdate = 0
		self.cPref = cPref
		self.status = DefStatus
		self.state = sList[0]
		if not added:
			self.save()

	def load_all(self):
		call_sfunctions("01si", (self.name,))

	def csend(self, stanza):
		Sender(self.disp, stanza)

	def isHere(self, nick):
		return self.users.has_key(nick)

	def isHereNow(self, nick):
		if self.isHere(nick):
			return self.users[nick].ishere
		return False

	def isHe(self, nick, source):
		return (self.users[nick].source == source)

	def get_user(self, nick):
		return self.users.get(nick)

	def get_nicks(self):
		return self.users.keys()

	def sorted_users(self):
		return [self.get_user(nick) for nick in sorted(self.get_nicks())]

	def get_users(self):
		return self.users.values()

	def joined(self, nick, role, source):
		access = Galist.get(source, None)
		if not access and access != 0:
			access = self.alist.get(source, None)
		self.users[nick] = sUser(nick, role, source, access)

	def aroles_change(self, nick, role):
		if self.get_user(nick).aroles(role):
			source = self.get_user(nick).source
			if not Galist.has_key(source):
				if not self.alist.has_key(source):
					self.get_user(nick).calc_acc()

	def NewNick(self, old_nick, nick):
		self.users[nick] = self.users.pop(old_nick)

	def leaved(self, nick):
		self.users[nick].ishere = False

	def composePres(self):
		stanza = xmpp.Presence("%s/%s" % (self.name, self.nick))
		stanza.setShow(self.state)
		stanza.setStatus(self.status)
		return caps_add(stanza)

	def join(self):
		stanza = self.composePres()
		self.sdate = time.time()
		query = stanza.setTag("x", namespace = xmpp.NS_MUC)
		query.addChild("history", {"maxchars": "0"})
		if self.code:
			query.setTagData("password", self.code)
		self.csend(stanza)

	def subject(self, body):
		self.csend(xmpp.Message(self.name, "", Types[1], body))

	def set_status(self, state, status):
		self.state, self.status = state, status

	def change_status(self, state, status):
		self.set_status(state, status)
		self.csend(self.composePres())

	def save_stats(self):
		call_sfunctions("03si", (self.name,))

	def leave(self, estatus = False):
		self.IamHere = None
		self.isModer = True
		self.more = ""
		stanza = xmpp.Presence(self.name, Types[4])
		if estatus:
			stanza.setStatus(estatus)
		self.csend(stanza)

	def full_leave(self, status = False):
		self.leave(status)
		del Chats[self.name]
		self.save_stats()
		self.save(False)
		call_sfunctions("04si", (self.name,))
		if ChatsAttrs.has_key(self.name):
			del ChatsAttrs[self.name]

	def save(self, True_save = True):
		if initialize_file(ChatsFile):
			list = eval(get_file(ChatsFile))
			if not True_save:
				if list.has_key(self.name):
					del list[self.name]
			else:
				list[self.name] = {"disp": self.disp, Types[20]: self.nick, "cPref": self.cPref, "code": self.code}
			cat_file(ChatsFile, str(list))
		else:
			delivery("%s" % (self.name))

	def iq_sender(self, x, y, afrls, afrl, text = "", source = ()):
		stanza = xmpp.Iq(to = self.name, typ = Types[9])
		stanza.setID("Bs-i%d" % Info["outiq"].plus())
		query = xmpp.Node(Types[18])
		query.setNamespace(xmpp.NS_MUC_ADMIN)
		arole = query.addChild("item", {x: y, afrls: afrl})
		if text:
			arole.setTagData("reason", text)
		stanza.addChild(node = query)
		if not source:
			self.csend(stanza)
		else:
			CallForResponse(self.disp, stanza, Handle_Answer, {"source": source})

	def ban(self, jid, text = "", source = ()):
		self.iq_sender(Types[19], jid, AflRoles[0], AflRoles[1], text, source)

	def none(self, jid, text = "", source = ()):
		self.iq_sender(Types[19], jid, AflRoles[0], AflRoles[2], text, source)

	def member(self, jid, text = "", source = ()):
		self.iq_sender(Types[19], jid, AflRoles[0], AflRoles[3], text, source)

	def admin(self, jid, text = "", source = ()):
		self.iq_sender(Types[19], jid, AflRoles[0], AflRoles[4], text, source)

	def owner(self, jid, text = "", source = ()):
		self.iq_sender(Types[19], jid, AflRoles[0], AflRoles[5], text, source)

	def kick(self, nick, text = "", source = ()):
		self.iq_sender(Types[20], nick, AflRoles[6], AflRoles[2], text, source)

	def visitor(self, nick, text = "", source = ()):
		self.iq_sender(Types[20], nick, AflRoles[6], AflRoles[7], text, source)

	def participant(self, nick, text = "", source = ()):
		self.iq_sender(Types[20], nick, AflRoles[6], AflRoles[8], text, source)

	def moder(self, nick, text = "", source = ()):
		self.iq_sender(Types[20], nick, AflRoles[6], AflRoles[9], text, source)

def get_source(source, nick):
	if Chats.has_key(source):
		if Chats[source].isHere(nick):
			source = getattr(Chats[source].get_user(nick), "source")
		else:
			source = None
	return source

def get_access(source, nick):
	if Chats.has_key(source):
		if Chats[source].isHere(nick):
			access = getattr(Chats[source].get_user(nick), "access")
		else:
			access = 0
	else:
		access = Galist.get(source, 2)
	return access

enough_access = lambda conf, nick, Numb = int(): (Numb <= get_access(conf, nick))

object_encode = lambda body: (body if isinstance(body, UnicodeType) else body.decode("utf-8", str.replace.__name__))

def delivery(body):
	try:
		disp, body = Gen_disp, object_encode(body)
		if not online(Gen_disp):
			for disp_ in Clients.keys():
				if Gen_disp != disp_ and online(disp_):
					disp = disp_
					break
				if Gen_disp == disp:
					raise SelfExc("None connected clients!")
		Info["omsg"].plus()
		Clients[disp].send(xmpp.Message(GodName, body, Types[0]))
	except IOError:
		Print("\n\n%s" % (body), color1)
	except SelfExc:
		Print("\n\n%s" % (body), color1)
	except:
		exc_info_()

def Msend(instance, body, disp = None):
	body = object_encode(body)
	if Chats.has_key(instance):
		ltype = Types[1]
		if not disp:
			disp = Chats[instance].disp
		if len(body) > ConfLimit:
			Chats[instance].more = body[ConfLimit:].strip()
			body = (AnsBase[18] % (body[:ConfLimit].strip(), ConfLimit))
	else:
		ltype = Types[0]
		if not disp:
			if isinstance(instance, xmpp.JID):
				chat = instance.getStripped()
			else:
				chat = (instance.split(chr(47)))[0].lower()
			if Chats.has_key(chat):
				disp = Chats[chat].disp
			else:
				disp = Gen_disp
		if len(body) > PrivLimit:
			col, all = itypes.Number(), str((len(body) / PrivLimit) + 1)
			while len(body) > PrivLimit:
				text = "[%d/%s] %s[...]" % (col.plus(), all, body[:PrivLimit].strip())
				Info["omsg"].plus()
				Sender(disp, xmpp.Message(instance, text, ltype))
				body = body[PrivLimit:].strip()
				time.sleep(2)
			body = "[%d/%s] %s" % (col.plus(), all, body)
	Info["omsg"].plus()
	Sender(disp, xmpp.Message(instance, body.strip(), ltype))

def Answer(body, ltype, source, disp = None):
	body = object_encode(body)
	if ltype == Types[1]:
		body = "%s: %s" % (source[2], body)
		Msend(source[1], body, disp)
	elif ltype == Types[0]:
		Msend(source[0], body, disp)

def CheckFlood(disp):
	disp = get_disp(disp)
	if not Flood.has_key(disp):
		Flood[disp] = []
	Flood[disp].append(time.time())
	col = len(Flood[disp])
	if col >= 4:
		if (Flood[disp][col - 1] - Flood[disp][0]) <= 8:
			Flood[disp] = [Flood[disp].pop()]
			xmpp_raise()
		else:
			Flood[disp].pop(0)

def IdleClient():
	cls = dict()
	for disp in Clients.keys():
		if online(disp):
			cls[disp] = 0
	for conf in Chats.keys():
		disp = Chats[conf].disp
		if cls.has_key(disp):
			cls[disp] += 1
	if cls:
		idle = min(cls.values())
		for disp, chats in cls.items():
			if chats == idle:
				return disp
	return Gen_disp

def ejoinTimer(conf):
	if Chats.has_key(conf):
		Chats[conf].join()

ejoinTimerName = lambda conf: "%s-%s" % (ejoinTimer.func_name, conf.decode("utf-8"))

def get_self_nick(conf):
	if Chats.has_key(conf):
		return getattr(Chats[conf], Types[20], DefNick)
	return DefNick

get_disp = lambda disp: "%s@%s" % (disp._owner.User, disp._owner.Server)

def online(disp):
	if isinstance(disp, InstanceType):
		disp = get_disp(disp)
	if Clients.has_key(disp):
		return Clients[disp].isConnected()
	return False

def CallForResponse(disp, stanza, handler, keywords = {}):
	if isinstance(stanza, xmpp.Iq):
		if isinstance(disp, InstanceType):
			disp = get_disp(disp)
		if Clients.has_key(disp):
			ID = stanza.getID()
			if not ID:
				xmpp.dispatcher.ID += 1
				ID = str(xmpp.dispatcher.ID)
				stanza.setID(ID)
			Clients[disp].RespExp[ID] = (handler, keywords)
			Sender(disp, stanza)

def exec_bsExp(instance, disp, node, kdesc):
	instance(disp, node, **kdesc)

def ResponseChecker(disp, stanza):
	Name = get_disp(disp)
	Numb = stanza.getID()
	if Clients[Name].RespExp.has_key(Numb):
		(handler, keywords) = Clients[Name].RespExp.pop(Numb)
		sThread(handler.func_name, exec_bsExp, (handler, disp, stanza, keywords))
		xmpp_raise()

def Handle_Answer(disp, stanza, source):
	if xmpp.isResultNode(stanza):
		Answer(AnsBase[4], source[0], source[1], disp)
	else:
		Answer(AnsBase[7], source[0], source[1], disp)

def Sender(disp, stanza):
	try:
		if not isinstance(disp, InstanceType):
			if Clients.has_key(disp):
				disp = Clients[disp]
			else:
				raise SelfExc("'%s' isn't my client!" % (disp))
		disp.send(stanza)
	except IOError:
		pass
	except SelfExc:
		pass
	except:
		lytic_crashlog(Sender)

sUnavailable = lambda disp, data: Sender(disp, xmpp.Presence(typ = Types[4], status = data))

def caps_add(node):
	node.setTag("c", {"node": Caps, "ver": CapsVer}, xmpp.NS_CAPS)
	return node

Yday = lambda: getattr(time.gmtime(), "tm_yday")

def sAttrs(stanza):
	source = stanza.getFrom()
	instance = source.getStripped()
	resource = source.getResource()
	stype = stanza.getType()
	return (source, instance.lower(), stype, resource)

GetRole = lambda node: (str(node.getAffiliation()), str(node.getRole()))

def xmpp_raise():
	raise xmpp.NodeProcessed("continue")

# file work handlers

chat_file = lambda chat, name: dynamic % ("%s/%s") % (chat, name)

def initialize_file(filename, data = "{}"):
	filename = cefile(filename)
	if os.path.isfile(filename):
		return True
	try:
		folder = os.path.dirname(filename)
		if folder and not os.path.exists(folder):
			os.makedirs(folder, 0755)
		cat_file(filename, data)
	except:
		return False
	return True

def del_file(filename):
	exec_(os.remove, (cefile(filename),))

def get_file(filename):
	path = cefile(filename)
	with open(path, "r") as fp:
		return fp.read()

def cat_file(filename, data, otp = "wb"):
	path = cefile(filename)
	with Sequence:
		with open(path, otp) as fp:
			fp.write(data)

# Crashlogs

def Dispatch_fail():
	crashfile = open(GenCrash, "a")
	exc_info_(crashfile)
	crashfile.close()

def lytic_crashlog(handler, command = None):
	Number, handler, error_body = (len(VarCache["errors"]) + 1), handler.func_name, get_exc()
	VarCache["errors"].append(error_body)
	if GetExc and online(Gen_disp):
		if command:
			exc = AnsBase[13] % (command, handler)
		else:
			exc = AnsBase[14] % (handler)
		delivery(AnsBase[15] % (exc))
	else:
		Print("\n\nError: can't execut '%s'!" % (handler), color2)
	filename = "%s/error[%d]%s.crash" % (FeilDir, (Info["cfw"]._int() + 1), strTime("[%H.%M.%S][%d.%m.%Y]"))
	try:
		if not os.path.exists(FeilDir):
			os.mkdir(FeilDir, 0755)
		crashfile = open(filename, "wb")
		Info["cfw"].plus()
		exc_info_(crashfile)
		crashfile.close()
		if GetExc and online(Gen_disp):
			if oSlist[0]:
				delivery(AnsBase[16] % (Number, filename))
			else:
				delivery(AnsBase[17] % (Number, filename))
		else:
			Print("\n\nCrash file --> %s\nError number --> %d" % (filename, Number), color2)
	except:
		exc_info_()
		if GetExc and online(Gen_disp):
			delivery(error_body)
		else:
			Print(*try_body(error_body, color2))

# Other handlers

def load_expansions():
	Print("\n\nExpansions loading...\n", color4)
	for PlugDir in os.listdir(PlugsDir):
		if (".svn") == (PlugDir) or not os.path.isdir(os.path.join(PlugsDir, PlugDir)):
			continue
		exp = expansion(PlugDir)
		if exp.isExp:
			loaded = exp.load()
			if loaded[1]:
				Print("%s - successfully loaded!" % (loaded[0]), color3)
			else:
				exp.dels(True)
				Print("Can't load - %s!%s" % (loaded[0], "\n\t* %s: %s") % (loaded[2]), color2)
		else:
			Print("%s - isn't an expansion!" % (exp.name), color2)

def get_pipe(command):
	try:
		pipe = os.popen(command)
		data = pipe.read()
		pipe.close()
		if oSlist[0]:
			data = data.decode("cp866")
	except:
		data = "(...)"
	return data

class Web:

	import urllib as One, urllib2 as Two

	Opener = One.FancyURLopener()
	Opener_2 = Two.build_opener()

	def __init__(self, link, data = [], headers = {}):
		self.link = link
		self.headers = headers
		if data:
			list = []
			for Name, Attr in data:
				Name = self.One.quote_plus(Name)
				Attr = self.One.quote_plus(Attr)
				list.append("%s=%s" % (Name, Attr))
			self.link += "&".join(list)

	def add_header(self, name, header):
		self.headers[name] = header

	def get_page(self, header = ()):
		dest = self.Two.Request(self.link)
		if header:
			self.add_header(*header)
		if self.headers:
			for header, desc in self.headers.iteritems():
				dest.add_header(header, desc)
		site = self.Opener_2.open(dest)
		data = site.read()
		return data

def get_text(body, s0, s2, s1 = "(?:.|\s)+"):
	comp = compile__("%s(%s?)%s" % (s0, s1, s2), 16)
	body = comp.search(body)
	if body:
		body = (body.group(1)).strip()
	return body

def sub_desc(body, ls, sbls = False):
	if isinstance(ls, dict):
		for x, z in ls.items():
			body = body.replace(x, z)
	else:
		for x in ls:
			if isinstance(x, tuple) or isinstance(x, list):
				if len(x) >= 2:
					body = body.replace(x[0], x[1])
				else:
					body = body.replace(x[0], (sbls if sbls else ""))
			else:
				body = body.replace(x, (sbls if sbls else ""))
	return body

strTime = lambda data = "%d.%m.%Y (%H:%M:%S)", local = True: time.strftime(data, time.localtime() if local else time.gmtime())

def Time2Text(Time):
	ext, ls = [], [("Year", 0), ("Month", 12), ("Day", 30), ("Hour", 24), ("Minute", 60), ("Second", 60)]
	while True:
		lr = ls.pop()
		if lr[1]:
			(Time, Rest) = divmod(Time, lr[1])
		else:
			Rest = Time
		if Rest:
			ext.insert(0, "%d %s%s" % (Rest, lr[0], ("s" if Rest >= 2 else "")))
		if not (ls and Time):
			return str.join(chr(32), ext)

def Size2Text(Size):
	ext, ls = [], list("TGMK.")
	while True:
		lr = ls.pop()
		if ls:
			(Size, Rest) = divmod(Size, 1024)
		else:
			Rest = Size
		if Rest:
			ext.insert(0, "%d %sB." % (Rest, (lr if lr != "." else "")))
		if not (ls and Size):
			return str.join(chr(32), ext)

def enumerated_list(list):
	ls, Mumb = [], itypes.Number()
	for line in list:
		ls.append(AnsBase[12] % (Mumb.plus(), line))
	return str.join(chr(10), ls)

isNumber = lambda objt: (None if exec_(int, (objt,)) is None else True)

isSource = lambda data: IsJID.match(data)

def calculate(Numb = int()):
	if oSlist[0]:
		lines = get_pipe(sys_cmds[1] % (BsPid)).splitlines()
		if len(lines) >= 3:
			list = lines[3].split()
			if len(list) >= 6:
				Numb = "%s%s" % (list[4], list[5])
	else:
		lines = get_pipe(sys_cmds[0] % (BsPid)).splitlines()
		if len(lines) >= 2:
			Numb = lines[1].strip()
	return (int() if not isNumber(Numb) else int(Numb))

def check_copies():
	try:
		if not os.path.isfile(PidFile):
			raise SelfExc()
		try:
			Cache = eval(get_file(PidFile))
		except:
			del_file(PidFile); raise SelfExc()
		if BsPid == Cache["PID"]:
			Cache["alls"].append(strTime())
		elif oSlist[0]:
			get_pipe(sys_cmds[4] % (Cache["PID"])); raise SelfExc()
		else:
			os.kill(Cache["PID"], 9); raise SelfExc()
	except:
		Cache = {"PID": BsPid, "up": Info["sess"], "alls": []}
	exec_(cat_file, (PidFile, str(Cache)))
	del Cache["PID"]; Info.update(Cache)

def join_chats():
	if initialize_file(ChatsFile):
		try:
			Confs = eval(get_file(ChatsFile))
		except KeyboardInterrupt:
			raise KeyboardInterrupt("Interrupt (Ctrl+C)")
		except SyntaxError:
			del_file(ChatsFile)
			Confs = {}
			initialize_file(ChatsFile)
		except:
			Confs = {}
		Print("\n\nThere are %d rooms in list..." % len(Confs.keys()), color4)
		for conf in Confs.keys():
			Attrs = Confs[conf]
			Chats[conf] = sConf(conf, Attrs["disp"], Attrs["code"], Attrs["cPref"], Attrs["nick"], True)
			Chats[conf].load_all()
			if Clients.has_key(Chats[conf].disp):
				Chats[conf].join()
				Print("\n%s joined %s" % (Chats[conf].disp, conf), color3)
			else:
				Print("\nI'll join %s then %s would be connected..." % (conf, Chats[conf].disp), color1)
	else:
		Print("\n\nError: unable to create chatrooms list file!", color2)

# Presence Handler

def Xmpp_Presence_Cb(disp, stanza):
	Info["prs"].plus()
	(source, conf, stype, nick) = sAttrs(stanza)
	if not enough_access(conf, nick):
		xmpp_raise()
	if stype == Types[5]:
		disp = get_disp(disp)
		if Clients[disp].Roster:
			if enough_access(conf, nick, 7):
				Clients[disp].Roster.Authorize(conf)
				Clients[disp].Roster.setItem(conf, conf, ["Admins"])
				Clients[disp].Roster.Subscribe(conf)
			elif Roster["on"]:
				Clients[disp].Roster.Authorize(conf)
				Clients[disp].Roster.setItem(conf, conf, ["Users"])
				Clients[disp].Roster.Subscribe(conf)
			else:
				Sender(disp, xmpp.Presence(conf, Types[7]))
		xmpp_raise()
	elif Chats.has_key(conf):
		if stype == Types[7]:
			ecode = stanza.getErrorCode()
			if ecode:
				if ecode == eCodes[9]:
					Chats[conf].nick = "%s." % (nick)
					Chats[conf].join()
				elif ecode in [eCodes[5], eCodes[12]]:
					Chats[conf].IamHere = False
					TimerName = ejoinTimerName(conf)
					if TimerName not in iThr.ThrNames():
						try:
							composeTimer(360, ejoinTimer, TimerName, (conf,)).start()
						except:
							delivery(AnsBase[20] % (ecode, eCodesDesc[ecode], conf))
				elif ecode == eCodes[4]:
					Chats[conf].full_leave(eCodesDesc[ecode])
					delivery(AnsBase[21] % (ecode, eCodesDesc[ecode], conf))
				elif ecode in [eCodes[2], eCodes[6]]:
					Chats[conf].leave(eCodesDesc[ecode])
					delivery(AnsBase[22] % (ecode, eCodesDesc[ecode], conf))
		elif stype in [Types[3], None]:
			if Chats[conf].nick == nick:
				Chats[conf].IamHere = True
			Role = GetRole(stanza)
			instance = stanza.getJid()
			if not instance:
				if Chats[conf].isModer:
					Chats[conf].isModer = False
					if not Mserve:
						Chats[conf].change_status(AnsBase[23], sList[2])
						Msend(conf, AnsBase[24], disp)
						xmpp_raise()
				elif not Mserve:
					xmpp_raise()
			elif Chats[conf].isModer is False:
				if Chats[conf].nick == nick and aDesc.get(Role[0], 0) >= 2:
					Chats[conf].isModer = True
					Chats[conf].leave(AnsBase[25])
					time.sleep(0.4)
					Chats[conf].join()
				xmpp_raise()
			else:
				instance = (instance.split(chr(47)))[0].lower()
			if Chats[conf].isHereNow(nick) and Chats[conf].isHe(nick, instance):
				Chats[conf].aroles_change(nick, Role)
			else:
				Chats[conf].joined(nick, Role, instance)
				call_functions("04eh", (conf, nick, instance, Role, disp,))
		elif stype == Types[4]:
			scode = stanza.getStatusCode()
			if Chats[conf].nick == nick and scode in [sCodes[0], sCodes[2]]:
				Chats[conf].full_leave(sCodesDesc[scode])
				delivery(AnsBase[26] % (scode, conf, sCodesDesc[scode]))
				xmpp_raise()
			elif not Mserve and not stanza.getJid():
				xmpp_raise()
			elif scode == sCodes[1]:
				Nick = stanza.getNick()
				if Chats[conf].isHere(nick):
					Chats[conf].NewNick(nick, Nick)
				else:
					instance = stanza.getJid()
					if instance:
						instance = (instance.split(chr(47)))[0].lower()
					Role = GetRole(stanza)
					if Chats[conf].isHereNow(Nick) and Chats[conf].isHe(Nick, instance):
						Chats[conf].aroles_change(Nick, Role)
					else:
						Chats[conf].joined(Nick, Role, instance)
			else:
				status = (stanza.getReason() or stanza.getStatus())
				if Chats[conf].isHereNow(nick):
					Chats[conf].leaved(nick)
				call_functions("05eh", (conf, nick, status, scode, disp,))
		if Chats.has_key(conf):
			call_functions("02eh", (stanza, disp,))

# Iq Handler

def Xmpp_Iq_Cb(disp, stanza):
	Info["iq"].plus()
	ResponseChecker(disp, stanza)
	(source, instance, stype, nick) = sAttrs(stanza)
	if not enough_access(instance, nick):
		xmpp_raise()
	if stype == Types[10]:
		Name = stanza.getQueryNS()
		if not Name:
			Name = (stanza.getTag(Types[16]) or stanza.getTag(Types[17]))
			if Name:
				Name = Name.getNamespace()
		if Features.count(Name):
			answer = stanza.buildReply(Types[8])
			if Name == Features[5]:
				query = answer.getTag(Types[18])
				query.addChild("identity", {"category": "client",
											"type": "bot",
											"name": ProdName[:10]})
				for Feature in aFeatures:
					query.addChild("feature", {"var": Feature})
			elif Name == Features[4]:
				query = answer.getTag(Types[18])
				query.setAttr("seconds", int(time.time() - VarCache["idle"]))
				query.setData(VarCache["action"])
			elif Name == Features[0]:
				query = answer.getTag(Types[18])
				query.setTagData("name", ProdName)
				query.setTagData("version", ProdVer)
				PyVer = str(sys.version).split()[0]
				if oSlist[0]:
					os_name = get_pipe(sys_cmds[5]).strip()
				elif oSlist[1]:
					os_name = os.uname()[0]
				else:
					os_name = "Os[%s]" % (BotOs)
				query.setTagData("os", "%s / PyVer[%s]" % (os_name, PyVer))
			elif Name == Features[2]:
				query = answer.getTag(Types[18])
				utc = strTime("%Y%m%dT%H:%M:%S", False)
				tz = strTime("%Z")
				if oSlist[0]:
					tz = tz.decode("cp1251")
				dis = strTime("%a, %d %b %Y %H:%M:%S UTC")
				query.setTagData("utc", utc)
				query.setTagData("tz", tz)
				query.setTagData("display", dis)
			elif Name == Features[3]:
				query = answer.addChild(Types[17], {}, [], Features[3])
				query.setTagData("utc", strTime("%Y-%m-%dT%H:%M:%SZ", False))
				TimeZone = (time.altzone if time.daylight else time.timezone)
				query.setTagData("tzo", "%s%02d:%02d" % (((TimeZone < 0) and "+" or "-"),
											abs(TimeZone) / 3600,
											abs(TimeZone) / 60 % 60))
			Sender(disp, answer)
			xmpp_raise()
	call_functions("03eh", (stanza, disp,))

# Message Handler

def Xmpp_Message_Cb(disp, stanza):
	Info["msg"].plus()
	(source, instance, stype, nick) = sAttrs(stanza)
	if not enough_access(instance, nick):
		xmpp_raise()
	if stanza.getTimestamp():
		xmpp_raise()
	isConf = Chats.has_key(instance)
	if not isConf:
		CheckFlood(disp)
	if not Mserve and isConf and Chats[instance].isModer is False:
		xmpp_raise()
	BotNick = (DefNick if not isConf else Chats[instance].nick)
	if nick == BotNick:
		xmpp_raise()
	body = stanza.getBody()
	if body:
		body = body.strip()
	if not body:
		xmpp_raise()
	if len(body) > IncLimit:
		body = "%s[...] %d symbols limit." % (body[:IncLimit].strip(), IncLimit)
	stype = stanza.getType()
	if stype == Types[7]:
		ecode = stanza.getErrorCode()
		if ecode in [eCodes[10], eCodes[7]]:
			if ecode == eCodes[7]:
				if not isConf:
					xmpp_raise()
				Chats[instance].join()
				time.sleep(0.6)
			Msend(source, body)
		xmpp_raise()
	if stype != Types[1]:
		if (stanza.getTag(Types[22])):
			answer = xmpp.Message(source)
			answer.setTag(Types[11], namespace = xmpp.NS_RECEIPTS)
			answer.setID(stanza.getID())
			Sender(disp, answer)
		stype = Types[0]
	cbody, isToBs, Parameters = body, (stype == Types[0]), ""
	for x in ["%s%s" % (BotNick, Key) for Key in [":",",",">"]]:
		if cbody.startswith(x):
			cbody, isToBs = cbody[len(x):].lstrip(), True
			break
	if not cbody:
		xmpp_raise()
	command = cbody.split()[0].lower()
	if not isToBs and isConf and Chats[instance].cPref and command not in sCmds:
		if Chats[instance].cPref == command[:1]:
			command = command[1:]
		else:
			command = False
	elif isToBs and not Cmds.has_key(command) and (command[:1] in cPrefs):
		command = command[1:]
	if isConf and command in Chats[instance].oCmds:
		xmpp_raise()
	if Cmds.has_key(command):
		VarCache["action"] = AnsBase[27] % (command.upper())
		if cbody.count(chr(32)):
			Parameters = cbody[(cbody.find(chr(32)) + 1):].strip()
		VarCache["idle"] = time.time()
		Cmds[command].execute(stype, (source, instance, nick), Parameters, disp)
	else:
		call_functions("01eh", (stanza, isConf, stype, (source, instance, nick), body, isToBs, disp,))

# Connecting Clients & Dispatching

def connect_client(source, InstanceAttrs):
	(server, cport, host, user, code) = InstanceAttrs
	disp = xmpp.Client(host, cport, None)
	Print("\n\n'%s' connecting..." % (source), color4)
	if ConTls:
		ConType = disp.connect((server, cport), None, None, False)
	else:
		ConType = disp.connect((server, cport), None, False, True)
	if ConType:
		ConType = ConType.upper()
		if ConTls and ConType != "TLS":
			Print("\n'%s' was connected, but connection isn't secure." % (source), color1)
		else:
			Print("\n'%s' was successfully connected!" % (source), color3)
		Print("\n'%s' using - '%s'" % (source, ConType), color4)
	else:
		Print("\n'%s' can't connect to '%s' (Port: %s). I will retry later..." % (source, server.upper(), str(cport)), color2)
		return (False, False)
	Print("\n'%s' authenticating..." % (source), color4)
	try:
		Auth = disp.auth(user, code, GenResource)
	except KeyboardInterrupt:
		raise KeyboardInterrupt("Interrupt (Ctrl+C)")
	except:
		eBody = exc_info()
		Print("Can't authenticate '%s'!\n\t'%s' - %s" % (source, eBody[0], eBody[1]), color2)
		return (False, eCodes[2])
	if Auth:
		if Auth == "sasl":
			Print("\n'%s' was successfully authenticated!" % (source), color3)
		else:
			Print("\n'%s' was authenticated, but old auth method was used...", color1)
	else:
		eBody = str(disp.lastErr)
		eCode = str(disp.lastErrCode)
		Print("Can't authenticate '%s'! Error: '%s' (%s)" % (source, eCode, eBody), color2)
		return (False, eCode)
	try:
		disp.getRoster()
	except IOError:
		if disp.isConnected():
			disp.Roster = None
		else:
			return (False, False)
	except:
		disp.Roster = None
	disp.RespExp = {}
	disp.RegisterHandler(xmpp.NS_PRESENCE, Xmpp_Presence_Cb)
	disp.RegisterHandler(xmpp.NS_IQ, Xmpp_Iq_Cb)
	disp.RegisterHandler(xmpp.NS_MESSAGE, Xmpp_Message_Cb)
	Clients[source] = disp
	Sender(disp, caps_add(xmpp.Presence(show = sList[0], status = DefStatus)))
	return (True, source)

def connectAndDispatch(disp):
	if Reverse_disp(disp, False):
		time.sleep(60)
		for conf in Chats.keys():
			if disp == Chats[conf].disp:
				Chats[conf].join()
		Dispatch_handler(disp)
	else:
		delivery(AnsBase[28] % (disp))

def connect_clients():
	for Inctance, Attrs in InstansesDesc.items():
		conn = connect_client(Inctance, Attrs)
		if not conn[0]:
			if conn[1] and conn[1] == eCodes[2]:
				continue
			composeTimer(60, connectAndDispatch, "%s%s" % (Types[13], Inctance), (Inctance,)).start()

def Reverse_disp(disp, chats_ = True):
	Iters = itypes.Number()
	while 1440 > Iters.plus():
		if connect_client(disp, InstansesDesc[disp])[0]:
			if chats_:
				for conf in Chats.keys():
					if disp == Chats[conf].disp:
						Chats[conf].join()
			return True
		else:
			time.sleep(60)

def Dispatch_handler(disp):
	ZeroCycles = itypes.Number()
	while VarCache["alive"]:
		try:
			Cycle = Clients[disp].iter()
			if not Cycle:
				Cycles = ZeroCycles.plus()
				if Cycles >= 16:
					raise IOError("disconnected!")
		except KeyboardInterrupt:
			break
		except iThr.ThrKill:
			break
		except IOError:
			if not Reverse_disp(disp):
				delivery(AnsBase[28] % (disp))
				break
			ZeroCycles = itypes.Number()
		except xmpp.Conflict:
			delivery(AnsBase[29] % (disp))
			break
		except xmpp.SystemShutdown:
			if not Reverse_disp(disp):
				delivery(AnsBase[28] % (disp))
				break
			ZeroCycles = itypes.Number()
		except xmpp.StreamError:
			pass
		except:
			Dispatch_fail()
			if Info["errors"].plus() >= len(Clients.keys())*8:
				sys_exit("Dispatch Errors!")

# load_mark2 & exit

def load_mark2():
	Print("\n\n%s\n\n" % (FullName), color3)
	check_copies()
	load_expansions()
	call_sfunctions("00si")
	connect_clients()
	while len(Clients.keys()) is 0:
		pass
	Print("\n\nYahoo! I am online!", color3)
	join_chats()
	Print("\n\n%s is ready to serve!\n\n" % (ProdName), color3)
	call_sfunctions("02si")
	for disp in Clients.keys():
		ThrName = "%s%s" % (Types[13], disp)
		if ThrName not in iThr.ThrNames():
			composeThr(Dispatch_handler, ThrName, (disp,)).start()
	while VarCache["alive"]:
		time.sleep(180)
		Cls = itypes.Number()
		for Name in iThr.ThrNames():
			if Name.startswith(Types[13]):
				Cls.plus()
		if 0 is Cls._int():
			sys_exit("All clients was fallen!")
		sys.exc_clear()
		gc.collect()
		if MaxMemory and MaxMemory <= calculate():
			sys_exit("Memory leak...")

def sys_exit(exit_desclr = "Suicide!"):
	VarCache["alive"] = False
	Print("\n\n%s" % (exit_desclr), color2)
	iThr.Threads_kill()
	for disp in Clients.keys():
		if online(disp):
			sUnavailable(disp, exit_desclr)
	call_sfunctions("03si")
	Exit("\n\nReloading...\n\nPress Ctrl+C to exit", 0, 30)

if __name__ == "__main__":
	try:
		load_mark2()
	except KeyboardInterrupt:
		sys_exit("Interrupt (Ctrl+C)")
	except:
		lytic_crashlog(load_mark2)
		sys_exit("Critical Feil!")

# The End is Near =>