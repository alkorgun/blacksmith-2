# coding: utf-8

#  BlackSmith mark.2
# exp_name = "dns" # /code.py v.x1
#  Id: 34~1c
#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]

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

	commands = ((command_dns, "dns", 1,),)
