# coding: utf-8

UserAgents = {
	"RU": "ru-RU",
	"UA": "ua-UA",
	"EN": "en-US"
				}

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Не могу получить доступ к ресурсу.", # 0
		"Проблемы с разметкой...", # 1
		"Твоих запросов нет в базе.", # 2
		"Не вижу твоего JID'а, поэтому не могу найти твоих запросов в базе.", # 3
		"\n\n** Ещё %d результатов (командуй «гугл *»).", # 4
		"Ничего не найдено...", # 5
		"Этот язык не поддерживается.", # 6
		"\n\n** Ещё %d вариантов перевода (командуй «перевод *»).", # 7
		"Поддерживаемые языки:\n", # 8
		"Завершено - {0}%", # 9
		"Начинается загрузка. Это может занять несколько минут...", # 10
		"Сейчас я занят другой загрузкой. Попробуй позже.", # 11
		"\n* Погода предоставлена Gismeteo.ru", # -2
		"Запрос блокирован Кинопоиском." # -1
					)])

	LangMap = {
		"af": "Африкаанс",		"ar": "Арабский",		"be": "Белорусский",
		"bg": "Болгарский",		"ca": "Каталанский",	"cs": "Чешский",
		"cy": "Валлийский",		"da": "Датский",		"de": "Немецкий",
		"el": "Греческий",		"en": "Английский",		"es": "Испанский",
		"et": "Эстонский",		"fa": "Персидский",		"fi": "Финский",
		"fr": "Французский",	"ga": "Ирландский",		"gl": "Галисийский",
		"hi": "Хинди",			"hr": "Хорватский",		"hu": "Венгерский",
		"id": "Индонезийский",	"is": "Исландский",		"it": "Итальянский",
		"iw": "Иврит",			"ja": "Японский",		"ko": "Корейский",
		"la": "Латынь",			"lt": "Литовский",		"lv": "Латышский",
		"mk": "Македонский",	"mt": "Мальтийский",	"nl": "Голландский",
		"no": "Норвежский",		"pl": "Польский",		"pt": "Португальский",
		"ro": "Румынский",		"ru": "Русский",		"sk": "Словацкий",
		"sl": "Словенский",		"sq": "Албанский",		"sr": "Сербский",
		"sv": "Шведский",		"sw": "Суахили",		"th": "Тайский",
		"tl": "Тагальский",		"tr": "Турецкий",		"uk": "Украинский",
		"vi": "Вьетнамский",	"yi": "Идиш",			"zh-CN": "Китайский"
					}

	Currency_desc = {
		"AMD": "Армянский драм",
		"AUD": "Австралийский доллар ($)",
		"AZN": "Азербайджанский манат",
		"BGN": "Болгарский лев",
		"BRL": "Бразильский реал",
		"BYR": "Белорусский рубль",
		"CAD": "Канадский доллар",
		"CHF": "Швейцарский франк (₣)",
		"CNY": "Китайский юань",
		"CZK": "Чешская крона",
		"DKK": "Датская крона",
		"EUR": "Евро (€)",
		"GBP": "Фунт стерлингов Соединенного королевства (£)",
		"HUF": "Венгерский форинт",
		"INR": "Индийская рупия",
		"JPY": "Японская йена (¥)",
		"KGS": "Киргизский сом",
		"KRW": "Вон Республики Корея",
		"KZT": "Казахский тенге",
		"LTL": "Литовский лит",
		"LVL": "Латвийский лат",
		"MDL": "Молдавская лея",
		"NOK": "Норвежская крона",
		"PLN": "Польская злотая",
		"RON": "Новая Румынская лея",
		"RUB": "Российский рубль",
		"SEK": "Шведская крона",
		"SGD": "Сингапурский доллар",
		"TJS": "Таджикская сомони",
		"TMT": "Новый туркменский манат",
		"TRY": "Турецкая лира (£)",
		"UAH": "Украинская гривна",
		"USD": "Доллар США ($)",
		"UZS": "Узбекский сум",
		"XDR": "Специальные права заимствования (¤)",
		"ZAR": "Южноафриканский рэнд"
					}
else:
	AnsBase_temp = (
		"No access to the resource.", # 0
		"Trouble with the marking...", # 1
		"There are no your requests in the cache.", # 2
		"I can't find your requests in the cache, because I don't know your JID.", # 3
		'\n\n** There are %d another results (type "google *").', # 4
		"No result...", # 5
		"This language is not supported.", # 6
		'\n\n** There are %d another translations (type "tr *").', # 7
		"Supported languages:\n", # 8
		"loaded - {0}%", # 9
		"Download can take several minutes...", # 10
		"Now I'm busy with another load. Try again later." # 11
					)

	LangMap = {
		"af": "Afrikaans",		"ar": "Arabic",			"be": "Byelorussian",
		"bg": "Bulgarian",		"ca": "Catalan",		"cs": "Czech",
		"cy": "Welsh",			"da": "Danish",			"de": "German",
		"el": "Greek",			"en": "English",		"es": "Spanish",
		"et": "Estonian",		"fa": "Persian",		"fi": "Finnish",
		"fr": "French",			"ga": "Irish",			"gl": "Galician",
		"hi": "Hindi",			"hr": "Croatian",		"hu": "Hungarian",
		"id": "Indonesian",		"is": "Icelandic",		"it": "Italian",
		"iw": "Hebrew",			"ja": "Japanese",		"ko": "Korean",
		"la": "Latin",			"lt": "Lithuanian",		"lv": "Latvian",
		"mk": "Macedonian",		"mt": "Maltese",		"nl": "Dutch",
		"no": "Norwegian",		"pl": "Polish",			"pt": "Portuguese",
		"ro": "Romanian",		"ru": "Russian",		"sk": "Slovak",
		"sl": "Slovenian",		"sq": "Albanian",		"sr": "Serbian",
		"sv": "Swedish",		"sw": "Swahili",		"th": "Thai",
		"tl": "Tagalog",		"tr": "Turkish",		"uk": "Ukrainian",
		"vi": "Vietnamese",		"yi": "Yiddish",		"zh-CN": "Chinese"
				}