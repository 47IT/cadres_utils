from enum import Enum

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'


_ONES = {
    1: {Gender.MALE: "один", Gender.FEMALE: "одна"},
    2: {Gender.MALE: "два", Gender.FEMALE: "дві"},
    3: "три",
    4: "чотири",
    5: "п’ять",
    6: "шість",
    7: "сім",
    8: "вісім",
    9: "дев’ять",
}

_TEENS = {
    10: "десять",
    11: "одинадцять",
    12: "дванадцять",
    13: "тринадцять",
    14: "чотирнадцять",
    15: "п’ятнадцять",
    16: "шістнадцять",
    17: "сімнадцять",
    18: "вісімнадцять",
    19: "дев’ятнадцять",
}

_TENS = {
    2: "двадцять",
    3: "тридцять",
    4: "сорок",
    5: "п’ятдесят",
    6: "шістдесят",
    7: "сімдесят",
    8: "вісімдесят",
    9: "дев’яносто",
}

_HUNDREDS = {
    1: "сто",
    2: "двісті",
    3: "триста",
    4: "чотириста",
    5: "п’ятсот",
    6: "шістсот",
    7: "сімсот",
    8: "вісімсот",
    9: "дев’ятсот",
}


def _under_1000(n: int, gender: Gender) -> list[str]:
    words = []
    h, rem = divmod(n, 100)
    if h:
        words.append(_HUNDREDS[h])
    if 10 <= rem <= 19:
        words.append(_TEENS[rem])
    else:
        t, o = divmod(rem, 10)
        if t:
            words.append(_TENS[t])
        if o:
            val = _ONES[o]
            words.append(val[gender] if isinstance(val, dict) else val)
    return words


def _thousand_word(count: int) -> str:
    if count == 1:
        return "тисяча"
    if count in (2, 3, 4):
        return "тисячі"
    return "тисяч"


def number_to_words(value: int, gender: Gender) -> str:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 9999:
        return str(value)
    if value == 0:
        return "нуль"

    words = []
    thousands, rest = divmod(value, 1000)
    if thousands:
        words += _under_1000(thousands, Gender.FEMALE)  # тисяча is feminine
        words.append(_thousand_word(thousands))
    if rest:
        words += _under_1000(rest, gender)
    return " ".join(words)

# DEPRECATED: use new name unless you're 13 years old who's 2cool4school
int_2_text_ukraine=number_to_words
