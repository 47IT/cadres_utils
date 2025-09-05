import pytest
from cadres_utils.language_ua_utils import int_2_text_ukraine, Gender


class TestInt2TextUkraine:
    
    def test_single_digits_male(self):
        expected_male = [
            'нуль', 'один', 'два', 'три', 'чотири', 
            'п\'ять', 'шість', 'сім', 'вісім', 'дев\'ять'
        ]
        for i, expected in enumerate(expected_male):
            assert int_2_text_ukraine(i, Gender.MALE) == expected
    
    def test_single_digits_female(self):
        expected_female = [
            'нуль', 'одна', 'дві', 'три', 'чотири',
            'п\'ять', 'шість', 'сім', 'вісім', 'дев\'ять'
        ]
        for i, expected in enumerate(expected_female):
            assert int_2_text_ukraine(i, Gender.FEMALE) == expected
    
    def test_teens(self):
        expected_teens = [
            'десять', 'одинадцять', 'дванадцять', 'тринадцять', 'чотирнадцять',
            'п\'ятнадцять', 'шістнадцять', 'сімнадцять', 'вісімнадцять', 'дев\'ятнадцять'
        ]
        for i, expected in enumerate(expected_teens):
            assert int_2_text_ukraine(i + 10, Gender.MALE) == expected
            assert int_2_text_ukraine(i + 10, Gender.FEMALE) == expected
    
    def test_multiples_of_ten(self):
        expected_tens = {
            20: 'двадцять',
            30: 'тридцять', 
            40: 'сорок',
            50: 'п\'ятьдесят',
            60: 'шістьдесят',
            70: 'сімдесят',
            80: 'вісімдесят',
            90: 'дев\'яносто'
        }
        for number, expected in expected_tens.items():
            assert int_2_text_ukraine(number, Gender.MALE) == expected
            assert int_2_text_ukraine(number, Gender.FEMALE) == expected
    
    def test_two_digit_combinations_male(self):
        test_cases = {
            21: 'двадцять один',
            35: 'тридцять п\'ять',
            42: 'сорок два',
            67: 'шістьдесят сім',
            89: 'вісімдесят дев\'ять',
            91: 'дев\'яносто один',
            92: 'дев\'яносто два'
        }
        for number, expected in test_cases.items():
            assert int_2_text_ukraine(number, Gender.MALE) == expected
    
    def test_two_digit_combinations_female(self):
        test_cases = {
            21: 'двадцять одна',
            32: 'тридцять дві',
            41: 'сорок одна',
            52: 'п\'ятьдесят дві',
            61: 'шістьдесят одна',
            72: 'сімдесят дві',
            81: 'вісімдесят одна',
            92: 'дев\'яносто дві'
        }
        for number, expected in test_cases.items():
            assert int_2_text_ukraine(number, Gender.FEMALE) == expected
    
    def test_hundreds_exact(self):
        expected_hundreds = {
            100: 'сто',
            200: 'двісті',
            300: 'триста',
            400: 'чотириста',
            500: 'п\'ятсот',
            600: 'шістсот',
            700: 'сімсот',
            800: 'вісімсот',
            900: 'дев\'ятсот'
        }
        for number, expected in expected_hundreds.items():
            assert int_2_text_ukraine(number, Gender.MALE) == expected
            assert int_2_text_ukraine(number, Gender.FEMALE) == expected
    
    def test_three_digit_combinations_male(self):
        test_cases = {
            123: 'сто двадцять три',
            234: 'двісті тридцять чотири',
            345: 'триста сорок п\'ять',
            456: 'чотириста п\'ятьдесят шість',
            567: 'п\'ятсот шістьдесят сім',
            678: 'шістсот сімдесят вісім',
            789: 'сімсот вісімдесят дев\'ять',
            891: 'вісімсот дев\'яносто один',
            999: 'дев\'ятсот дев\'яносто дев\'ять'
        }
        for number, expected in test_cases.items():
            assert int_2_text_ukraine(number, Gender.MALE) == expected
    
    def test_three_digit_combinations_female(self):
        test_cases = {
            121: 'сто двадцять одна',
            132: 'сто тридцять дві',
            241: 'двісті сорок одна',
            352: 'триста п\'ятьдесят дві',
            461: 'чотириста шістьдесят одна',
            572: 'п\'ятсот сімдесят дві',
            681: 'шістсот вісімдесят одна',
            792: 'сімсот дев\'яносто дві'
        }
        for number, expected in test_cases.items():
            assert int_2_text_ukraine(number, Gender.FEMALE) == expected
    
    def test_edge_case_error_for_numbers_over_1000(self):
        with pytest.raises(ValueError, match='Підтримуються лише числа до 1000'):
            int_2_text_ukraine(1000, Gender.MALE)
        
        with pytest.raises(ValueError, match='Підтримуються лише числа до 1000'):
            int_2_text_ukraine(1001, Gender.FEMALE)
        
        with pytest.raises(ValueError, match='Підтримуються лише числа до 1000'):
            int_2_text_ukraine(5000, Gender.MALE)
    
    def test_boundary_values(self):
        assert int_2_text_ukraine(0, Gender.MALE) == 'нуль'
        assert int_2_text_ukraine(0, Gender.FEMALE) == 'нуль'
        assert int_2_text_ukraine(999, Gender.MALE) == 'дев\'ятсот дев\'яносто дев\'ять'
        assert int_2_text_ukraine(999, Gender.FEMALE) == 'дев\'ятсот дев\'яносто дев\'ять'

    def test_custom_cases(self):
        test_cases = {
            130: 'сто тридцять',
        }
        for number, expected in test_cases.items():
            assert int_2_text_ukraine(number, Gender.FEMALE) == expected
