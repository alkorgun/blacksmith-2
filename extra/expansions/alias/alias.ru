добавление нового функционала "на лету"
{command} (global) ([add] [название_алиаса] [событие] [переменная0/переменная1/и т.д.] [условие0/условие1/и т.д.] [<!--текст первого условия--><!--текст второго условия--><!--и т.д.-->] [флаг0&флаг1/флаг0&флаг1/и т.д.] (command|set|message) (имя_команды|affiliation|role|chat|private) (аргументы_алиаса|причина))|([add] [название] [macro] [имя_команды] (аргументы))|([show] [название] [событие|macro] (bold))|([access] [название] [уровень_доступа])|([help] [название] [set|clear] (текст_хелпа))|([del] [название] [событие|macro])|(enable|disable|state|help|bold)
*/{command} help
бот покажет приложение к данному хелпу
*/{command} add akick0 join jid is <!--dude@jab.org--> null set kick And never come back
бот будет автоматичеки кикать юзера с JID'ом "dude@jab.org" из текущей конференции с причиной "And never come back"
*/{command} global add amoder0 join jid/role is/not_ends <!--my-admin@jab.org--><!--moderator--> null/null set moder Glory my Master
бот будет выдавать права модератора во всех конференция на входе юзеру с JID'ом "my-admin@jab.org" с причиной "Glory my Master"
*/{command} add msg0 message body/role cont/not_ends <!--fuck--><!--moderator--> lower/null command сказать %(nick)s: decorous!
бот добавит алиас на событие "message" с именем "00" и будет предупреждать сквернословящих пользователей
*/{command} global add сome_back status show/nick is/is <!--away--><!--Woody--> null/strip&layout message chat Come back Woody!
бот добавит глобальный алиас, реагирующий на смену статуса (на "отошел") юзеров с ником похожим на "Woody"
*/{command} add role0 role null null <!----> null message chat %(nick)s became - %(role)s
бот добавит алиас, "озвучивающий" любую смену роли
*/{command} add punch macro сказать /me strikes %(args)s $rand(1, 9) times with $rand([the sword||cheeseburger||detached $rand_user's leg])
бот добавит локальное макро с именем "punch" для команды "сказать"
*/{command} add msg1 message stype/role/body is/not_starts/re <!--groupchat--><!--none--><!--(?:http[s]?|ftp|svn)://[^\s'\"<>]+--> null/null/null message chat %(nick)s: годная ссылка
бот будет подмечать полезность ссылки, отправленной в чат
*/{command} access punch 2
бот установит доступ 2 для макро "punch"
*/{command} help punch add comic command to alert an user
бот добавит хелп для макро "punch"
*/{command} help punch clear
бот удалит хелп
*/{command} del msg0 message
бот удалит алиас "msg0" из категории "message" (актуально и для макро)
*/{command} show akick0 join
бот покажет содержание алиаса "akick0" из категори "join"
*/{command} show akick0 join bold
бот покажет алиас в "чистом" виде (т.е. в виде пригодном для добавления)
*/{command} state
бот покажет состояние плагина (включен/выключен)
*/{command} enable
бот включит алиасы (доступ 8)
*/{command} disable
бот отключит алиасы
*/{command} bold
бот покажет список алиасов в "чистом" виде
*/{command}
бот покажет развёрнутый список алиасов