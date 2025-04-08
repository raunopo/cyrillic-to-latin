import re

BASE_RULES = {
    "by": {
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'h', 
		'д': 'd', 
		'е': 'ie', 
		'ё': 'io', 
		'ж': 'ž',
        'з': 'z',
        'і': 'i',
		'й': 'j', 
		'к': 'k', 
		'л': 'l', 
		'м': 'm', 
		'н': 'n', 
		'о': 'o',
        'п': 'p', 
		'р': 'r', 
		'с': 's', 
		'т': 't', 
		'у': 'u', 
		'ў': 'ŭ', 
		'ф': 'f', 
		'х': 'ch',
        'ц': 'c', 
		'ч': 'č', 
		'ш': 'š', 
		'ы': 'y', 
		'ь': '', 
		'э': 'e', 
		'ю': 'iu', 
		'я': 'ia',
        '’': ''
    },
    "ru": {
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'g', 
		'д': 'd', 
		'е': 'e', 
		'ё': 'ë', 
		'ж': 'ž',
        'з': 'z', 
		'и': 'i', 
		'й': 'j', 
		'к': 'k', 
		'л': 'l', 
		'м': 'm', 
		'н': 'n', 
		'о': 'o',
        'п': 'p', 
		'р': 'r', 
		'с': 's', 
		'т': 't', 
		'у': 'u', 
		'ф': 'f', 
		'х': 'h', 
		'ц': 'c',
        'ч': 'č', 
		'ш': 'š', 
		'щ': 'šč', 
		'ъ': '”', 
		'ы': 'y', 
		'ь': '’', 
		'э': 'è', 
		'ю': 'ju',
        'я': 'ja', 
		'’': ''
    },
    "ua": { #Ївгенія
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'h', 
		'ґ': 'g', 
		'д': 'd', 
		'е': 'e', 
		'є': 'ie',
        'ж': 'zh', 
		'з': 'z', 
		'и': 'y',
        'і': 'i',
		'ї': 'i', 
		'й': 'i', 
		'к': 'k', 
		'л': 'l',
        'м': 'm', 
		'н': 'n', 
		'о': 'o', 
		'п': 'p', 
		'р': 'r', 
		'с': 's', 
		'т': 't', 
		'у': 'u',
        'ф': 'f', 
		'х': 'kh', 
		'ц': 'ts', 
		'ч': 'ch', 
		'ш': 'sh', 
		'щ': 'shch', 
		'ь': '',
        'ю': 'iu', 
		'я': 'ia', 
		'’': ''
    }
}

SPECIAL_RULES = {
    "by": {
        'е': {
            'trigger': ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я', 'і', 'ў', 'ь', '’'],
            'start': 'je',
            'after': 'je',
            'else': 'ie'
        },
        'ё': {
            'trigger': ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я', 'і', 'ў', 'ь', '’'],
            'start': 'jo',
            'after': 'jo',
            'else': 'io'
        },
        'ю': {
            'trigger': ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я', 'і', 'ў', 'ь', '’'],
            'start': 'ju',
            'after': 'ju',
            'else': 'iu'
        },
        'я': {
            'trigger': ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я', 'і', 'ў', 'ь', '’'],
            'start': 'ja',
            'after': 'ja',
            'else': 'ia'
        }

    },
    "ua": {
        'є': {'start': 'ye', 'else': 'ie'},
        'ї': {'start': 'yi', 'else': 'i'},
        'й': {'start': 'y', 'else': 'i'},
        'ю': {'start': 'yu', 'else': 'iu'},
        'я': {'start': 'ya', 'else': 'ia'},
        'зг': {'seq': 'zgh'},
        'ій': {'seq': 'ii'},
        'ий': {'seq': 'yi'}
    }
}

def eki(text: str, lang: str) -> str | None:
    """
    Transliterates Cyrillic text to Latin using EKI (Estonian Language Institute) rules.
    
    Args:
        text: Input text to be transliterated
        lang: Language code ('by' for Belarusian, 'ru' for Russian, 'ua' for Ukrainian)
    
    Returns:
        Transliterated text or None for invalid input/unsupported language
    
    Examples:
        >>> eki("Дзень добры", "by")
        "dzen dobry"
        >>> eki("Привет", "ru")
        "privet"
    """    
    if not isinstance(text, str):
        if isinstance(text, (float, int)):
            text = str(text)
        else:
            return None
            
    if not isinstance(lang, str):
        return None

    text = text.strip().lower()
    lang = lang.lower()

    if lang == "ua":
        text = text.replace('’', '')

    rules = BASE_RULES.get(lang)
    specials = SPECIAL_RULES.get(lang, {})
    if not rules:
        return None

    result = []
    i = 0

    while i < len(text):
        char = text[i]
        prev_char = text[i - 1] if i > 0 else ''
        next_char = text[i + 1] if i + 1 < len(text) else ''
        translit = None

        # Ukraina erijuhud: mitmetähelised järjestused
        if lang == "ua":
            for seq in ['зг', 'ій', 'ий']:
                if text[i:i + len(seq)] == seq:
                    translit = specials.get(seq, {}).get('seq')
                    if translit is None:
                        return None  # tundmatu mitmetäheline reegel
                    result.append(translit)
                    i += len(seq)
                    break
            if translit:
                continue

        # Valgevene erijuhud: algus, vokaal, pehmendus
        if char in specials:
            rule = specials[char]
            is_start = i == 0 or not text[i - 1].isalpha()
            if is_start and 'start' in rule:
                translit = rule['start']
            elif 'trigger' in rule and prev_char in rule['trigger'] and 'after' in rule:
                translit = rule['after']
            elif 'else' in rule:
                translit = rule['else']

        # 'ь' käsitlus
        if char == 'ь':
            if lang == 'by' and result:
                result[-1] += '́'  # lisame akuut
                i += 1
                continue
            elif lang == 'ua':
                i += 1  # ignoreeri
                continue

        # Tavaline reegel
        if translit is None:
            translit = rules.get(char)
            if translit is None and char.isalpha():
                return None  # tundmatu täht
            translit = translit if translit is not None else char

        result.append(translit)
        i += 1

    return ''.join([x for x in result if x is not None])