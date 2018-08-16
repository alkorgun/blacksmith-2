# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Логгер выключен.", # 0
		"Логгер включен.", # 1
		"Логгер полностью отключен, эта команда не доступна.", # 2
		"Ничего не записано.", # 3
		"Пароль для веб-страницы с логами: '%s'.", # 4
		"Пароль не был задан.", # 5
		"Просмотр логов в сети отныне разрешен без пароля." # 6
	)])
else:
	AnsBase_temp = (
		"The logger is off.", # 0
		"The logger is on.", # 1
		"The logger is totally disabled, this command is unavailable.", # 2
		"Nothing was logged.", # 3
		"Password for the Web interface: '%s'.", # 4
		"Password has not been set.", # 5
		"Viewing of logs from the Web allowed without a password." # 6
	)