events:

macro - call of the shell of the commands
message - just a message
/me - a message starting with "/me"
subject - a change of the subject
join - an user joined
version - a result of the version check
leave - an user leaved
ban - an user has been banned
kick - an user has been kicked
nick - nick changing
role - role changing
status - status changing

conds:

null - null condition (always true)
is - check for {A is B} is truly
is_not - conversely
starts - {A starts with B}
not_starts - conversely
ends - {A ends with B}
not_ends - conversely
cont - {A contains B}
not_cont - conversely
in - {B contains A}
not_in - conversely
len_more - {length of A > B}
len_less - conversely
re - check for A matches regular expression

* A - one of the variables (read near)
* B - the body of the condition (at the main help-file it's named "clause")

vars:

message:
	body - text of the message,
	jid - JID of user sent message,
	nick - nick of user sent message,
	role - role of user sent message (looks like "admin/moderator"),
	stype - a type of the message ("chat" - private, "groupchat" - msg to muc)
/me: body, jid, nick, role
subject: body, nick
join: caps, caps_ver, jid, nick, role,
	show - a type of the status (chat, away, xa, dnd),
	status - text of the status
version: jid, nick, role,
	name - name of the users's client,
	version - version of the users's client,
	os - OS of the user
leave, ban, kick: jid, nick, role,
	reason - a reason of leaving/ban/kick
nick: jid, role,
	nick - new nick,
	old_nick - old nick
role: jid, nick, role
status: jid, nick, role, show, status

about clause:

the body of the condition must be written like html comment: <!--some text goes here-->
also for more flexible conditions verify that the variables, there is a tool called "flags".
if the flags are not needed, then you must specify "null". You can use one or more flags.
if the flags are more than one, they must be specified with the separation character "&", as follows: flag0&flag1&flag2

flags:
	strip - just removing whitespace from the edges of variable,
	lower - translating variable to the lower case,
	layout - equalization of the similar characters of Cyrillic and Latin alphabets

reaction types:

command: the first parameter must to be the one of the bot's commands (command is executed on behalf of the bot)
set: outcast, none, member, admin, owner, kick, visitor, participant, moder
message: chat (message to muc), private (private message)

about args of alias:

you can insert an alias corresponding variables into parameters. do so at the expense of the syntax - "%(var_name)s".
you can also insert a random value. the syntax:
	$rand(1, 9) - random number from a specified range, where 1 - start, and 9 - the end
	$rand([option one||option two]) - random selection from a list of options (options must be separated by "||")
	$rand_user - inserting nick of random user of the conference (each use of this option will insert a new nick)

all this can be combined, for example: some text $rand([$rand(11, 21) some text||some text %(nick)s||$rand_user some text||some text])

variables to insert into the text of the macro: nick, jid, role, stype,
	aff - affiliation of the user,
	arg0 - the first argument of the args typed by the user when calling a macro (if none, it will be replaced by JID of the chat),
	arg1 - second (if none, it would be replaced by value of variable "stype"),
	arg2 - third (if none, it would be replaced by aff. of the user),
	arg3 - 4th (if none, it would be replaced by role of the user),
	args - arguments entirely

* Also, you can insert a variable "chat" everywhere
* The variable "stype" can not added to the args of the alias for the event "message"