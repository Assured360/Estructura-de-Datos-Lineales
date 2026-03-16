class Queue:

    def __init__(self, initial_elements=[]):
        self._data = []
        self._push_count = 0
        self._pop_count = 0
        for element in initial_elements:
            self.push(element)

    def __str__(self):
        if self.isEmpty():
            return "Queue: []"
        items = " | ".join(str(i) for i in self._data)
        return (
            f"Queue (frente → final): [ {items} ]\n"
            f"  Tamaño   : {len(self)}\n"
            f"  Frente   : {self.peek()}\n"
            f"  Final    : {self._data[-1]}\n"
            f"  Entradas : {self._push_count}\n"
            f"  Salidas  : {self._pop_count}"
        )

    def __repr__(self):
        # Representación técnica de la cola
        return f"Queue({self._data!r})"

    def __len__(self):
        # Retorna la cantidad de elementos en la cola
        return len(self._data)

    def __eq__(self, other):
        # Compara si dos colas tienen los mismos elementos en el mismo orden
        if not isinstance(other, Queue):
            return False
        return self._data == other._data

    def __reversed__(self):
        # Permite recorrer la cola en orden inverso (de final a frente)
        return iter(self._data[::-1])

    def isEmpty(self):
        # Retorna True si la cola no tiene elementos
        return len(self._data) == 0

    def isFull(self, capacity):
        # Retorna True si la cola alcanzó la capacidad máxima indicada
        if capacity <= 0:
            raise ValueError("La capacidad debe ser un entero positivo")
        return len(self._data) >= capacity

    def peek(self):
        # Retorna el elemento del frente sin eliminarlo
        if self.isEmpty():
            raise IndexError("No se puede hacer peek en una cola vacía")
        return self._data[0]

    def peekRear(self):
        # Retorna el elemento del final sin eliminarlo
        if self.isEmpty():
            raise IndexError("No se puede hacer peek en una cola vacía")
        return self._data[-1]

    def __iter__(self):
        # Permite recorrer la cola con un for (de frente a final)
        return iter(self._data)

    def __contains__(self, element):
        # Retorna True si el elemento existe en la cola
        return element in self._data

    def push(self, element):
        # Encola: agrega el elemento al final de la cola
        self._data.append(element)
        self._push_count += 1

    def pushAll(self, elements):
        # Encola múltiples elementos a la vez desde cualquier iterable
        for element in elements:
            self.push(element)

    def pop(self):
        # Desencola: elimina y retorna el elemento del frente (FIFO)
        if self.isEmpty():
            raise IndexError("No se puede hacer pop en una cola vacía")
        self._pop_count += 1
        return self._data.pop(0)

    def popAll(self):
        # Desencola todos los elementos y los retorna como lista
        result = []
        while not self.isEmpty():
            result.append(self.pop())
        return result

    def clear(self):
        # Elimina todos los elementos y reinicia los contadores
        self._data.clear()
        self._push_count = 0
        self._pop_count = 0

    def copy(self):
        # Retorna una copia superficial de la cola
        nueva_cola = Queue()
        nueva_cola._data = self._data[:]
        nueva_cola._push_count = self._push_count
        nueva_cola._pop_count = self._pop_count
        return nueva_cola

    def toList(self):
        # Retorna el contenido de la cola como una lista (frente → final)
        return list(self._data)

    def stats(self):
        # Retorna un diccionario con estadísticas de uso de la cola
        return {
            "tamaño"          : len(self),
            "está_vacía"      : self.isEmpty(),
            "frente"          : self.peek() if not self.isEmpty() else None,
            "final"           : self.peekRear() if not self.isEmpty() else None,
            "total_encolados" : self._push_count,
            "total_desencolados": self._pop_count,
        }
