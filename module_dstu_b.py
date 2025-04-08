import re
#Ївгенія

# --- DSTU System B: Base transliteration rules ---
BASE_RULES_B = {
    'а': 'a', 
	'б': 'b', 
	'в': 'v', 
	'г': 'gh', 
	'ґ': 'g', 
	'д': 'd', 
	'е': 'e', 
	'є': 'je',
    'ж': 'zh', 
	'з': 'z', 
	'и': 'y', 
    'і': 'i',
	'ї': 'ji', 
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
	'х': 'kh', 
	'ц': 'c', 
	'ч': 'ch', 
	'ш': 'sh', 
	'щ': 'shch', 
	'ь': 'j',
    'ю': 'ju', 
	'я': 'ja', 
	'ё': 'jow', 
	'э': 'è', 
	'ы': 'yw', 
	'ъ': 'oh', 
	'ѣ': 'ieh',
    'ў': 'uh', 
	'ѫ': 'juw', 
	'ѧ': 'jaw', 
	'ѯ': 'xh', 
	'ѱ': 'ph', 
	'ѳ': 'fh', 
	'ѵ': 'yh', 
	'џ': 'dh',
    '’': "'", 
	'ȣ': 'uw', 
	'í': "i'", 
    'є́': "je'"
    }

# --- Kontekstipõhised erireeglid ---
SPECIAL_RULES_B = {
    'б': {'й': "b'"},
    'в': {'й': "v'"},
    'г': {'й': "gh'"},
    'ґ': {'й': "g'"},
    'д': {'й': "d'"},
    'ж': {'й': "zh'"},
    'з': {'й': "z'"},
    'к': {'й': "k'"},
    'л': {'й': "l'"},
    'м': {'й': "m'"},
    'н': {'й': "n'"},
    'п': {'й': "p'"},
    'р': {'й': "r'"},
    'с': {'й': "s'"},
    'т': {'й': "t'"},
    'ф': {'й': "f'"},
    'х': {'й': "kh'"},
    'ц': {'й': "c'"},
    'ч': {'й': "ch'"},
    'ш': {'й': "sh'"},
    'щ': {'й': "shch'"},
    'џ': {'й': "dh'"},
    'ѯ': {'й': "xh'"},
    'Ѱ': {'й': "ph'"},
    'Ѳ': {'й': "fh'"},
    #'g': {'й': "gw'"}, see ei ole kirillitsa täht
    'ь': {'а': "j'", 'е': "j'", 'і': "j'", 'у': "j'", 'ȣ': "j'"},
    'й': {'а': "j'", 'е': "j'", 'і': "j'", 'у': "j'", 'ȣ': "j'"},
}

# --- Isoleeritud 'ь' erijuht ---
ISOLATED_RULES_B = {
    'ь': 'hj'
}

def dstu_b(text: str, lang: str = None) -> str | None:
    """
    Transliterates Cyrillic text to Latin using DSTU 9112:2021 (B) standard.
    
    Args:
        text: Input text to be transliterated
        lang: Language code (optional, currently unused)
    
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

            # Erireegel: ainult üksiktäht
            if len(token) == 1 and char in ISOLATED_RULES_B:
                translit_token.append(ISOLATED_RULES_B[char])
                continue

            # Erireegel: kahetäheline kombinatsioon
            if char in SPECIAL_RULES_B and next_char in SPECIAL_RULES_B[char]:
                translit_token.append(SPECIAL_RULES_B[char][next_char])
                continue

            # Tavaline reegel
            mapped = BASE_RULES_B.get(char)
            if mapped is not None:
                translit_token.append(mapped)
            else:
                return None  # Tundmatu sümbol – katkestame

        result.append(''.join(translit_token))

    return ''.join(result)

