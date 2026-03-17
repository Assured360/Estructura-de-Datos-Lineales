class Stack:
    
    def __init__(self, initial_elements=[]):
        self._data = list(initial_elements)
    
    def __str__(self):
        return f"Stack({self._data})"
    
    def __len__(self):
        return len(self._data)
    
    def isEmpty(self):
        return len(self._data) == 0
    
    def peek(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        return self._data[-1]
    
    def __iter__(self):
        return iter(reversed(self._data))
    
    def __contains__(self, element):
        return element in self._data
    
    def push(self, element):
        self._data.append(element)
    
    def pop(self, index=-1):
        if self.isEmpty():
            raise IndexError("Pop from empty stack")
        return self._data.pop(index)
