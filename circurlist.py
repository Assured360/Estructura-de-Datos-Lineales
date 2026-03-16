
    def _init_(self, data):
        self.data = data
        self.next = None
        self.prev = None


class CircularList:

    def _init_(self, initial_elements=[]):
        self._head = None
        self._size = 0
        for element in initial_elements:
            self.append(element)

    def _str_(self):
        if self.isEmpty():
            return "[]"
        result = []
        current = self._head
        for _ in range(self._size):
            result.append(str(current.data))
            current = current.next
        return "[" + " <-> ".join(result) + " (circular)]"

    def _len_(self):
        return self._size

    def _getitem_(self, index):
        if index < 0 or index >= self._siz… Leer más
2:30 p.m.
