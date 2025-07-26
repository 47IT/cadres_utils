import pytest
from cadres_utils.list_utils import chunk_list


class TestChunkList:
    def test_chunk_list_even_division(self):
        lst = [1, 2, 3, 4, 5, 6]
        result = chunk_list(lst, 2)
        expected = [[1, 2], [3, 4], [5, 6]]
        assert result == expected

    def test_chunk_list_uneven_division(self):
        lst = [1, 2, 3, 4, 5]
        result = chunk_list(lst, 2)
        expected = [[1, 2], [3, 4], [5]]
        assert result == expected

    def test_chunk_list_chunk_size_equals_length(self):
        lst = [1, 2, 3]
        result = chunk_list(lst, 3)
        expected = [[1, 2, 3]]
        assert result == expected

    def test_chunk_list_chunk_size_greater_than_length(self):
        lst = [1, 2]
        result = chunk_list(lst, 5)
        expected = [[1, 2]]
        assert result == expected

    def test_chunk_list_chunk_size_one(self):
        lst = [1, 2, 3, 4]
        result = chunk_list(lst, 1)
        expected = [[1], [2], [3], [4]]
        assert result == expected

    def test_chunk_list_empty_list(self):
        lst = []
        result = chunk_list(lst, 2)
        expected = []
        assert result == expected

    def test_chunk_list_single_element(self):
        lst = [42]
        result = chunk_list(lst, 2)
        expected = [[42]]
        assert result == expected

    def test_chunk_list_string_elements(self):
        lst = ['a', 'b', 'c', 'd', 'e']
        result = chunk_list(lst, 3)
        expected = [['a', 'b', 'c'], ['d', 'e']]
        assert result == expected

    def test_chunk_list_mixed_types(self):
        lst = [1, 'a', 2.5, True, None, [1, 2]]
        result = chunk_list(lst, 2)
        expected = [[1, 'a'], [2.5, True], [None, [1, 2]]]
        assert result == expected

    def test_chunk_list_large_chunk_size(self):
        lst = list(range(100))
        result = chunk_list(lst, 10)
        assert len(result) == 10
        assert all(len(chunk) == 10 for chunk in result)
        assert result[0] == list(range(10))
        assert result[-1] == list(range(90, 100))

    def test_chunk_list_preserves_order(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = chunk_list(lst, 3)
        flattened = [item for chunk in result for item in chunk]
        assert flattened == lst