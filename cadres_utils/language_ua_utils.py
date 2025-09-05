from enum import Enum

HUNDRED = ['сто', 'двісті', 'триста', 'чотириста', 'п\'ятсот', 'шістсот', 'сімсот', 'вісімсот', 'дев\'ятсот']
TEN = ['двадцять', 'тридцять', 'сорок', 'п\'ятьдесят', 'шістьдесят', 'сімдесят', 'вісімдесят', 'дев\'яносто']
SINGLE_MALE = ['нуль', 'один', 'два', 'три', 'чотири', 'п\'ять', 'шість', 'сім', 'вісім', 'дев\'ять']
SINGLE_FEMALE = ['нуль', 'одна', 'дві', 'три', 'чотири', 'п\'ять', 'шість', 'сім', 'вісім', 'дев\'ять']
TEEN = ['десять', 'одинадцять', 'дванадцять', 'тринадцять', 'чотирнадцять', 'п\'ятнадцять', 'шістнадцять', 'сімнадцять', 'вісімнадцять', 'дев\'ятнадцять']


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'


def int_2_text_ukraine(int_val: int, gender: Gender) -> str:
    def __calc_less_100(val_2_proc: int) -> str:
        ten_val = val_2_proc // 10
        unit_val = val_2_proc % 10

        num_text = TEN[ten_val - 2]
        if unit_val > 0:
            num_text += f' {single_list[unit_val]}'
        return num_text

    if gender == Gender.MALE:
        single_list = SINGLE_MALE
    else:
        single_list = SINGLE_FEMALE

    if int_val < 10:
        res = single_list[int_val]
    elif int_val < 20:
        res = TEEN[int_val - 10]
    elif int_val < 100:
        res = __calc_less_100(int_val)
    elif int_val < 1000:
        hundred_val = int_val // 100
        rest_val = int_val % 100
        if rest_val == 0:
            res = HUNDRED[hundred_val - 1]
        else:
            res = f'{HUNDRED[hundred_val - 1]} {__calc_less_100(rest_val)}'
    else:
        raise ValueError('Підтримуються лише числа до 1000')

    return res

