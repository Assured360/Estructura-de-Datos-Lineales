class ArrayList:
    # size: initial capacity of the collection
    # initial_elements: allow the collection to start with some elements
    def __init__(self, size=100, initial_elements=None):
        if initial_elements is None:
            initial_elements = []
        
        # Configuramos la capacidad inicial (respetando si los elementos iniciales la superan)
        self._capacity = max(size, len(initial_elements))
        self._array = [None] * self._capacity
        self._size = 0
        
        for element in initial_elements:
            self.append(element)

    # return an str of the collection
    def __str__(self):
        return "[" + ", ".join(str(self._array[i]) for i in range(self._size)) + "]"

    # return the length of the elements in the collection
    def __len__(self):
        return self._size

    # return a boolean that implies if the collection is empty or not
    def isEmpty(self):
        return self._size == 0

    # return the element of the collection in the index position
    # Error: the index dont exist
    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Error: El índice no existe en la colección.")
        return self._array[index]

    # allow the collection to be called in a for loop
    def __iter__(self):
        for i in range(self._size):
            yield self._array[i]

    # return a boolean value representing the existence of an element in the collection
    def contains(self, element):
        for i in range(self._size):
            if self._array[i] == element:
                return True
        return False

    # Método interno para redimensionar el arreglo si se llena
    def _resize(self):
        self._capacity *= 2
        new_array = [None] * self._capacity
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array

    # add the element to the end of the collection
    def append(self, element):
        if self._size == self._capacity:
            self._resize()
        self._array[self._size] = element
        self._size += 1

    # add the element to the collection at the requested index
    # Error: non existing index in the collection
    def insert(self, index, element):
        if index < 0 or index > self._size:
            raise IndexError("Error: Índice inexistente en la colección.")
        
        if self._size == self._capacity:
            self._resize()
            
        # Desplazamos los elementos hacia la derecha para hacer espacio
        for i in range(self._size, index, -1):
            self._array[i] = self._array[i-1]
            
        self._array[index] = element
        self._size += 1

    # remove an element in the collection by its value
    # Error: the element dont exist in the collection
    def remove(self, element):
        for i in range(self._size):
            if self._array[i] == element:
                # Desplazamos los elementos hacia la izquierda para tapar el hueco
                for j in range(i, self._size - 1):
                    self._array[j] = self._array[j+1]
                self._array[self._size - 1] = None
                self._size -= 1
                return
        raise ValueError("Error: El elemento no existe en la colección.")

    # remove and return the element in the collection by its index
    def pop(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Error: El índice no existe en la colección.")
            
        element = self._array[index]
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i+1]
        
        self._array[self._size - 1] = None
        self._size -= 1
        return element

    # remove all elements in the collection
    def clear(self):
        self._array = [None] * self._capacity
        self._size = 0
