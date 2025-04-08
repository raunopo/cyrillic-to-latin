# Cyrillic-to-Latin Transliteration Schemes

**Last updated: 08.04.2025**

This repository contains rule-based transliteration modules for converting names from Cyrillic to Latin characters using various international and national standards.

---

### ⚠️ Handling unmapped characters and missing language input

For functions that require a language code (`text`, `lang`), the `lang` parameter must be explicitly provided (e.g., `"ru"`, `"ua"`, `"by"`). If this value is missing or unsupported, the function may raise an error or return `None`.

When the input text contains only characters that are not covered by the selected transliteration scheme (i.e., unmapped or invalid symbols), most modules will return **`None`**, indicating that no valid output could be produced. Some implementations, such as `rt_translit`, may return an **empty string** (`""`) instead.

---

### 🔤 Supported Transliteration Schemes

| Module        | Description |
|---------------|-------------|
| `iso9`        | **ISO 9:1995** — International Organization for Standardization – Transliteration of Cyrillic characters into Latin characters. [Wikipedia](https://en.wikipedia.org/wiki/ISO_9) |
| `icao`        | **ICAO Doc 9303** — International Civil Aviation Organization – Machine Readable Travel Documents (MRTD) transliteration standard. [PDF](https://www.icao.int/publications/Documents/9303_p3_cons_en.pdf) |
| `bgn`         | **BGN/PCGN** — Board on Geographic Names (USA) and Permanent Committee on Geographical Names (UK). Romanization system for geographic names. [Wikipedia](https://en.wikipedia.org/wiki/BGN/PCGN_romanization) |
| `gost_b`      | **GOST 7.79 B** — Russian national standard for information, library, and publishing transliteration. ГОСТ 7.79–2000. «Система стандартов по информации, библиотечному и издательскому делу. Правила транслитерации кирилловского письма латинским алфавитом» [PDF](https://ifap.ru/library/gost/7792000.pdf)|
| `dstu_a`      | **DSTU 9112:2021 (System A)** — State Standard of Ukraine. Official rules for Cyrillic–Latin transliteration and re-transliteration. Державний стандарт України. Кирилично-латинична транслітерація та латинично-кирилична ретранслітерація українських текстів. Правила написання [DOI](https://doi.org/10.32388/VH8DLJ) |
| `dstu_b`      | **DSTU 9112:2021 (System B)** — Alternative system under DSTU for Ukrainian texts. Державний стандарт України. Кирилично-латинична транслітерація та латинично-кирилична ретранслітерація українських текстів. Правила написання [DOI](https://doi.org/10.32388/VH8DLJ)|
| `blr`         | **Belarus Decree No. 288** — Transliteration instruction by the Ministry of Internal Affairs of the Republic of Belarus. ПОСТАНОВЛЕНИЕ МВД РБ № 288 (8/19678) «Об утверждении Инструкции по транслитерации фамилий и собственных имен граждан Республики Беларусь при включении их персональных данных в регистр населения» [PDF](https://pravo.by/document/?guid=2012&oldDoc=2008-261/2008-261(081-092).pdf&oldDocPage=1)|
| `rt_translit` | **Estonian Government Regulation** — Tähetabel nr 1: Transcription of Russian names into Estonian documents. [Act](https://www.riigiteataja.ee/akt/131072019013)|
| `rt_transcrib`| **Estonian Government Regulation** — Tähetabelid nr 2, 8, 9: Transliteration of Russian, Ukrainian, and Belarusian names into Estonian documents. [Act](https://www.riigiteataja.ee/akt/131072019013)|
| `eki`         | **Estonian Language Institute** — Transliteration tables for Russian–Latin, Belarusian–Latin, and Ukrainian–Latin. [EKI](https://www.eki.ee) |

---

### 🧪 Example usage

```python
import pandas as pd
from module_blr import blr
from module_bgn import bgn
from module_dstu_a import dstu_a
from module_dstu_b import dstu_b
from module_eki import eki
from module_gost_b import gost_b
from module_icao import icao
from module_iso9 import iso9
from module_rt_translit import rt_translit
from module_rt_transcrib import rt_transcrib

# Sample input names
df_test = pd.DataFrame({
    "input_name": [
        "євгеній борисенко",               # Ukrainian, includes ї and є
        "ульянов сергей владимирович",     # Russian, includes patronymic
        "пятроў ігар",                     # Belarusian, includes ў
        "сёмина анна-людмила",             # Hyphenated Russian name
        "александрова (кузьміна) анна",    # Alternative surname in parentheses
        "джон сміт",                       # Western name in Cyrillic
        "лю юйчжун",                       # Chinese name in Cyrillic
        "шарифзаде мухаммад",              # Persian-origin name
        "ніна іванівна",                   # Ukrainian name with patronymic only
        "густаво адольфо"                  # Latin-American name in Cyrillic
    ],
    "lang": ["ua", "ru", "by", "ru", "ru", "ru", "ru", "ru", "ua", "ru"]
})

# Single-argument functions
df_test["dstu_b"] = df_test["input_name"].apply(dstu_b)
df_test["icao"] = df_test["input_name"].apply(icao)
df_test["iso9"] = df_test["input_name"].apply(iso9)
df_test["rt_transcrib"] = df_test["input_name"].apply(rt_transcrib)

# Two-argument functions (require language code)
df_test["bgn"] = df_test.apply(lambda row: bgn(row["input_name"], row["lang"]), axis=1)
df_test["blr"] = df_test.apply(lambda row: blr(row["input_name"], row["lang"]), axis=1)
df_test["dstu_a"] = df_test.apply(lambda row: dstu_a(row["input_name"], row["lang"]), axis=1)
df_test["rt_translit"] = df_test.apply(lambda row: rt_translit(row["input_name"], row["lang"]), axis=1)
df_test["eki"] = df_test.apply(lambda row: eki(row["input_name"], row["lang"]), axis=1)
df_test["gost_b"] = df_test.apply(lambda row: gost_b(row["input_name"], row["lang"]), axis=1)

print(df_test)
