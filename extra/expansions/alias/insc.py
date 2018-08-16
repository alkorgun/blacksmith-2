# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Алиасы отключены.", # 0
		"Алиасы включены.", # 1
		"Алиасы итак включены.", # 2
		"Алиасы итак отключены.", # 3
		"Список алиасов пуст.", # 4
		"%s\nДоступ: %d\nКоманда: %s\nПараметры: %s", # 5
		"%s\nСобытие: %s\nУсловиe(я):\n%s\nДействие: %s", # 6
		"Нет такого алиаса.", # 7
		"Параметры не пригодны для форматирования.", # 8
		"Уже есть глобальное макро с таким именем.", # 9
		"Кривая регулярка!", # 10
		"Значение условия не может быть пустым!", # 11
		"Длина одного условия не должна превышать %d символов!", # 12
		"Переменные и/или значения условий некорректны!", # 13
		"Количество условий, переменных, значений и наборов флагов не совпадает!", # 14
		"Количество условий не может превышать 8.", # 15
		"Использовать регулярные выражения может только суперадмин.", # 16
		"Название «%s» занято командой.", # 17
		"Значение роли неверно!", # 18
		"Тип сообщения некорректен!", # 19
		"Отсутствует условие!", # 20
		"Доступ не должен быть меньше 1 и больше %d.", # 21
		"Длина названия алиаса не может превышать 16 символов.", # 22
		"А хелпа и не было.", # 23
		"Полный список макро:", # 24
		"\->\nОписание:\n\t%s\nДоступ: %d", # 25
		"Хелп не был задан.", # 26
		"В параметрах к макро не может содержаться команд на которые у тебя нет доступа и команды для контроля алиасов.", # 27
		"Макро «%s» разрешено.", # 28
		"Макро «%s» запрещено.", # 29
		"Нет запрещенных макро." # 30
	)])
else:
	AnsBase_temp = (
		"Alias disabled.", # 0
		"Alias enabled.", # 1
		"Alias already enabled.", # 2
		"Alias already disabled.", # 3
		"The liast of alias is empty.", # 4
		"%s\nAccess: %d\nCommand: %s\nArgs: %s", # 5
		"%s\nEvent: %s\nCondition(s):\n%s\nAction: %s", # 6
		"There is no alias such like this.", # 7
		"Args are not suitable for formatting.", # 8
		"Already there is a global macro with the same name.", # 9
		"Bad regex!", # 10
		"Body of the condition can not be empty!", # 11
		"The length of one condition may not exceed %d characters!", # 12
		"Vars and/or clauses are invalid!", # 13
		"Number of conditions, variables, clauses and a set of flags is not the same!", # 14
		"Number of conditions may not exceed 8.", # 15
		"Use regular expressions can only superadmin.", # 16
		"Name '%s' occupied by the command.", # 17
		"The role is incorrect!", # 18
		"The message type is invalid!", # 19
		"No clause!", # 20
		"Access should not be less than 1 and more than %d.", # 21
		"Alias ​​name length can not exceed 16 characters.", # 22
		"There is no help.", # 23
		"The full list of macro:", # 24
		"\->\nDescription:\n\t%s\nAccess: %d", # 25
		"Help has not been set.", # 26
		"In the parameters of the macro can't contain commands to which you do not have access and command to control aliases.", # 27
		"Macro '%s' allowed.", # 28
		"Macro '%s' forbidden.", # 29
		"There are no forbidden macro." # 30
	)