import re

# --- Reeglipõhine transkriptsiooniskeem ---
TRANSCRIBE_RULES = {
    'а': 'a', 
	'б': 'b', 
	'в': 'v', 
	'г': 'g', 
	'д': 'd', 
	'е': 'je', 
	'ё': 'o',
    'ж': 'ž', 
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
	'х': 'h', 
	'ц': 'ts', 
	'ч': 'tš', 
	'ш': 'š', 
	'щ': 'štš',
    'ъ': '', 
	'ы': 'õ', 
	'ь': '', 
	'э': 'e', 
	'ю': 'ju', 
	'я': 'ja'
}

VOWELS = {'а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я'}
SOFT_SIGN = 'ь'
HARD_SIGN = 'ъ'

def rt_transcrib (text: str) -> str | None:

    if text is None or not isinstance(text, str) or not text.strip():
        return None
    
    text = text.strip().lower()
    tokens = re.findall(r"[^\W\d_]+|\W+", text, re.UNICODE)
    result = []

    for token in tokens:
        if not token.isalpha():
            result.append(token)
            continue

        translit_token = []
        i = 0
        while i < len(token):
            char = token[i]
            prev_char = token[i - 1] if i > 0 else ''
            next_char = token[i + 1] if i + 1 < len(token) else ''

            # --- Lõppev 'ий' reegel ---
            if i == len(token) - 2 and token[-2:] == "ий":
                vowel_count = sum(1 for c in token if c in VOWELS)
                translit_token.append('i' if vowel_count >= 2 else 'ii')
                i += 2
                continue

            if char == 'е':
                translit_token.append('je' if i == 0 or prev_char in VOWELS or prev_char in {SOFT_SIGN, HARD_SIGN} else 'e')
                i += 1
                continue

            if char == 'ё':
                translit_token.append('o' if prev_char in {'ж', 'ч', 'ш', 'щ'} else 'jo')
                i += 1
                continue

            if char in {'и', 'й'} and (i == 0 and next_char in VOWELS):
                translit_token.append('j')
                i += 1
                continue

            if char == 'с':
                if prev_char in VOWELS and (next_char in VOWELS or i == len(token) - 1):
                    translit_token.append('ss')
                else:
                    translit_token.append('s')
                i += 1
                continue

            if char == 'х':
                if prev_char in VOWELS and (next_char in VOWELS or i == len(token) - 1):
                    translit_token.append('hh')
                else:
                    translit_token.append('h')
                i += 1
                continue

            if char == 'ь':
                if next_char in VOWELS - {'е', 'ё', 'ю', 'я'}:
                    translit_token.append('j')
                # muidu jääb tühjaks
                i += 1
                continue

            mapped = TRANSCRIBE_RULES.get(char)
            if mapped is not None:
                translit_token.append(mapped)
            elif char.isalpha():
                return None  # tundmatu täht
            else:
                translit_token.append(char)

            i += 1

        result.append(''.join(translit_token))

    return ''.join(result)