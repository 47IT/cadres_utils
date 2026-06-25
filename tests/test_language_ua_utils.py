import pytest
from cadres_utils.language_ua_utils import number_to_words, Gender


class TestNumberToWords:
    def test_single_digits_male(self):
        expected_male = [
            'нуль', 'один', 'два', 'три', 'чотири',
            'п’ять', 'шість', 'сім', 'вісім', 'дев’ять'
        ]
        for i, expected in enumerate(expected_male):
            assert number_to_words(i, Gender.MALE) == expected

    def test_single_digits_female(self):
        expected_female = [
            'нуль', 'одна', 'дві', 'три', 'чотири',
            'п’ять', 'шість', 'сім', 'вісім', 'дев’ять'
        ]
        for i, expected in enumerate(expected_female):
            assert number_to_words(i, Gender.FEMALE) == expected

    def test_teens(self):
        expected_teens = [
            'десять', 'одинадцять', 'дванадцять', 'тринадцять', 'чотирнадцять',
            'п’ятнадцять', 'шістнадцять', 'сімнадцять', 'вісімнадцять', 'дев’ятнадцять'
        ]
        for i, expected in enumerate(expected_teens):
            assert number_to_words(i + 10, Gender.MALE) == expected
            assert number_to_words(i + 10, Gender.FEMALE) == expected

    def test_multiples_of_ten(self):
        expected_tens = {
            20: 'двадцять',
            30: 'тридцять',
            40: 'сорок',
            50: 'п’ятдесят',
            60: 'шістдесят',
            70: 'сімдесят',
            80: 'вісімдесят',
            90: 'дев’яносто'
        }
        for number, expected in expected_tens.items():
            assert number_to_words(number, Gender.MALE) == expected
            assert number_to_words(number, Gender.FEMALE) == expected

    def test_two_digit_combinations_male(self):
        test_cases = {
            21: 'двадцять один',
            35: 'тридцять п’ять',
            42: 'сорок два',
            67: 'шістдесят сім',
            89: 'вісімдесят дев’ять',
            91: 'дев’яносто один',
            92: 'дев’яносто два'
        }
        for number, expected in test_cases.items():
            assert number_to_words(number, Gender.MALE) == expected

    def test_two_digit_combinations_female(self):
        test_cases = {
            21: 'двадцять одна',
            32: 'тридцять дві',
            41: 'сорок одна',
            52: 'п’ятдесят дві',
            61: 'шістдесят одна',
            72: 'сімдесят дві',
            81: 'вісімдесят одна',
            92: 'дев’яносто дві'
        }
        for number, expected in test_cases.items():
            assert number_to_words(number, Gender.FEMALE) == expected

    def test_hundreds_exact(self):
        expected_hundreds = {
            100: 'сто',
            200: 'двісті',
            300: 'триста',
            400: 'чотириста',
            500: 'п’ятсот',
            600: 'шістсот',
            700: 'сімсот',
            800: 'вісімсот',
            900: 'дев’ятсот'
        }
        for number, expected in expected_hundreds.items():
            assert number_to_words(number, Gender.MALE) == expected
            assert number_to_words(number, Gender.FEMALE) == expected


    def test_thousands(self):
        expected_hundreds = {
            1000: 'одна тисяча',
            2000: 'дві тисячі',
            3000: 'три тисячі',
            4000: 'чотири тисячі',
            5000: 'п’ять тисяч',
            6000: 'шість тисяч',
            7000: 'сім тисяч',
            8000: 'вісім тисяч',
            9000: 'дев’ять тисяч',
        }
        for number, expected in expected_hundreds.items():
            assert number_to_words(number, Gender.MALE) == expected
            assert number_to_words(number, Gender.FEMALE) == expected

    def test_three_digit_combinations_male(self):
        test_cases = {
            123: 'сто двадцять три',
            234: 'двісті тридцять чотири',
            345: 'триста сорок п’ять',
            456: 'чотириста п’ятдесят шість',
            567: 'п’ятсот шістдесят сім',
            678: 'шістсот сімдесят вісім',
            789: 'сімсот вісімдесят дев’ять',
            891: 'вісімсот дев’яносто один',
            999: 'дев’ятсот дев’яносто дев’ять'
        }
        for number, expected in test_cases.items():
            assert number_to_words(number, Gender.MALE) == expected

    def test_three_digit_combinations_female(self):
        test_cases = {
            121: 'сто двадцять одна',
            132: 'сто тридцять дві',
            241: 'двісті сорок одна',
            352: 'триста п’ятдесят дві',
            461: 'чотириста шістдесят одна',
            572: 'п’ятсот сімдесят дві',
            681: 'шістсот вісімдесят одна',
            792: 'сімсот дев’яносто дві'
        }
        for number, expected in test_cases.items():
            assert number_to_words(number, Gender.FEMALE) == expected

    def test_four_digit_combinations_male(self):
        test_cases = {
            1121: 'одна тисяча сто двадцять один',
            9999: 'дев’ять тисяч дев’ятсот дев’яносто дев’ять'
        }
        for number, expected in test_cases.items():
            assert number_to_words(number, Gender.MALE) == expected

    def test_four_digit_combinations_female(self):
        test_cases = {
            1121: 'одна тисяча сто двадцять одна',
            9999: 'дев’ять тисяч дев’ятсот дев’яносто дев’ять'
        }
        for number, expected in test_cases.items():
            assert number_to_words(number, Gender.FEMALE) == expected

    def test_edge_case_error_for_numbers_over_9999(self):
        assert number_to_words(10001, Gender.FEMALE) == '10001'
        assert number_to_words(99999, Gender.MALE) == '99999'
        assert number_to_words(-1, Gender.MALE) == '-1'

    def test_boundary_values(self):
        assert number_to_words(0, Gender.MALE) == 'нуль'
        assert number_to_words(0, Gender.FEMALE) == 'нуль'
        assert number_to_words(999, Gender.MALE) == 'дев’ятсот дев’яносто дев’ять'
        assert number_to_words(999, Gender.FEMALE) == 'дев’ятсот дев’яносто дев’ять'

    def test_custom_cases(self):
        test_cases = {
            130: 'сто тридцять',
        }
        for number, expected in test_cases.items():
            assert number_to_words(number, Gender.FEMALE) == expected
