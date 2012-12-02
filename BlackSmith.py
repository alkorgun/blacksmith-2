#!/usr/bin/python
# coding: utf-8

# BlackSmith's core mark.2
# BlackSmith.py

# Code © (2010-2012) by WitcherGeralt [alkorgun@gmail.com]

# imports

from types import NoneType, UnicodeType, InstanceType
from traceback import print_exc as exc_info__
from random import shuffle, randrange, choice
from re import compile as compile__

import sys, os, gc, time, shutil, ConfigParser

BsCore = getattr(sys.modules["__main__"], "__file__", None)
if BsCore:
	BsCore = os.path.abspath(BsCore)
	BsRoot = os.path.dirname(BsCore)
	if BsRoot:
		os.chdir(BsRoot)
else:
	BsRoot = os.getcwd()
ZipLib = "librarys.zip"
sys.path.insert(0, ZipLib)

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

Types = (
	"chat", # 0
	"groupchat", # 1
	"normal", # 2
	"available", # 3
	"unavailable", # 4
	"subscribe", # 5
	"answer", # 6
	"error", # 7
	"result", # 8
	"set", # 9
	"get", # 10
	"jid", # 11
	"nick", # 12
	"dispatch", # 13
	"request", # 14
	"received", # 15
	"ping", # 16
	"time", # 17
	"query" # 18
				)

aRoles = (
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
				)

sList = (
	"chat", # готов поболтать
	"away", # отошел
	"xa", # не беспокоить
	"dnd" # недоступен
				)

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

IqXEPs = (
	xmpp.NS_VERSION, # 0
	xmpp.NS_PING, # 1
	xmpp.NS_TIME, # 2
	xmpp.NS_URN_TIME, # 3
	xmpp.NS_LAST, # 4
	xmpp.NS_DISCO_INFO # 5
				)

XEPs = set(IqXEPs + (
	xmpp.NS_CAPS,
	xmpp.NS_SASL,
	xmpp.NS_TLS,
	xmpp.NS_MUC,
	xmpp.NS_ROSTER,
	xmpp.NS_RECEIPTS
				))

isJID = compile__(".+?@[\w-]+?\.[\w-]+?", 32)

VarCache = {
	"idle": 0.24,
	"alive": True,
	"errors": [],
	"action": "# %s %s &" % (os.path.basename(sys.executable), BsCore)
				}

Info = {
	"cmd": itypes.Number(),		"sess": time.time(),
	"msg": itypes.Number(),		"alls": [],
	"cfw": itypes.Number(),		"up": 1.24,
	"prs": itypes.Number(),		"iq": itypes.Number(),
	"errors": itypes.Number(),
	"omsg": itypes.Number(),	"outiq": itypes.Number()
				}

# Useful features

class SelfExc(Exception):
	pass

def exc_info():
	exc = sys.exc_info()
	return (exc[0].__name__ if exc[0] else str(exc[0]), str(exc[1]))

def exc_info_(fp = None):
	try:
		exc_info__(None, fp)
	except:
		pass

sleep, database = time.sleep, itypes.Database

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
		color = None
	return (body, color)

def text_color(text, color):
	if eColors and color:
		text = color+text+color0
	return text

def Print(text, color = None):
	try:
		print text_color(text, color)
	except:
		pass

def try_sleep(slp):
	try:
		sleep(slp)
	except KeyboardInterrupt:
		os._exit(0)
	except:
		pass

def Exit(text, exit, slp):
	Print(text, color2); try_sleep(slp)
	if exit:
		os._exit(0)
	else:
		os.execl(sys.executable, sys.executable, BsCore)

try:
	reload(sys)
	sys.setdefaultencoding("utf-8")
except:
	Print("\n\nError: can't set default encoding!", color2)

stdout = "stdout.tmp"
if not sys.stdin.isatty():
	if os.path.isfile(stdout):
		if os.path.getsize(stdout) >= 131072:
			stdout = open(stdout, "wb", 0)
		else:
			stdout = open(stdout, "ab", 0)
	else:
		stdout = open(stdout, "wb", 0)
	sys.stdout = stdout
	sys.stderr = stdout
	if eColors:
		eColors = not eColors
else:
	stdout = sys.stdout

# Important Variables

static = "static/%s"
dynamic = "current/%s"
ExpsDir = "expansions"
FailDir = "exceptions"
PidFile = "sessions.db"
GenCrash = "dispatcher.crash"
SvnCache = ".svn/entries"
GenInscFile = static % ("insc.py")
GenConFile = static % ("config.ini")
ConDispFile = static % ("clients.ini")
ChatsFile = dynamic % ("chats.db")

(BsMark, BsVer, BsRev) = (2, 39, 0)

if os.access(SvnCache, os.R_OK):
	Cache = open(SvnCache).readlines()
	if len(Cache) >= 4:
		BsRev = Cache[3].strip()
		if BsRev.isdigit():
			BsRev = int(BsRev)
		else:
			BsRev = 0

ProdName = "BlackSmith mark.%d" % (BsMark)
ProdVer = "%d (r.%s)" % (BsVer, BsRev)
Caps = "http://blacksmith-2.googlecode.com/svn/"
CapsVer = "%d.%d" % (BsMark, BsVer)
FullName = "HellDev's %s Ver.%s (%s)" % (ProdName, ProdVer, Caps)

BotOs, BsPid = os.name, os.getpid()

oSlist = ((BotOs == "nt"), (BotOs == "posix"))

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
	GenDisp, Instance = client_config(GenCon, "CLIENT")
	InstansesDesc = {GenDisp: Instance}
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
		for Block in ConDisp.sections():
			Disp, Instance = client_config(ConDisp, Block)
			InstansesDesc[Disp] = Instance
except:
	Exit("\n\nOne of the configuration files is corrupted!", 1, 30)

del Instance

MaxMemory = (32768 if (MaxMemory and MaxMemory <= 32768) else MaxMemory)

try:
	execfile(GenInscFile)
except:
	Exit("\n\nError: general inscript is damaged!", 1, 30)

if oSlist[0]:
	os.system(sys_cmds[2])
	os.system("%s %s" % (sys_cmds[3], FullName))

# lists & dicts

expansions = {}
Cmds = {}
cPrefs = ("!", "@", "#", ".", "*")
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
	"05eh": [], "06eh": [],
	"07eh": [], "08eh": [],
	"09eh": [], "00si": [],
	"01si": [], "02si": [],
	"03si": [], "04si": []
				}

Sequence = iThr.Semaphore()

# call & execute Threads & handlers

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
		collectExc(handler_instance, command)

def call_sfunctions(ls, list = ()):
	for inst in Handlers[ls]:
		execute_handler(inst, list)

def composeTimer(sleep, handler, Name = None, list = (), command = None):
	if not Name:
		Name = "iTimer-%d" % (iThr.aCounter._int())
	Timer = iThr.Timer(sleep, execute_handler, (handler, list, command,))
	Timer.name = Name
	return Timer

def composeThr(handler, Name, list = (), command = None):
	if not Name.startswith(Types[13]):
		Name = "%s-%d" % (Name, iThr.aCounter._int())
	return iThr.KThread(execute_handler, Name, (handler, list, command,))

def Try_Thr(Thr, Number = 0):
	if Number >= 4:
		raise RuntimeError("exit")
	try:
		Thr.start()
	except iThr.error:
		Try_Thr(Thr, (Number + 1))
	except:
		collectExc(Thr.start)

def sThread_Run(Thr, handler, command = None):
	try:
		Thr.start()
	except iThr.error:
		try:
			Try_Thr(Thr)
		except RuntimeError:
			try:
				Thr._run_backup()
			except KeyboardInterrupt:
				raise KeyboardInterrupt("Interrupt (Ctrl+C)")
			except:
				collectExc(handler, command)
	except:
		collectExc(sThread_Run, command)

def sThread(name, inst, list = (), command = None):
	sThread_Run(composeThr(inst, name, list, command), inst, command)

def call_efunctions(ls, list = ()):
	for inst in Handlers[ls]:
		sThread(ls, inst, list)

# expansions & commands

class expansion(object):

	commands, handlers = (), ()

	def __init__(self, name):
		self.name = name
		self.path = os.path.join(ExpsDir, self.name)
		self.file = os.path.join(self.path, "code.py")
		self.isExp = os.path.isfile(self.file)
		self.insc = os.path.join(self.path, "insc.py")
		if not os.path.isfile(self.insc):
			self.insc = None
		self.cmds = []
		self.desc = {}

	def initialize_exp(self):
		expansions[self.name] = (self)
		if self.insc:
			try:
				self.AnsBase = AnsBase_temp
			except NameError:
				pass
		for ls in self.commands:
			command_handler(self, *ls)
		for inst, ls in self.handlers:
			self.handler_register(getattr(self, inst.func_name), ls)

	def dels(self, full = False):
		while self.cmds:
			cmd = self.cmds.pop()
			if Cmds.has_key(cmd):
				Cmds[cmd].off()
		self.funcs_del()
		self.commands = ()
		self.handlers = ()
		if full and expansions.has_key(self.name):
			del expansions[self.name]

	def ls_add(self, ls):
		if not self.desc.has_key(ls):
			self.desc[ls] = []

	def funcs_del(self, handler = None):

		def Del(inst, ls):
			if ls == "03si":
				execute_handler(inst)
			self.inst_del(ls, inst)
			list = self.desc[ls]
			list.remove(inst)
			if not list:
				del self.desc[ls]

		if handler:
			for ls, list in sorted(self.desc.items()):
				for inst in list:
					if inst == handler:
						handler = Del(inst, ls)
						break
				if not handler:
					break
		else:
			for ls, list in sorted(self.desc.items()):
				for inst in list:
					Del(inst, ls)

	def initialize_all(self):
		for ls, list in sorted(self.desc.items()):
			if not ls.endswith("si"):
				continue
			for inst in list:
				if ls in ("00si", "02si"):
					execute_handler(inst)
				elif ls == "01si":
					for conf in Chats.keys():
						execute_handler(inst, (conf,))

	def func_add(self, ls, inst):
		self.ls_add(ls)
		self.desc[ls].append(inst)

	def load(self):
		if expansions.has_key(self.name):
			expansions[self.name].dels()
		try:
			if self.insc:
				execfile(self.insc, globals())
			execfile(self.file, globals())
			exp_inst = expansion_temp(self.name)
		except:
			exp = (None, exc_info())
		else:
			exp = (exp_inst, ())
		return exp

	def inst_add(self, ls, inst):
		if inst not in Handlers[ls]:
			Handlers[ls].append(inst)

	def inst_del(self, ls, inst):
		if inst in Handlers[ls]:
			Handlers[ls].remove(inst)

	def handler_register(self, inst, ls):
		Name = inst.func_name
		for instance in Handlers[ls]:
			if Name == instance.func_name:
				self.inst_del(ls, instance)
		self.inst_add(ls, inst)
		self.func_add(ls, inst)

class Command(object):

	def __init__(self, inst, name, access, help, exp):
		self.exp = exp
		self.numb = itypes.Number()
		self.name = name
		self.isAvalable = True
		self.help = help
		self.handler = inst
		self.desc = []
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

	def execute(self, stype, source, body, disp):
		if enough_access(source[1], source[2], self.access):
			if self.isAvalable and self.handler:
				Info["cmd"].plus()
				sThread("command", self.handler, (self.exp, stype, source, body, disp), self.name)
				self.numb.plus()
				source = get_source(source[1], source[2])
				if source and source not in self.desc:
					self.desc.append(source)
			else:
				Answer(AnsBase[19] % (self.name), stype, source, disp)
		else:
			Answer(AnsBase[10], stype, source, disp)

def command_handler(exp_inst, handler, name, access, prefix = True):
	Path = os.path.join(ExpsDir, exp_inst.name, name)
	try:
		commands = eval(get_file("%s.name" % Path).decode("utf-8"))
	except:
		commands = {}
	if commands.has_key(DefLANG):
		name = commands[DefLANG].decode("utf-8")
		help = "%s.%s" % (Path, DefLANG.lower())
	else:
		help = "%s.en" % (Path)
	if Cmds.has_key(name):
		Cmds[name].reload(handler, access, help, exp_inst)
	else:
		Cmds[name] = Command(handler, name, access, help, exp_inst)
	if not prefix and name not in sCmds:
		sCmds.append(name)
	exp_inst.cmds.append(name)

# Chats, Users & Other

class sUser(object):

	def __init__(self, nick, role, source, access = None):
		self.nick = nick
		self.source = source
		self.role = role
		self.ishere = True
		self.date = (time.time(), Yday(), strfTime(local = False))
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

class sConf(object):

	def __init__(self, name, disp, code = None, cPref = None, nick = DefNick, added = False):
		self.name = name
		self.disp = disp
		self.nick = nick
		self.code = code
		self.more = ""
		self.desc = {}
		self.IamHere = None
		self.isModer = True
		self.sdate = 0
		self.alist = {}
		self.oCmds = []
		self.cPref = cPref
		self.status = DefStatus
		self.state = sList[0]
		if not added:
			self.save()

	def load_all(self):
		call_sfunctions("01si", (self.name,))

	def csend(self, stanza):
		Sender(self.disp, stanza)

	isHere = lambda self, nick: self.desc.has_key(nick)

	isHereTS = lambda self, nick: (self.desc[nick].ishere if self.isHere(nick) else False)

	get_user = lambda self, nick: self.desc.get(nick)

	isHe = lambda self, nick, source: (source == self.desc[nick].source)

	get_nicks = lambda self: self.desc.keys()

	sorted_users = lambda self: [self.get_user(nick) for nick in sorted(self.get_nicks())]

	get_users = lambda self: self.desc.values()

	def sjoined(self, nick, role, source, stanza):
		access = Galist.get(source, None)
		if not access and access != 0:
			access = self.alist.get(source, None)
		self.desc[nick] = sUser(nick, role, source, access)
		call_efunctions("04eh", (self.name, nick, source, role, stanza, self.disp,))

	def aroles_change(self, nick, role, stanza):
		sUser = self.get_user(nick)
		if sUser.aroles(role):
			if not Galist.has_key(sUser.source):
				if not self.alist.has_key(sUser.source):
					sUser.calc_acc()
			call_efunctions("07eh", (self.name, nick, role, self.disp,))
		else:
			call_efunctions("08eh", (self.name, nick, stanza, self.disp,))

	def set_nick(self, old_nick, nick):
		self.desc[nick] = self.desc.pop(old_nick)
		self.desc[nick].nick = nick
		call_efunctions("06eh", (self.name, old_nick, nick, self.disp,))

	def sleaved(self, nick):
		self.desc[nick].ishere = False

	def composePres(self):
		stanza = xmpp.Presence("%s/%s" % (self.name, self.nick))
		stanza.setShow(self.state)
		stanza.setStatus(self.status)
		return caps_add(stanza)

	def join(self):
		for sUser in self.get_users():
			sUser.ishere = False
		stanza = self.composePres()
		self.sdate = time.time()
		node = xmpp.Node("x")
		node.setNamespace(xmpp.NS_MUC)
		node.addChild("history", {"maxchars": "0"})
		if self.code:
			node.setTagData("password", self.code)
		stanza.addChild(node = node)
		self.csend(stanza)

	def subject(self, body):
		self.csend(xmpp.Message(self.name, "", Types[1], body))

	def set_status(self, state, status):
		self.state, self.status = (state, status)

	def change_status(self, state, status):
		self.set_status(state, status)
		self.csend(self.composePres())

	def save_stats(self):
		call_sfunctions("03si", (self.name,))

	def leave(self, exit_status = None):
		self.IamHere = None
		self.isModer = True
		self.more = ""
		stanza = xmpp.Presence(self.name, Types[4])
		if exit_status:
			stanza.setStatus(exit_status)
		self.csend(stanza)

	def full_leave(self, status = None):
		self.leave(status)
		del Chats[self.name]
		self.save_stats()
		self.save(False)
		call_sfunctions("04si", (self.name,))
		if ChatsAttrs.has_key(self.name):
			del ChatsAttrs[self.name]

	def save(self, RealSave = True):
		if initialize_file(ChatsFile):
			list = eval(get_file(ChatsFile))
			if not RealSave:
				if list.has_key(self.name):
					del list[self.name]
			else:
				list[self.name] = {"disp": self.disp, Types[12]: self.nick, "cPref": self.cPref, "code": self.code}
			cat_file(ChatsFile, str(list))
		else:
			delivery(self.name)

	def iq_sender(self, attr, data, afrls, role, reason = str(), handler = None):
		stanza = xmpp.Iq(to = self.name, typ = Types[9])
		stanza.setID("Bs-i%d" % Info["outiq"].plus())
		query = xmpp.Node(Types[18])
		query.setNamespace(xmpp.NS_MUC_ADMIN)
		arole = query.addChild("item", {attr: data, afrls: role})
		if reason:
			arole.setTagData("reason", reason)
		stanza.addChild(node = query)
		if not handler:
			self.csend(stanza)
		else:
			handler, kdesc = handler
			if not handler:
				handler = HandleResponse
				kdesc = {"source": kdesc}
			CallForResponse(self.disp, stanza, handler, kdesc)

	def outcast(self, jid, reason = str(), handler = ()):
		self.iq_sender(Types[11], jid, aRoles[0], aRoles[1], reason, handler)

	def none(self, jid, reason = str(), handler = ()):
		self.iq_sender(Types[11], jid, aRoles[0], aRoles[2], reason, handler)

	def member(self, jid, reason = str(), handler = ()):
		self.iq_sender(Types[11], jid, aRoles[0], aRoles[3], reason, handler)

	def admin(self, jid, reason = str(), handler = ()):
		self.iq_sender(Types[11], jid, aRoles[0], aRoles[4], reason, handler)

	def owner(self, jid, reason = str(), handler = ()):
		self.iq_sender(Types[11], jid, aRoles[0], aRoles[5], reason, handler)

	def kick(self, nick, reason = str(), handler = ()):
		self.iq_sender(Types[12], nick, aRoles[6], aRoles[2], reason, handler)

	def visitor(self, nick, reason = str(), handler = ()):
		self.iq_sender(Types[12], nick, aRoles[6], aRoles[7], reason, handler)

	def participant(self, nick, reason = str(), handler = ()):
		self.iq_sender(Types[12], nick, aRoles[6], aRoles[8], reason, handler)

	def moder(self, nick, reason = str(), handler = ()):
		self.iq_sender(Types[12], nick, aRoles[6], aRoles[9], reason, handler)

def get_source(source, nick):
	if source in Chats:
		source = getattr(Chats[source].get_user(nick), "source", None)
	return source

def get_access(source, nick):
	if source in Chats:
		access = getattr(Chats[source].get_user(nick), "access", 0)
	else:
		access = Galist.get(source, 2)
	return access

enough_access = lambda conf, nick, access = 0: (access <= get_access(conf, nick))

object_encode = lambda obj: (obj if isinstance(obj, UnicodeType) else str(obj).decode("utf-8", "replace"))

def delivery(body):
	try:
		Disp, body = GenDisp, object_encode(body)
		if not online(Disp):
			for disp in Clients.keys():
				if GenDisp != disp and online(disp):
					Disp = disp
					break
			if not online(Disp):
				raise SelfExc("disconnected!")
		Info["omsg"].plus()
		Clients[Disp].send(xmpp.Message(GodName, body, Types[0]))
	except IOError:
		Print("\n\n%s" % (body), color1)
	except SelfExc:
		Print("\n\n%s" % (body), color1)
	except:
		exc_info_()

def Message(inst, body, disp = None):
	body = object_encode(body)
	if Chats.has_key(inst):
		stype = Types[1]
		if not disp:
			disp = Chats[inst].disp
		if len(body) > ConfLimit:
			Chats[inst].more = body[ConfLimit:].strip()
			body = AnsBase[18] % (body[:ConfLimit].strip(), ConfLimit)
	else:
		stype = Types[0]
		if not disp:
			if isinstance(inst, xmpp.JID):
				chat = inst.getStripped()
			else:
				chat = (inst.split(chr(47)))[0].lower()
			if Chats.has_key(chat):
				disp = Chats[chat].disp
			else:
				disp = GenDisp
		if len(body) > PrivLimit:
			Number, all = itypes.Number(), str(len(body) / PrivLimit + 1)
			while len(body) > PrivLimit:
				Info["omsg"].plus()
				Sender(disp, xmpp.Message(inst, "[%d/%s] %s[...]" % (Number.plus(), all, body[:PrivLimit].strip()), stype))
				body = body[PrivLimit:].strip()
				sleep(2)
			body = "[%d/%s] %s" % (Number.plus(), all, body)
	Info["omsg"].plus()
	Sender(disp, xmpp.Message(inst, body.strip(), stype))

def Answer(body, stype, source, disp = None):
	if stype == Types[0]:
		instance = source[0]
	else:
		body = "%s: %s" % (source[2], object_encode(body))
		instance = source[1]
	Message(instance, body, disp)

def CheckFlood(disp):
	disp = get_disp(disp)
	if not Flood.has_key(disp):
		Flood[disp] = []
	Flood[disp].append(time.time())
	if len(Flood[disp]) >= 4:
		if (Flood[disp][-1] - Flood[disp][0]) <= 8:
			Flood[disp] = [Flood[disp].pop()]
			xmpp_raise()
		else:
			Flood[disp].pop(0)

def IdleClient():
	cls = dict()
	for disp in Clients.keys():
		if online(disp):
			cls[disp] = 0
	for conf in Chats.itervalues():
		disp = conf.disp
		if cls.has_key(disp):
			cls[disp] += 1
	if cls:
		idle = min(cls.values())
		for disp, chats in cls.items():
			if chats == idle:
				return disp
	return GenDisp

def ejoinTimer(conf):
	if Chats.has_key(conf):
		Chats[conf].join()

ejoinTimerName = lambda conf: "%s-%s" % (ejoinTimer.func_name, conf.decode("utf-8"))

get_disp = lambda disp: "%s@%s" % (disp._owner.User, disp._owner.Server) if isinstance(disp, (xmpp.Client, xmpp.dispatcher.Dispatcher)) else disp

get_nick = lambda chat: getattr(Chats.get(chat), Types[12], DefNick)

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

def HandleResponse(disp, stanza, source):
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
		collectExc(Sender)

sUnavailable = lambda disp, data: Sender(disp, xmpp.Presence(typ = Types[4], status = data))

def caps_add(Node):
	Node.setTag("c", {"node": Caps, "ver": CapsVer}, xmpp.NS_CAPS)
	return Node

Yday = lambda: getattr(time.gmtime(), "tm_yday")

def sAttrs(stanza):
	source = stanza.getFrom()
	instance = source.getStripped()
	resource = source.getResource()
	stype = stanza.getType()
	return (source, instance.lower(),
					stype, resource)

GetRole = lambda Node: (str(Node.getAffiliation()), str(Node.getRole()))

def xmpp_raise():
	raise xmpp.NodeProcessed("continue")

# Connect with FS

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
	with open(cefile(filename), "r") as fp:
		return fp.read()

def cat_file(filename, data, otype = "wb"):
	with Sequence:
		with open(cefile(filename), otype) as fp:
			fp.write(data)

# Crashlogs

def collectDFail():
	crashfile = open(GenCrash, "ab")
	exc_info_(crashfile)
	crashfile.close()

def collectExc(instance, command = None):
	Number, instance, error_body = (len(VarCache["errors"]) + 1), instance.func_name, get_exc()
	VarCache["errors"].append(error_body)
	if GetExc and online(GenDisp):
		if command:
			exception = AnsBase[13] % (command, instance)
		else:
			exception = AnsBase[14] % (instance)
		delivery(AnsBase[15] % exception)
	else:
		Print("\n\nError: can't execute '%s'!" % (instance), color2)
	filename = "%s/error[%d]%s.crash" % (FailDir, (Info["cfw"]._int() + 1), strfTime("[%H.%M.%S][%d.%m.%Y]"))
	try:
		if not os.path.exists(FailDir):
			os.mkdir(FailDir, 0755)
		crashfile = open(filename, "wb")
		Info["cfw"].plus()
		exc_info_(crashfile)
		crashfile.close()
		if GetExc and online(GenDisp):
			if oSlist[0]:
				delivery(AnsBase[16] % (Number, filename))
			else:
				delivery(AnsBase[17] % (Number, filename))
		else:
			Print("\n\nCrash file --> %s\nError's number --> %d" % (filename, Number), color2)
	except:
		exc_info_()
		if GetExc and online(GenDisp):
			delivery(error_body)
		else:
			Print(*try_body(error_body, color2))

# Other functions

def load_expansions():
	Print("\n\nExpansions loading...\n", color4)
	for ExpDir in sorted(os.listdir(ExpsDir)):
		if (".svn" == ExpDir) or not os.path.isdir(os.path.join(ExpsDir, ExpDir)):
			continue
		exp = expansion(ExpDir)
		if exp.isExp:
			exp, exc = exp.load()
			if exp:
				try:
					exp.initialize_exp()
				except:
					exc = exc_info()
					exp.dels(True)
					Print("Can't init - %s!%s" % (ExpDir, "\n\t* %s: %s" % exc), color2)
				else:
					Print("%s - successfully loaded!" % (ExpDir), color3)
			else:
				Print("Can't load - %s!%s" % (ExpDir, "\n\t* %s: %s" % exc), color2)
		else:
			Print("%s - isn't an expansion!" % (ExpDir), color2)

def get_pipe(command):
	try:
		with os.popen(command) as pipe:
			data = pipe.read()
		if oSlist[0]:
			data = data.decode("cp866")
	except:
		data = "(...)"
	return data

class Web:

	import urllib as One, urllib2 as Two

	Opener = Two.build_opener()

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

	def open(self, header = ()):
		dest = self.Two.Request(self.link)
		if header:
			self.add_header(*header)
		if self.headers:
			for header, desc in self.headers.iteritems():
				dest.add_header(header, desc)
		return self.Opener.open(dest)

	def download(self, filename = None, folder = None, handler = None, fb = None, header = ()):
		fp = self.open(header)
		info = fp.info()
		size = info.get("Content-Length", -1)
		if isNumber(size):
			size = int(size)
		else:
			raise SelfExc("no info about file's size")
		if not filename:
			if info.has_key("Content-Disposition"):
				disp = info.get("Content-Disposition")
				comp = compile__("filename=[\"']+?(.+?)[\"']+?")
				disp = comp.search(disp)
				if disp:
					filename = (disp.group(1)).decode("utf-8")
		if not filename:
			filename = self.One.unquote_plus(fp.url.split("/")[-1].split("?")[0].replace("%25", "%"))
			if not filename:
				raise SelfExc("can't get filename")
		if folder:
			filename = os.path.join(folder, filename)
		if AsciiSys:
			filename = filename.encode("utf-8")
		blockSize = 8192
		blockNumb = 0
		read = 0
		with open(filename, "wb") as dfp:
			while VarCache["alive"]:
				if handler:
					execute_handler(handler, (info, blockNumb, blockSize, size, fb))
				data = fp.read(blockSize)
				if not data:
					break
				dfp.write(data)
				blockNumb += 1
				read += len(data)
		if size >= 0 and read < size:
			raise SelfExc("file is corrupt, lost %d bytes" % (size - read))
		if AsciiSys:
			filename = filename.decode("utf-8")
		return (filename, info, size)

	get_page = lambda self, header = (): self.open(header).read()

def get_text(body, s0, s2, s1 = "(?:.|\s)+"):
	comp = compile__("%s(%s?)%s" % (s0, s1, s2), 16)
	body = comp.search(body)
	if body:
		body = (body.group(1)).strip()
	return body

def sub_desc(body, ls, sub = None):
	if isinstance(ls, dict):
		for x, z in ls.items():
			body = body.replace(x, z)
	else:
		for x in ls:
			if isinstance(x, (list, tuple)):
				if len(x) >= 2:
					body = body.replace(x[0], x[1])
				else:
					body = body.replace(x[0], (sub if sub else ""))
			else:
				body = body.replace(x, (sub if sub else ""))
	return body

strfTime = lambda data = "%d.%m.%Y (%H:%M:%S)", local = True: time.strftime(data, time.localtime() if local else time.gmtime())

def Time2Text(Time):
	ext, ls = [], [("Year", None), ("Day", 365.25), ("Hour", 24), ("Minute", 60), ("Second", 60)]
	while ls:
		lr = ls.pop()
		if lr[1]:
			(Time, Rest) = divmod(Time, lr[1])
		else:
			Rest = Time
		if Rest >= 1.0:
			ext.insert(0, "%d %s%s" % (Rest, lr[0], ("s" if Rest >= 2 else "")))
		if not (ls and Time):
			return str.join(chr(32), ext)

def Size2Text(Size):
	ext, ls = [], list("YZEPTGMK.")
	while ls:
		lr = ls.pop()
		if ls:
			(Size, Rest) = divmod(Size, 1024)
		else:
			Rest = Size
		if Rest >= 1.0:
			ext.insert(0, "%d%sB" % (Rest, (lr if lr != "." else "")))
		if not (ls and Size):
			return str.join(chr(32), ext)

enumerated_list = lambda ls: str.join(chr(10), ["%d) %s" % (numb, line) for numb, line in enumerate(ls, 1)])

isNumber = lambda obj: (not exec_(int, (obj,)) is None)

isSource = lambda jid: isJID.match(jid)

def calculate(Numb = int()):
	if oSlist[0]:
		lines = get_pipe(sys_cmds[1] % (BsPid)).splitlines()
		if len(lines) >= 3:
			list = lines[3].split()
			if len(list) >= 6:
				Numb = (list[4] + list[5])
	else:
		lines = get_pipe(sys_cmds[0] % (BsPid)).splitlines()
		if len(lines) >= 2:
			Numb = lines[1].strip()
	return (int() if not isNumber(Numb) else int(Numb))

def check_copies():
	Cache = Base = {"PID": BsPid, "up": Info["sess"], "alls": []}
	if os.path.isfile(PidFile):
		try:
			Cache = eval(get_file(PidFile))
		except:
			del_file(PidFile)
			Cache = Base
		else:
			try:
				if BsPid == Cache["PID"]:
					Cache["alls"].append(strfTime())
				elif oSlist[0]:
					get_pipe(sys_cmds[4] % (Cache["PID"])); raise SelfExc()
				else:
					os.kill(Cache["PID"], 9); raise SelfExc()
			except:
				Cache = Base
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
				Print("\n%s joined %s;" % (Chats[conf].disp, conf), color3)
			else:
				Print("\nI'll join %s then %s would be connected..." % (conf, Chats[conf].disp), color1)
	else:
		Print("\n\nError: unable to create the conferences-list file!", color2)

# Presence Handler

def XmppPresenceCB(disp, stanza):
	Info["prs"].plus()
	(source, conf, stype, nick) = sAttrs(stanza)
	if not enough_access(conf, nick):
		xmpp_raise()
	if stype == Types[5]:
		disp = disp._owner
		if disp.Roster:
			if enough_access(conf, nick, 7):
				disp.Roster.Authorize(conf)
				disp.Roster.setItem(conf, conf, ["Admins"])
				disp.Roster.Subscribe(conf)
			elif Roster["on"]:
				disp.Roster.Authorize(conf)
				disp.Roster.setItem(conf, conf, ["Users"])
				disp.Roster.Subscribe(conf)
			else:
				Sender(disp, xmpp.Presence(conf, Types[7]))
		xmpp_raise()
	elif Chats.has_key(conf):
		Chat = Chats[conf]
		if stype == Types[7]:
			ecode = stanza.getErrorCode()
			if ecode:
				if ecode == eCodes[9]:
					Chat.nick = "%s." % (nick)
					Chat.join()
				elif ecode in (eCodes[5], eCodes[12]):
					Chat.IamHere = False
					TimerName = ejoinTimerName(conf)
					if TimerName not in iThr.ThrNames():
						try:
							composeTimer(360, ejoinTimer, TimerName, (conf,)).start()
						except iThr.error:
							delivery(AnsBase[20] % (ecode, eCodesDesc[ecode], conf))
						except:
							collectExc(iThr.Thread.start)
				elif ecode == eCodes[4]:
					Chat.full_leave(eCodesDesc[ecode])
					delivery(AnsBase[21] % (ecode, eCodesDesc[ecode], conf))
				elif ecode in (eCodes[2], eCodes[6]):
					Chat.leave(eCodesDesc[ecode])
					delivery(AnsBase[22] % (ecode, eCodesDesc[ecode], conf))
		elif stype in (Types[3], None):
			if Chat.nick == nick:
				Chat.IamHere = True
			Role = GetRole(stanza)
			inst = stanza.getJid()
			if not inst:
				if Chat.isModer:
					Chat.isModer = False
					if not Mserve:
						Chat.change_status(AnsBase[23], sList[2])
						Message(conf, AnsBase[24], disp)
						xmpp_raise()
				elif not Mserve:
					xmpp_raise()
			elif not Chat.isModer:
				if Chat.nick == nick and aDesc.get(Role[0], 0) >= 2:
					Chat.isModer = True
					Chat.leave(AnsBase[25])
					sleep(0.4)
					Chat.join()
				xmpp_raise()
			else:
				inst = (inst.split(chr(47)))[0].lower()
			if Chat.isHereTS(nick) and Chat.isHe(nick, inst):
				Chat.aroles_change(nick, Role, stanza)
			else:
				Chat.sjoined(nick, Role, inst, stanza)
		elif stype == Types[4]:
			scode = stanza.getStatusCode()
			if Chat.nick == nick and scode in (sCodes[0], sCodes[2]):
				Chat.full_leave(sCodesDesc[scode])
				delivery(AnsBase[26] % (scode, conf, sCodesDesc[scode]))
				xmpp_raise()
			elif not Mserve and not stanza.getJid():
				xmpp_raise()
			elif scode == sCodes[1]:
				Nick = stanza.getNick()
				if Chat.isHere(nick):
					Chat.set_nick(nick, Nick)
				else:
					inst = stanza.getJid()
					if inst:
						inst = (inst.split(chr(47)))[0].lower()
					Role = GetRole(stanza)
					if Chat.isHereTS(Nick) and Chat.isHe(Nick, inst):
						Chat.aroles_change(Nick, Role, stanza)
					else:
						Chat.sjoined(Nick, Role, inst)
			else:
				status = (stanza.getReason() or stanza.getStatus())
				if Chat.isHereTS(nick):
					Chat.sleaved(nick)
				call_efunctions("05eh", (conf, nick, status, scode, disp,))
		if Chats.has_key(conf):
			call_efunctions("02eh", (stanza, disp,))

# Iq Handler

def XmppIqCB(disp, stanza):
	Info["iq"].plus()
	ResponseChecker(disp, stanza)
	(source, inst, stype, nick) = sAttrs(stanza)
	if not enough_access(inst, nick):
		xmpp_raise()
	if stype == Types[10]:
		Name = stanza.getQueryNS()
		if not Name:
			Name = (stanza.getTag(Types[16]) or stanza.getTag(Types[17]))
			if Name:
				Name = Name.getNamespace()
		if Name in IqXEPs:
			answer = stanza.buildReply(Types[8])
			if Name == xmpp.NS_DISCO_INFO:
				anode = answer.getTag(Types[18])
				anode.addChild("identity", {"category": "client",
											"type": "bot",
											"name": ProdName[:10]})
				for feature in XEPs:
					anode.addChild("feature", {"var": feature})
			elif Name == xmpp.NS_LAST:
				anode = answer.getTag(Types[18])
				anode.setAttr("seconds", int(time.time() - VarCache["idle"]))
				anode.setData(VarCache["action"])
			elif Name == xmpp.NS_VERSION:
				anode = answer.getTag(Types[18])
				anode.setTagData("name", ProdName)
				anode.setTagData("version", ProdVer)
				Python = "{} [{}.{}.{}]".format(sys.subversion[0], *sys.version_info)
				if oSlist[0]:
					Os = get_pipe(sys_cmds[5]).strip()
				elif oSlist[1]:
					Os = "{0} {2:.16} [{4}]".format(*os.uname())
				else:
					Os = BotOs.capitalize()
				anode.setTagData("os", "%s / %s" % (Os, Python))
			elif Name == xmpp.NS_URN_TIME:
				anode = answer.addChild(Types[17], namespace = xmpp.NS_URN_TIME)
				anode.setTagData("utc", strfTime("%Y-%m-%dT%H:%M:%SZ", False))
				TimeZone = (time.altzone if time.daylight else time.timezone)
				anode.setTagData("tzo", "%s%02d:%02d" % (((TimeZone < 0) and "+" or "-"),
											abs(TimeZone) / 3600,
											abs(TimeZone) / 60 % 60))
			elif Name == xmpp.NS_TIME:
				anode = answer.getTag(Types[18])
				anode.setTagData("utc", strfTime("%Y%m%dT%H:%M:%S", False))
				tz = strfTime("%Z")
				if oSlist[0]:
					tz = tz.decode("cp1251")
				anode.setTagData("tz", tz)
				anode.setTagData("display", time.asctime())
			Sender(disp, answer)
			xmpp_raise()
	call_efunctions("03eh", (stanza, disp,))

# Message Handler

def XmppMessageCB(disp, stanza):
	Info["msg"].plus()
	(source, inst, stype, nick) = sAttrs(stanza)
	if not enough_access(inst, nick):
		xmpp_raise()
	if stanza.getTimestamp():
		xmpp_raise()
	isConf = Chats.has_key(inst)
	if not isConf and not enough_access(inst, nick, 7):
		if not Roster["on"]:
			xmpp_raise()
		CheckFlood(disp)
	if isConf and not Mserve and not Chats[inst].isModer:
		xmpp_raise()
	BotNick = (DefNick if not isConf else Chats[inst].nick)
	if nick == BotNick:
		xmpp_raise()
	Subject = stanza.getSubject()
	body = stanza.getBody()
	if body:
		body = body.strip()
	elif Subject:
		body = Subject.strip()
	if not body:
		xmpp_raise()
	if len(body) > IncLimit:
		body = "%s[...] %d symbols limit." % (body[:IncLimit].strip(), IncLimit)
	if stype == Types[7]:
		code = stanza.getErrorCode()
		if code in (eCodes[10], eCodes[7]):
			if code == eCodes[7]:
				if not isConf:
					xmpp_raise()
				Chats[inst].join()
				sleep(0.6)
			Message(source, body)
		xmpp_raise()
	if Subject:
		call_efunctions("09eh", (inst, nick, Subject, body, disp,))
	else:
		Copy, isToBs = body, (stype == Types[0])
		if stype != Types[1]:
			if (stanza.getTag(Types[14])):
				answer = xmpp.Message(source)
				answer.setTag(Types[15], namespace = xmpp.NS_RECEIPTS)
				answer.setID(stanza.getID())
				Sender(disp, answer)
			stype = Types[0]
		for app in [(BotNick + Key) for Key in (":", ",", ">")]:
			if Copy.startswith(app):
				Copy, isToBs = Copy[len(app):].lstrip(), True
				break
		if not Copy:
			xmpp_raise()
		Copy = Copy.split(None, 1)
		command = (Copy.pop(0)).lower()
		if not isToBs and isConf and Chats[inst].cPref and command not in sCmds:
			if Chats[inst].cPref == command[:1]:
				command = command[1:]
			else:
				command = None
		elif isToBs and not Cmds.has_key(command) and command.startswith(cPrefs):
			command = command[1:]
		if isConf and command in Chats[inst].oCmds:
			xmpp_raise()
		if Cmds.has_key(command):
			VarCache["idle"] = time.time()
			VarCache["action"] = AnsBase[27] % command.upper()
			Cmds[command].execute(stype, (source, inst, nick), (Copy[0] if Copy else ""), disp)
		else:
			call_efunctions("01eh", (stanza, isConf, stype, (source, inst, nick), body, isToBs, disp,))

# Connecting & Dispatching

def connect_client(source, InstanceAttrs):
	(server, cport, host, user, code) = InstanceAttrs
	disp = xmpp.Client(host, cport, None)
	Print("\n\n'%s' connecting..." % (source), color4)
	if ConTls:
		ConType = (None, False)
	else:
		ConType = (False, True)
	try:
		ConType = disp.connect((server, cport), None, *ConType)
	except KeyboardInterrupt:
		raise KeyboardInterrupt("Interrupt (Ctrl+C)")
	except:
		Print("\n'%s' can't connect to '%s' (Port: %s). I'll retry later..." % (source, server.upper(), str(cport)), color2)
		return (False, None)
	if ConType:
		ConType = ConType.upper()
		if ConTls and ConType != "TLS":
			Print("\n'%s' was connected, but a connection isn't secure." % (source), color1)
		else:
			Print("\n'%s' was successfully connected!" % (source), color3)
		Print("\n'%s' using - '%s'" % (source, ConType), color4)
	else:
		Print("\n'%s' can't connect to '%s' (Port: %s). I'll retry later..." % (source, server.upper(), str(cport)), color2)
		return (False, None)
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
			Print("\n'%s' was authenticated, but old auth method is used...", color1)
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
			return (False, None)
	except:
		disp.Roster = None
	disp.RespExp = {}
	disp.RegisterHandler(xmpp.NS_PRESENCE, XmppPresenceCB)
	disp.RegisterHandler(xmpp.NS_IQ, XmppIqCB)
	disp.RegisterHandler(xmpp.NS_MESSAGE, XmppMessageCB)
	Clients[source] = disp
	Sender(disp, caps_add(xmpp.Presence(show = sList[0], status = DefStatus)))
	return (True, source)

def connectAndDispatch(disp):
	if ReverseDisp(disp, False):
		sleep(60)
		for conf in Chats.itervalues():
			if disp == conf.disp:
				conf.join()
		DispatchHandler(disp)
	else:
		delivery(AnsBase[28] % (disp))

def connect_clients():
	for Inctance, Attrs in InstansesDesc.items():
		conn = connect_client(Inctance, Attrs)
		if not conn[0]:
			if conn[1] and conn[1] == eCodes[2]:
				continue
			composeTimer(60, connectAndDispatch, "%s-%s" % (Types[13], Inctance), (Inctance,)).start()

def ReverseDisp(disp, rejoin = True):
	Iters = itypes.Number()
	while 1440 > Iters.plus():
		if connect_client(disp, InstansesDesc[disp])[0]:
			if rejoin:
				for conf in Chats.itervalues():
					if disp == conf.disp:
						conf.join()
			return True
		else:
			sleep(60)

def DispatchHandler(disp):
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
			if not ReverseDisp(disp):
				delivery(AnsBase[28] % (disp))
				break
			ZeroCycles = itypes.Number()
		except xmpp.Conflict:
			delivery(AnsBase[29] % (disp))
			break
		except xmpp.SystemShutdown:
			if not ReverseDisp(disp):
				delivery(AnsBase[28] % (disp))
				break
			ZeroCycles = itypes.Number()
		except xmpp.StreamError:
			pass
		except:
			collectDFail()
			if Info["errors"].plus() >= len(Clients.keys())*8:
				sys_exit("Dispatch Errors!")

# load_mark2 & exit

def load_mark2():
	Print("\n\n%s\n\n" % (FullName), color3)
	check_copies()
	load_expansions()
	call_sfunctions("00si")
	connect_clients()
	while len(Clients.keys()) == 0:
		sleep(0.02)
	Print("\n\nYahoo! I am online!", color3)
	join_chats()
	Print("\n\n%s is ready to serve!\n\n" % (ProdName), color3)
	call_sfunctions("02si")
	for disp in Clients.keys():
		ThrName = "%s-%s" % (Types[13], disp)
		if ThrName not in iThr.ThrNames():
			composeThr(DispatchHandler, ThrName, (disp,)).start()
	while VarCache["alive"]:
		sleep(180)
		Cls = itypes.Number()
		for Name in iThr.ThrNames():
			if Name.startswith(Types[13]):
				Cls.plus()
		if Cls._int() == 0:
			sys_exit("All of the clients now fallen!")
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
		collectExc(load_mark2)
		sys_exit("Critical Fail!")

# The End is Near =>