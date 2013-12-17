# coding: utf-8

#  BlackSmith mark.2
# exp_name = "dns" # /code.py v.x2
#  Id: 34~2c
#  Code © (2012-2013) by WitcherGeralt [alkorgun@gmail.com]

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	import socket

	def command_dns(self, stype, source, adress, disp):
		if adress:
			try:
				name, alias, addrs = self.socket.gethostbyaddr(adress.encode("idna"))
			except self.socket.error:
				answer = AnsBase[7]
			else:
				addrs.insert(0, name)
				answer = ", ".join(addrs)
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	def command_port(self, stype, source, adress, disp):
		if adress:
			adress = adress.split()
			if len(adress) == 2:
				host, port = adress
				if port.isdigit():
					server = (host.encode("idna"), int(port))
					if ":" in host:
						flag = self.socket.AF_INET6
						server = server.__add__((0, 0))
						host = host.join(("[", "]"))
					else:
						flag = self.socket.AF_INET
					sock = self.socket.socket(flag, self.socket.SOCK_STREAM)
					sock.settimeout(6)
					try:
						sock.connect(server)
					except Exception:
						answer = "{0}:{1} is closed.".format(host, port)
					else:
						answer = "{0}:{1} is opened.".format(host, port)
					finally:
						sock.close()
				else:
					answer = AnsBase[30]
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		Answer(answer, stype, source, disp)

	commands = (
		(command_dns, "dns", 1,),
		(command_port, "port", 1,)
	)
