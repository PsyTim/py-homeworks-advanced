class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_index = 0
        self.inner_index = 0

    def __iter__(self):
        return self

    def __next__(self):

        # Пропускаем пустые списки
        while self.outer_index < len(self.list_of_list) and self.inner_index >= len(
            self.list_of_list[self.outer_index]
        ):
            self.outer_index += 1
            self.inner_index = 0

        # Если дошли до конца всех списков
        if self.outer_index >= len(self.list_of_list):

            raise StopIteration

        # Получаем текущий элемент
        item = self.list_of_list[self.outer_index][self.inner_index]
        self.inner_index += 1

        # item = None
        return item


def test_1():

    list_of_lists_1 = [["a", "b", "c"], ["d", "e", "f", "h", False], [1, 2, None]]

    for flat_iterator_item, check_item in zip(
        FlatIterator(list_of_lists_1),
        ["a", "b", "c", "d", "e", "f", "h", False, 1, 2, None],
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "h",
        False,
        1,
        2,
        None,
    ]


if __name__ == "__main__":
    test_1()
