class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
        

class CircularList:

    def __init__(self, initial_elements=[]):
        self._head = None
        self._size = 0
        for element in initial_elements:
            self.append(element)

    def __str__(self):
        if self.isEmpty():
            return "[]"
        result = []
        current = self._head
        for _ in range(self._size):
            result.append(str(current.data))
            current = current.next
        return "[" + " <-> ".join(result) + " (circular)]"

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for list of size {self._size}")
        current = self._head
        for _ in range(index):
            current = current.next
        return current.data

    def isEmpty(self):
        return self._size == 0

    def __iter__(self):
        if self.isEmpty():
            return
        current = self._head
        for _ in range(self._size):
            yield current.data
            current = current.next

    def __contains__(self, element):
        for item in self:
            if item == element:
                return True
        return False

    def append(self, element):
        new_node = Node(element)
        if self.isEmpty():
            new_node.next = new_node
            new_node.prev = new_node
            self._head = new_node
        else:
            tail = self._head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self._head
            self._head.prev = new_node
        self._size += 1

    def add(self, index, element):
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range")
        if index == self._size:
            self.append(element)
            return
        new_node = Node(element)
        if index == 0:
            if self.isEmpty():
                new_node.next = new_node
                new_node.prev = new_node
            else:
                tail = self._head.prev
                new_node.next = self._head
                new_node.prev = tail
                self._head.prev = new_node
                tail.next = new_node
            self._head = new_node
        else:
            current = self._head
            for _ in range(index):
                current = current.next
            prev_node = current.prev
            prev_node.next = new_node
            new_node.prev = prev_node
            new_node.next = current
            current.prev = new_node
        self._size += 1

    def remove(self, element):
        if self.isEmpty():
            raise ValueError(f"Element '{element}' not found in list")
        current = self._head
        for _ in range(self._size):
            if current.data == element:
                if self._size == 1:
                    self._head = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self._head:
                        self._head = current.next
                self._size -= 1
                return
            current = current.next
        raise ValueError(f"Element '{element}' not found in list")

    def pop(self, index):
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range")
        current = self._head
        for _ in range(index):
            current = current.next
        data = current.data
        if self._size == 1:
            self._head = None
        else:
            current.prev.next = current.next
            current.next.prev = current.prev
            if current == self._head:
                self._head = current.next
        self._size -= 1
        return data

    def clear(self):
        self._head = None
        self._size = 0
