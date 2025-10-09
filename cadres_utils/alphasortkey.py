ALPHABET = 'АаБбВвГгҐґДдЕеЄєЖжЗзИиІіЇїЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЬьЮюЯя'
CHAR_ORDER = { char: idx for idx, char in enumerate(ALPHABET) }

# Usage:
#
# With list
#
# words = ['Яблуко', 'Абрикос', 'Ґава', 'Береза', 'Їжак', 'Єнот', 'Ілюзія', 'Дуб', 'Ґудзик']
# sorted(words, key=alphasortkey) # => ['Абрикос', 'Береза', 'Ґава', 'Ґудзик',
#                                 #     'Дуб', 'Єнот', 'Ілюзія', 'Їжак', 'Яблуко']
#
# with DataFrame:
#
# df.sort_values(by='name', key=lambda col: col.apply(alphasortkey))

def alphasortkey(val: str) -> tuple[int, ...]:
    if not isinstance(val, str):
        return val
    # Українські літери найперші та за алфавітом, решта за замовчуванням
    return tuple(CHAR_ORDER.get(char, 1000 + ord(char)) for char in val)
