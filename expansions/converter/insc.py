# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Неверно указана единица измерения.", # 0
		"Oops...", # 1
		"Неверно указана категория." # 2
					)])
else:
	AnsBase_temp = (
		"Incorrect unit.", # 0
		"Oops...", # 1
		"Incorrect category." # 2
					)