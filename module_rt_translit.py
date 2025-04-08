import re
import pandas as pd

'''
UA erireeglit с tähe kohta ei ole rakendatud:

Reeglid:
    s		 Сосюра = Sosjura, Леся = Lesja, Васьо = Vasjo, Мейтус = Meitus
    ss	vokaalide vahel (kuid mitte я, ю, є ega ьо ees, sest nende algul hääldub konsonant j) ja sõna lõpul rõhulise silbi vokaali järel	Лисенко = Lõssenko, Панас = Panass, Олесь = Oless

Tulemus:
    Трипільський	ua	trõpilskõi	FALSE	trõpilsskõi
    Рильський	ua	rõlskõi	FALSE	rõlsskõi
    Сосюра	ua	sosjura	FALSE	sossjura
    Леся	ua	lesja	FALSE	lessja
    Васьо	ua	vasjo	FALSE	vassjo
    
    Панас	ua	panass	FALSE	panas
    
BY erireeglit ei ole rakendatud:

с > ss vokaalide vahel ja sõna lõpul rõhulise silbi vokaali järel

Tulemus:
    Барыс	by	barõss	FALSE	barõs




'''


BASE_RULES = {
    "ld": {
        'à': 'a',
        'á': 'a',
        'â': 'a',
        'ã': 'a',
        'ā': 'a',
        'ă': 'a',
        'å': 'a',
        'ą': 'a',
        'æ': 'ä',
        'ć': 'c',
        'č': 'c',
        'ç': 'c',
        'ď': 'd',
        'đ': 'dj',
        'ð': 'dh',
        'è': 'e',
        'é': 'e',
        'ê': 'e',
        'ē': 'e',
        'ė': 'e',
        'ë': 'e',
        'ě': 'e',
        'ę': 'e',
        'ğ': 'g',
        'ģ': 'g',
        'ì': 'i',
        'í': 'i',
        'î': 'i',
        'ī': 'i',
        'ı': 'i',
        'ï': 'i',
        'į': 'i',
        'ķ': 'k',
        'ĺ': 'l',
        'ľ': 'l',
        'ļ': 'l',
        'ł': 'l',
        'ń': 'n',
        'ñ': 'n',
        'ň': 'n',
        'ņ': 'n',
        'ò': 'o',
        'ó': 'o',
        'ô': 'o',
        'ō': 'o',
        'ő': 'ö',
        'ø': 'ö',
        'œ': 'oe',
        'ŕ': 'r',
        'ř': 'r',
        'ŗ': 'r',
        'ś': 's',
        'ş': 's',
        'ß': 'ss',
        'ť': 't',
        'ţ': 't',
        'þ': 'th',
        'ù': 'u',
        'ú': 'u',
        'û': 'u',
        'ū': 'u',
        'ů': 'u',
        'ű': 'ü',
        'ų': 'u',
        'ý': 'y',
        'ÿ': 'y',
        'ź': 'z',
        'ż': 'z'
    },
    "by": {
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'g', 
		'д': 'd', 
		'дж': 'dž', 
		'дз': 'dz',
        'е': 'je', 
		'ё': 'jo', 
		'ж': 'ž', 
		'з': 'z', 
		'й': 'i', 
		'к': 'k',
        'л': 'l', 
		'м': 'm', 
		'н': 'n', 
		'о': 'o', 
		'п': 'p', 
		'р': 'r', 
		'с': 'ss',
        'т': 't', 
		'у': 'u', 
		'ў': 'v', 
		'ф': 'f', 
		'х': 'hh', 
		'ц': 'ts', 
		'цц': 'tts',
        'ч': 'tš', 
		'чч': 'ttš', 
		'ш': 'š', 
		'ы': 'õ', 
		'э': 'e', 
		'ю': 'ju',
        'я': 'ja', 
		'ь': '', 
		'’': ''
    },
    "ua": {
        'а': 'a', 
		'б': 'b', 
		'в': 'v', 
		'г': 'g', 
		'ґ': 'g', 
		'д': 'd', 
		'е': 'e', 
		'є': 'je',
        'ж': 'ž', 
		'з': 'z', 
		'и': 'õ', 
        'і': 'i',
		'ї': 'ji', 
		'й': 'j', 
		'ій': 'i', 
		'ий': 'õi',
        'к': 'k', 
		'л': 'l', 
		'м': 'm', 
		'н': 'n', 
		'о': 'o', 
		'п': 'p', 
		'р': 'r', 
		'с': 'ss',
        'т': 't', 
		'у': 'u', 
		'ф': 'f', 
		'х': 'hh', 
		'ц': 'ts', 
		'ч': 'tš', 
		'чч': 'ttš', 
		'ш': 'š',
        'щ': 'štš', 
		'ю': 'ju', 
		'я': 'ja', 
		'ь': '', 
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
		'я': 'ja'
    }
}

SPECIAL_RULES = {
    "by": {
        'е': {
            'start': 'je',
            'after': 'je',
            'else': 'e',
            'trigger': ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я', 'і', 'ў', 'ь', '’']
        },
        'і': {
            'start_next_vowel': 'j',
            'after': 'ji',
            'else': 'i',
            'trigger': ['ь', '’'],
            'vowels': ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я', 'і']
        },
        '’і': {
            'seq': 'ji'
        },
        'ьі': {
            'seq': 'ji'
        },
        'чч': {
            'seq': 'ttš'
        },
        'цц': {
            'seq': 'tts'
        },
        'с': {
            'between_vowels': 'ss',
            'else': 's'
        },
        'х': {
            'between_vowels': 'hh',
            'after_vowel_end': 'hh',
            'else': 'h'
        },
        'ь': {
            'else': ''  # alati jääb märkimata
        },
        '’': {
            'else': ''  # sama
        }
    },
    "ua": {
        'чч': {
            'seq': 'ttš'
        },
        'х': {
            'between_vowels': 'hh',
            'after_vowel_end': 'hh',
            'else': 'h'
        },
        'й': {
            'before_vowel': 'j',
            'else': 'i'
        },

        'ий': {
            'seq': 'õi'
        },
        'ій': {
            'end_if_multivowel': 'i',
            'else': 'ii'
        },
        'ь': {
            'before_vowel': 'j',
            'else': ''
        },
        '’': {
            'else': ''
        },
        'с': {
            'between_vowels': 'ss',
            'word_final_after_vowel': 'ss',
            'not_before': ['я', 'ю', 'є', 'ьо'],
            'else': 's'
        }
    }
}

def transliterate_word(text: str, lang: str) -> tuple[str, str, list[str]] | None:
    """Translitereerib ühe sõna. Tagastab (original, transliterated, warnings) või None, kui leidub tundmatuid tähti."""
    if not isinstance(text, str) or not isinstance(lang, str) or pd.isna(text) or pd.isna(lang):
        return None

    text = text.strip().lower()
    lang = lang.lower()
    if not text or lang not in BASE_RULES:
        return None

    result = []
    vowels = {'а', 'е', 'ё', 'и', 'і', 'о', 'у', 'ы', 'э', 'ю', 'я', 'ь'}
    rules = BASE_RULES[lang]
    specials = SPECIAL_RULES.get(lang, {})
    unknown_chars = set()

    i = 0
    while i < len(text):
        matched = False

        # Proovi 3- ja 2-tähelisi erireegleid
        for seq_len in [3, 2]:
            if i + seq_len > len(text):
                continue
            seq = text[i:i+seq_len]
            if seq in specials:
                rule = specials[seq]
                prev_char = text[i-1] if i > 0 else ''
                next_char = text[i+seq_len] if i + seq_len < len(text) else ''
                is_start = i == 0
                is_end = i + seq_len == len(text)

                if 'start' in rule and is_start:
                    result.append(rule['start'])
                    i += seq_len
                    matched = True
                    break
                elif 'after' in rule and 'trigger' in rule and prev_char in rule['trigger']:
                    result.append(rule['after'])
                    i += seq_len
                    matched = True
                    break
                elif 'after_vowel_end' in rule and is_end and prev_char in vowels:
                    result.append(rule['after_vowel_end'])
                    i += seq_len
                    matched = True
                    break
                elif 'after_soft' in rule and prev_char in {'ь', '’'}:
                    result.append(rule['after_soft'])
                    i += seq_len
                    matched = True
                    break
                elif 'between_vowels' in rule and prev_char in vowels and next_char in vowels:
                    if 'not_before' in rule:
                        skip = False
                        for forbidden in rule['not_before']:
                            if text[i+1:].startswith(forbidden):
                                skip = True
                                break
                        if not skip:
                            result.append(rule['between_vowels'])
                            i += seq_len
                            matched = True
                            break
                    else:
                        result.append(rule['between_vowels'])
                        i += seq_len
                        matched = True
                        break            
                elif 'before_vowel' in rule and next_char in vowels:
                    result.append(rule['before_vowel'])
                    i += seq_len
                    matched = True
                    break
                elif 'end_if_multivowel' in rule and is_end and sum(1 for c in text if c in vowels) > 1:
                    result.append(rule['end_if_multivowel'])
                    i += seq_len
                    matched = True
                    break
                elif 'seq' in rule:
                    result.append(rule['seq'])
                    i += seq_len
                    matched = True
                    break
                elif 'else' in rule:
                    result.append(rule['else'])
                    i += seq_len
                    matched = True
                    break
        if matched:
            continue

        # Ühe tähe erireegel
        char = text[i]
        if char in specials:
            rule = specials[char]
            prev_char = text[i-1] if i > 0 else ''
            next_char = text[i+1] if i + 1 < len(text) else ''
            is_start = i == 0
            is_end = i == len(text)-1

            if 'start' in rule and is_start:
                result.append(rule['start'])
            elif 'start_next_vowel' in rule and is_start and next_char in rule.get('vowels', []):
                result.append(rule['start_next_vowel'])
            elif 'after' in rule and 'trigger' in rule and prev_char in rule['trigger']:
                result.append(rule['after'])
            elif 'after_vowel_end' in rule and is_end and prev_char in vowels:
                result.append(rule['after_vowel_end'])
            elif 'after_soft' in rule and prev_char in {'ь', '’'}:
                result.append(rule['after_soft'])
            elif 'between_vowels' in rule and prev_char in vowels and next_char in vowels:
                result.append(rule['between_vowels'])
            elif 'before_vowel' in rule and next_char in vowels:
                result.append(rule['before_vowel'])
            elif 'end_if_multivowel' in rule and is_end and sum(1 for c in text if c in vowels) > 1:
                result.append(rule['end_if_multivowel'])
            elif 'seq' in rule:
                result.append(rule['seq'])
            elif 'else' in rule:
                result.append(rule['else'])
            else:
                unknown_chars.add(char)
                result.append(char)
            i += 1
            continue

        # ← see `else` tuleb alati käivitada, kui pole special-reeglit
        if char in rules:
            result.append(rules[char])
        elif lang == "ld" and char in "abcdefghijklmnopqrstuvwxyz":
            result.append(char)  # lubab läbida ka tavalisi ladina tähti, kui neid pole mappingus
        elif lang == "ld" and not char.isalpha():
            result.append(char)  # lubab kirjavahemärgid jms
        else:
            unknown_chars.add(char)
            result.append(char)
        i += 1
        
    transliterated = ''.join(result)
    warnings = sorted(unknown_chars)
    if warnings:
        return None
    return (text, transliterated, warnings)

def rt_translit(text: str, lang: str) -> str | None:
    """Peamine transliteratsioonifunktsioon. Tagastab None, kui tundmatuid tähti leidub."""
    try:
        if not isinstance(text, str) or not isinstance(lang, str) or pd.isna(text) or pd.isna(lang):
            return None

        tokens = re.findall(r"[а-яА-ЯёЁіІїЇєЄґҐўЎ’']+|[^\w\s]+|\s+", text, re.UNICODE)
        transliterated_tokens = []

        for token in tokens:
            if any(c.isalpha() for c in token):
                result = transliterate_word(token, lang)
                if result is None:
                    return None
                _, translit, _ = result
                transliterated_tokens.append(translit)
            else:
                transliterated_tokens.append(token)

        result_str = ''.join(transliterated_tokens)

        if lang in {"ua","by"}:
            result_str = result_str.replace("’", "").replace("'", "")  # eemaldab ülakomad ainult UA ja BY skeemil

        return result_str

    except Exception:
        return None
