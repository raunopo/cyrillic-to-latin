import re

# Põhivormide (default) transliteratsioon
BASE_RULES = {
    'а': 'a', 
	'б': 'b', 
	'в': 'v', 
	'г': 'ğ', 
	'ґ': 'g', 
	'д': 'd', 
	'е': 'e', 
	'є': 'je',
    'ж': 'ž', 
	'з': 'z', 
	'и': 'y', 
	'і': 'i', 
	'ї': 'ï', 
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
	'х': 'x', 
	'ц': 'c', 
	'ч': 'č', 
	'ш': 'š', 
	'щ': 'ŝ', 
	'ь': 'j', 
	'ю': 'ju',
    'я': 'ja', 
	'ё': 'ö', 
	'э': 'è', 
	'ы': 'ɏ', 
	'ъ': 'ǒ', 
	'ѣ': 'ė', 
	'ў': 'ŭ',
    'ѫ': 'ü', 
	'ѧ': 'ä', 
	'ѯ': 'ƙ', 
	'ѱ': 'ƥ', 
	'ѳ': 'ḟ', 
	'ѵ': 'ỳ', 
	'џ': 'ǆ',
    '’': '’', 
	'ȣ': 'ȣ', 
	'Ѯ': 'ƙ', 
	'Ѱ': 'ƥ', 
	'Ѳ': 'ḟ', 
	# 'g': 'ġ', 'j': 'ǐ', 'і':	'í' # need on standardis aga need ei ole kirillitsa tähed

}

# Erireeglid: kui täht on enne й või kindlat vokaali
SPECIAL_RULES = {
    'б': {'й': 'b’'},
    'в': {'й': 'v’'},
    'г': {'й': 'ğ’'},
    'ґ': {'й': 'g’'},
    'д': {'й': 'd’'},
    'ж': {'й': 'ž’'},
    'з': {'й': 'z’'},
    'к': {'й': 'k’'},
    'л': {'й': 'l’'},
    'м': {'й': 'm’'},
    'н': {'й': 'n’'},
    'п': {'й': 'p’'},
    'р': {'й': 'r’'},
    'с': {'й': 's’'},
    'т': {'й': 't’'},
    'ф': {'й': 'f’'},
    'х': {'й': 'х’'},
    'ц': {'й': 'c’'},
    'ч': {'й': 'č’'},
    'ш': {'й': 'š’'},
    'щ': {'й': 'ŝ’'},
    'џ': {'й': 'ǆ’'},
    'ѯ': {'й': 'ƙ’'},
    'Ѱ': {'й': 'ƥ’'},
    'Ѳ': {'й': 'ḟ’'},
    #'g': {'й': 'ġ’'}, # see on standardis, aga see ei ole kirillitsa täht
    'ь': {'а': 'j’', 'е': 'j’', 'у': 'j’'},
    'й': {'а': 'j’', 'е': 'j’', 'у': 'j’'},
}


ISOLATED_RULES = {
    'ь': 'ĵ'
}

def dstu_a(text: str, lang: str = None) -> str | None:
    """
    Transliterates Cyrillic text to Latin using DSTU 9112:2021 (A) standard.
    
    Args:
        text: Input text to be transliterated
        lang: Language code (currently unused, for future compatibility)
    
    Returns:
        Transliterated text or None if invalid characters found
    """

    if not isinstance(text, str):
        if isinstance(text, (float, int)):
            text = str(text)
        else:
            return None   
    
    text = text.strip().lower()
    tokens = re.findall(r"[^\W\d_]+|\W+", text, re.UNICODE)
    result = []

    for token in tokens:
        if not token.isalpha():
            result.append(token)
            continue

        translit_token = []
        for i, char in enumerate(token):
            next_char = token[i + 1] if i + 1 < len(token) else ''

            if len(token) == 1 and char in ISOLATED_RULES:
                translit_token.append(ISOLATED_RULES[char])
                continue

            if char in SPECIAL_RULES and next_char in SPECIAL_RULES[char]:
                translit_token.append(SPECIAL_RULES[char][next_char])
                continue

            mapped = BASE_RULES.get(char)
            if mapped is not None:
                translit_token.append(mapped)
            else:
                return None  # unknown character found

        result.append(''.join(translit_token))

    return ''.join(result)
