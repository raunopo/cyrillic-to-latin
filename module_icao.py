import re

ICAO_RULES = {
    'ё': 'e', 
	'ђ': 'd', 
	'є': 'ie', 
	'ѕ': 'dz', 
	'і': 'i', 
	'ї': 'i', 
	'ј': 'j',
    'љ': 'lj', 
	'њ': 'nj', 
	'ќ': 'k', 
	'ў': 'u', 
	'џ': 'dz', 
	'а': 'a', 
	'б': 'b',
    'в': 'v', 
	'г': 'g', 
	'д': 'd', 
	'е': 'e', 
	'ж': 'zh', 
	'з': 'z', 
	'и': 'i',
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
	'ъ': 'ie', 
	'ь': '', # sümbol ь ICAO mappingus tegelikult puudub - asendame tühjaga
	'ы': 'y', 
	'э': 'e', 	
    'ю': 'iu', 
	'я': 'ia', 
	'ѫ': 'u', 
	'ѵ': 'y', 
	'ґ': 'g', 
	'ғ': 'g', 
	'һ': 'c'
}

def icao(text: str, lang: str = "ru") -> str | None:
    try:
        if text is None or not isinstance(text, str) or not isinstance(lang, str):
            return None

        lang = lang.lower()
        text = text.strip()

        if not text:
            return None

        tokens = re.findall(r'\b\w+\b|\W+', text, re.UNICODE)
        transliterated_tokens = []

        for token in tokens:
            if token.isalpha():
                translit_token = []
                for idx, char in enumerate(token.lower()):
                    is_start = idx == 0
                    char_lower = char.lower()

                    if char_lower not in ICAO_RULES:
                        return None  # tundmatu täht

                    translit = ICAO_RULES[char_lower]

                    # Keelepõhised erandid
                    if lang == 'ua':
                        if char_lower == 'є' and is_start:
                            translit = 'ye'
                        elif char_lower == 'ї' and is_start:
                            translit = 'yi'
                        elif char_lower == 'й' and is_start:
                            translit = 'y'
                        elif char_lower == 'ю' and is_start:
                            translit = 'yu'
                        elif char_lower == 'я' and is_start:
                            translit = 'ya'
                        elif char_lower == 'г':
                            translit = 'h'
                        elif char_lower == 'ґ':
                            translit = 'g'

                    elif lang == 'by':
                        if char_lower == 'г':
                            translit = 'h'
                        elif char_lower == 'ё':
                            translit = 'io'

                    translit_token.append(translit)

                transliterated_tokens.append(''.join(translit_token))
            else:
                transliterated_tokens.append(token)

        return ''.join(transliterated_tokens)

    except Exception:
        return None