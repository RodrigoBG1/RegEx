import math

class HeapNode:
    def __init__(self, key, value = None):
        self.key = key
        self.value = value

class Heap:
    def __init__(self):
        self.heap = []
        self.size = 0

    # Regresa el indice del padre del nodo en este indice
    def parent(self, i):
        return i // 2

    # Regresa el indice del hijo izquierdo del nodo en i
    def left_child(self, i):
        return i * 2

    # Regresa el indice del hijo derecho del nodo en i
    def right_child(self, i):
        return i * 2 + 1
    
    def heapify(self, idx):
        # Obtener el indice de los dos hijos
        left_idx = self.left_child(idx)
        right_idx = self.right_child(idx)

        if left_idx <= self.size and self.heap[left_idx].key < self.heap[idx].key: #PARA EL MIN HEAP CAMBIA EL SEGUNDO A < 
            largest_idx = left_idx
        else:
            largest_idx = idx

        # Compara el hijo derecho con el largest index
        if right_idx <= self.size and self.heap[right_idx].key < self.heap[largest_idx].key: # PARA EL MIN HEAP CAMBIA EL SEGUNDO A < 
            largest_idx = right_idx

        if largest_idx != idx:
            # Intercambiamos elementos
            aux = self.heap[idx]
            self.heap[idx] = self.heap[largest_idx]
            self.heap[largest_idx] = aux
            self.heapify(largest_idx)            #EL LARGEST_IDX NO CAMBIA
    
    def array(self, listac):
        # Crear una lista de objetos HeapNode a partir de una lista de números
        array = [HeapNode(x,x) for x in listac]
        self.build_heap(array)

    def build_heap(self, elements):
        self.heap = elements

        # Hacemos el size igual al tamaño del arreglo
        self.size = len(self.heap)

        self.heap.insert(0, HeapNode(-1))

        # Hacer un ciclo desde la mitad del heap hasta 1
        # Para cada elemento llamar a al funcion heapify con su indice
        for i in range(self.size // 2, 0, -1):
            self.heapify(i)

    def pop(self):
        # Comprobar que haya elementos en el heap
        if (self.size >= 1):
            # Guardamos el elemento raíz en un aux
            aux = self.heap[1]

            # Movemos el último elemento del heap a la raiz
            self.heap[1] = self.heap[self.size]
        
            # Reducimos el  tamaño del heap en 1
            self.size -= 1 #NUNCA SE BORRA EL ULTIMO ELEMENTO SIMPLEMENTE SE IMPRIME EL TAMAÑO DEL HEAP -1
                           #PERO SI UTILIZAMOS ESTA FUNCION "self.heap.pop()" o "del self.heap[self.size-1]" SI LO ELIMINA
            self.heap.pop()

            # Llamamos a la función heapify con la raíz
            self.heapify(1)
            
            # Regresamos el aux
            return aux.key
    
    def get_size(self):
        return self.size
    
    def heap_increase_key(self, index, key):
        if key <= self.heap[index].key:  #PARA EL MIN HEAP CAMBIA A < 
            self.heap[index].key = key
            self.heap[index].value = key
            padre_idx = self.parent(index)
            while index > 1 and self.heap[index].key < self.heap[padre_idx].key: #PARA EL MIN HEAP CAMBIA A <  
                aux = self.heap[padre_idx]
                self.heap[padre_idx] = self.heap[index]
                self.heap[index] = aux
                index = padre_idx
                padre_idx = self.parent(index)
        else:
            return "El valor es menor al actual"
    
    def heap_insert(self, key, value):
        self.size += 1
        #self.heap.insert(self.size, HeapNode(-math.inf, value)) #EN ESTE TIENES QUE DECIR DONDE LO QUIERES METER OSEA EL INDICE
        
        if self.size >= len(self.heap) - 1:
            self.heap.append(HeapNode(math.inf, value)) # PARA EL MIN HEAP CAMBIA A +
        else:
            self.heap[self.size] = HeapNode(math.inf, value) # PARA EL MIN HEAP CAMBIA A +

        self.heap_increase_key(self.size, value)