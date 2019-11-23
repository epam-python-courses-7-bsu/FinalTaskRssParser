from collections.abc import Collection


class LinksCollection(Collection):

    def __len__(self) -> int:
        return len(self.items_dict)

    def __contains__(self, __x: object) -> bool:
        return __x in self.items_dict

    def __iter__(self):
        return self.items_dict.__iter__()

    def __init__(self, initial=None):
        self.items_dict = dict()
        self._next_index_ = 1

        if initial is not None:
            for element in initial:
                self.add(element)

    def add(self, item):
        if item is not None and item not in self.items_dict:
            self.items_dict[item] = self._next_index_
            self._next_index_ += 1
        return self.items_dict[item]
