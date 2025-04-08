import re
from typing import Optional

BASE_RULES = {
    'by': {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'h',
        'д': 'd',
        'е': 'e',
        'ё': 'o',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
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
        'ф': 'f',
        'х': 'kh',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'shch',
        'ы': 'y',
        'ъ': '', #kuigi nõutud "j" peale täishäälikut, siis näite alusel seda tegelikult ei translitereerita: Адъютантов [hääldus: адjутантов] – ladina k. Adjutantov
        'э': 'e',
        'ю': 'ju',
        'я': 'ja',
        'ў': 'w',
        'ь': '',
        '’': '', #kuigi nõutud "j" peale täishäälikut, siis näite alusel seda tegelikutl ei translitereerita, (nt: Дар’я [hääldus: darja] → ladina k. Darja) 
        "'": ''  # Lisame eraldi apostroofi reegli - see on selleks, et ' käsitletakse eraldajana ja pärast pannakse tokenite liitmisel tagasi
    },
    'ru': {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'zh',
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
        'х': 'kh',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'shch',
        'ы': 'y',
        'ъ': '', #kuigi nõutud "j" peale täishäälikut, siis näite alusel seda tegelikult ei translitereerita: Адъютантов [hääldus: адjутантов] – ladina k. Adjutantov
        'э': 'e', 'ю': 'iu',  'я': 'ia',  'ь': '', '’': '', #kuigi nõutud "j" peale täishäälikut, siis näite alusel seda tegelikutl ei translitereerita, (nt: Дар’я [hääldus: darja] → ladina k. Darja)
        "'": ''  # Lisame eraldi apostroofi reegli - see on selleks, et ' käsitletakse eraldajana ja pärast pannakse tokenite liitmisel tagasi
    }    
}

SPECIAL_RULES = {
    'by': {
        'е': {
            'start': 'je',
            'after_vowel_or_soft': 'je',
            'after_consonant': 'ie' # reegel on vastuoluline kuna hiljem on standardis toosdud näide: лябецкая	liabetskaja aga peale konsonanti peaks E olema IE: liabetskaja  
        },
        'ё': {
            'start': 'jo',
            'after_vowel_or_soft': 'jo',
            'after_consonant': 'io'
        },
        'ю': {
            'start': 'ju',
            'after_vowel_or_soft': 'ju',
            'after_consonant': 'iu'
        },
        'я': {
            'start': 'ja',
            'after_vowel_or_soft': 'ja',
            'after_consonant': 'ia'
        }
    }
}

def blr(text: str, lang: str = 'by') -> str | None:
    
    
    # Check for NaN/float values
    if not isinstance(text, str) or not text.strip():
        return None
    
    if not isinstance(lang, str):
        return None
    
    text = text.strip().lower()
    lang = lang.lower()

    rules = BASE_RULES.get(lang)
    specials = SPECIAL_RULES.get(lang, {})
    vowels = {'а', 'е', 'ё', 'и', 'і', 'о', 'у', 'ы', 'э', 'ю', 'я'}
    softs = {'ь', 'ъ', '’', "'", 'ў'}  # Pehmendusmärgid
    consonants = set('бвгджзйклмнпрстфхцчшщ')

    if not rules:
        return None

    tokens = re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)*|\W+", text, re.UNICODE)
    result = []

    for token in tokens:
        if not any(c.isalpha() for c in token):
            result.append(token)
            continue

        translit_token = []
        for i, char in enumerate(token):
            if char in {"'", "’"}:
                continue  # ignoreeri pehmendusmärke

            prev_char = token[i - 1] if i > 0 else ''
            next_char = token[i + 1] if i + 1 < len(token) else ''
            prev_was_soft = prev_char in softs

            rule = specials.get(char)
            translit = None

            if rule:
                if i == 0:
                    translit = rule.get('start')
                elif prev_char in vowels or prev_was_soft:
                    translit = rule.get('after_vowel_or_soft')
                elif prev_char in consonants:
                    translit = rule.get('after_consonant')

            if translit is None:
                if char not in rules and char.isalpha():
                    return None  # tundmatu täht
                translit = rules.get(char, char)

            translit_token.append(translit)

        result.append(''.join([x for x in translit_token if x is not None]))

    return ''.join([x for x in result if x is not None])