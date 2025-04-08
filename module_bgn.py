import re

RULES = {
    "by": {
        'а': 'a', 
        'б': 'b', 
        'в': 'v', 
        'г': 'h', 
        'д': 'd', 
        'е': 'ye',
        'ё': 'yo', 
        'ж': 'zh', 
        'з': 'z', 
        'і': 'i', 
        'й': 'y', 
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
        'ў': 'w', 
        'ф': 'f', 
        'х': 'kh',
        'ц': 'ts', 
        'ч': 'ch', 
        'ш': 'sh', 
        'ы': 'y', 
        'ь': "'", 
        'э': 'e',
        'ю': 'yu', 
        'я': 'ya', 
        "'": '"'
    },
    "ru": {
        'а': 'a', 
        'б': 'b', 
        'в': 'v', 
        'г': 'g', 
        'д': 'd', 
        'е': 'e',
        'ё': 'ë', 
        'ж': 'zh', 
        'з': 'z', 
        'и': 'i', 
        'й': 'y', 
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
        'ъ': '"', 
        'ы': 'y',
        'ь': "'", 
        'э': 'e', 
        'ю': 'yu', 
        'я': 'ya'
    },
    "ua": {
        'а': 'a', 
        'б': 'b', 
        'в': 'v', 
        'г': 'h', 
        'ґ': 'g', 
        'д': 'd',
        'е': 'e', 
        'є': 'ye', 
        'ж': 'zh', 
        'з': 'z', 
        'и': 'y', 
        'і': 'i', 
        'ї': 'yi',
        'й': 'y', 
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
        'ь': "'", 
        "'": '"'
    }
}

SPECIAL_RULES = {
    "ru": {
        'е': {
            'prev_chars': list("аеёиоуыэюяйъь"),
            'translit': 'ye',
            'else': 'e'
        },
        'ё': {
            'prev_chars': list("аеёиоуыэюяйъь"),
            'translit': 'yë',
            'else': 'ë'
        }
    },
    "ua": {
        'є': {'position': 'start', 'translit': 'ye', 'else': 'ie'},
        'ї': {'position': 'start', 'translit': 'yi', 'else': 'i'},
        'й': {'position': 'start', 'translit': 'y', 'else': 'i'},
        'ю': {'position': 'start', 'translit': 'yu', 'else': 'iu'},
        'я': {'position': 'start', 'translit': 'ya', 'else': 'ia'},
        'зг': {'translit': 'zgh'}
    }
}

def bgn(text: str, lang: str) -> str | None:
    """
    Transliterates text from Cyrillic to Latin using BGN rules for the specified language.
    
    Args:
        text: Input text to transliterate.
        lang: Language code ('by', 'ru', or 'ua').
    
    Returns:
        Transliterated text as a string, or None if the language is unsupported or contains invalid characters.
    """

    # Check for NaN/float values
    if not isinstance(text, str) or not isinstance(lang, str):
        return None
        
    text = text.strip()
    lang = lang.lower()
    result = []

    rules = RULES.get(lang)
    special_rules = SPECIAL_RULES.get(lang, {})

    if not rules:
        return None  # Unsupported language

    tokens = re.findall(r'\b\w+\b|\W+', text, re.UNICODE)

    for token in tokens:
        if token.isalpha():
            i = 0
            while i < len(token):
                char_lower = token[i].lower()
                is_upper = token[i].isupper()
                translit = None

                # Handle multi-char special cases like 'зг'
                if i + 1 < len(token):
                    pair = token[i:i+2].lower()
                    if pair in special_rules:
                        translit = special_rules[pair]['translit']
                        if is_upper:
                            translit = translit[0].upper() + translit[1:] if len(translit) > 1 else translit.upper()
                        result.append(translit)
                        i += 2
                        continue

                # Handle special rules for specific characters
                if char_lower in special_rules:
                    rule = special_rules[char_lower]
                    prev_char = token[i - 1].lower() if i > 0 else ''

                    if 'position' in rule and i == 0:
                        translit = rule['translit']
                    elif 'prev_chars' in rule and prev_char in rule['prev_chars']:
                        translit = rule['translit']
                    elif 'else' in rule:
                        translit = rule['else']

                # Apply default rule if no special case
                if not translit:
                    if char_lower not in rules and char_lower.isalpha():
                        return None  # Unsupported character
                    translit = rules.get(char_lower, char_lower)

                result.append(translit)
                i += 1
        else:
            result.append(token)

    return ''.join(result)