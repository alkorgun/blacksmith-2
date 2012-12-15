управление ростером бота
{command} (jid бота/номер jid'а) ([+/-] [jid] (nick) (админ))
*/{command}
бот покажет пронумерованый список своих jid'ов
*/{command} some@jid.com + qwerty@xmpp.ru Qwerty админ
добавит "qwerty@xmpp.ru" в группу "Admins" с ником "Qwerty"
*/{command} 1 + qwerty@xmpp.ru
добавит "qwerty@xmpp.ru" в группу "Users"
*/{command} 1 - qwerty@xmpp.ru
удалит "qwerty@xmpp.ru" из ростера