import re
import pandas as pd

RULES = {
    "ru": {
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'g', 
		'д': 'd', 
		'е': 'e', 
		'ё': 'yo',
        'ж': 'zh', 
		'з': 'z', 
		'и': 'i', 
		'й': 'j', 
		'і': 'i', 
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
		'ч': 'ch', 
		'ш': 'sh', 
		'щ': 'shh', 
		'ъ': "''",
        'ы': 'y′', 
		'ь': "'", 
		'э': 'e′', 
		'ю': 'yu', 
		'я': 'ya', 
		'’': '’',
        'ѣ': 'ue', 
		'ѳ': 'fh', 
		'ѵ': 'yh'
    },
    "ua": {
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'g', 
		'ґ': 'g̀', 
		'д': 'd', 
		'е': 'e', 
		'є': 'ye',
        'ж': 'zh', 
		'з': 'z', 
		'и': 'y′', 
		'й': 'j', 
		'і': 'i', 
		'ї': 'yi', 
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
		'ч': 'ch', 
		'ш': 'sh', 
		'щ': 'shh',
        'ь': "'", 
		'ю': 'yu', 
		'я': 'ya', 
		'’': '’'
    },
    "by": {
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'g', 
		'д': 'd', 
		'е': 'e', 
		'ё': 'yo',
        'ж': 'zh', 
		'з': 'z', 
		'й': 'j', 
		'і': 'i', 
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
        'ў': 'u′', 
		'ф': 'f', 
		'х': 'x', 
		'ч': 'ch', 
		'ш': 'sh', 
		'ы': 'y′', 
		'ь': "'",
        'э': 'e′', 
		'ю': 'yu', 
		'я': 'ya', 
		'’': '’'
    }
}

c_followed_by_c = {'и','е','ё','ю','я','й','і'}


def gost_b(text: str, lang: str) -> str | None:

    # Teisendame float (NaN) stringiks
    if isinstance(text, float):
        text = str(text) if not pd.isna(text) else ''
    if isinstance(lang, float):
        lang = str(lang) if not pd.isna(lang) else ''
    
    # Tühja sisendi kontroll
    if not isinstance(text, str) or not isinstance(lang, str):
        return None
            
    if not isinstance(lang, str):
        return None
        
    text = text.strip().lower()
    lang = lang.lower()

    if lang not in RULES:
        return None

    text = text.strip().lower()
    lang = lang.lower()
    
    rules = RULES.get(lang)
    if not rules:
        return None  # tundmatu keel

    result = []
    for idx, char in enumerate(text):
        if char == 'ц':
            next_char = text[idx + 1] if idx + 1 < len(text) else ''
            translit = 'c' if next_char in c_followed_by_c else 'cz'
        elif char == 'і' and lang == 'ru':
            translit = 'i′'
        else:
            translit = rules.get(char)
            if translit is None:
                if char.isalpha():
                    return None  # tundmatu täht
                translit = char  # nt punkt, tühik jne

        result.append(translit)

    return ''.join([x for x in result if x is not None])