# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Библиотека пуста.", # 0
		"Данный %.5s в библиотеке отсутствует.", # 1
		"В библиотеке нет такой серии.", # 2
		"Этой книги в библиотеке нет.", # 3
		"У тебя нет закладок.", # 4
		"Я не могу тайти твои закладки, ибо я не знаю твой JID.", # 5
		"Последняя страница книги - %d.", # 6
		"Книга пуста.", # 7
		"Всего в библиотеке %d книг.", # 8
		"Этого файла не существует.", # 9
		"Уже в библиотеке.", # 10
		"Добавлено с id='%s'.", # 11
		"Такого пункта в библиотечной карте нет.", # 12
		"Неверный номер страницы.", # 13
		"Нет такой страницы.", # 14
		"Неверное название." # 15
					)])
else:
	AnsBase_temp = (
		"The library is empty.", # 0
		"No such %s in base.", # 1
		"No such cycle in base.", # 2
		"No such book in library.", # 3
		"You haven't any bookmarks.", # 4
		"I can't find your bookmark, because I don't know your JID.", # 5
		"The last page is %d.", # 6
		"The book is empty.", # 7
		"There are %d books in library.", # 8
		"File is not exist.", # 9
		"Already in.", # 10
		"Added with id='%s'.", # 11
		"No such data field in base.", # 12
		"Incorrect page number.", # 13
		"No such page.", # 14
		"Incorrect name." # 15
					)