from BMHBusquedaSimple import BMHMatching1
from BMHModificado import BMHMatching
from BMHModificado2 import BMHMatching2
from MinHeap import Heap

class Proyecto:
	def __init__(self):
	 	self.text = ""

class Regex:
	def leer_archivo(self, nombre):
		with open(nombre,'r') as file:
			self.text = file.read()

	def ingresar_tipo_de_busqueda(self):
		patt = input("Ingresa el patron: ")
		n1 = self.char_to_index(patt[1])
		matches = []
		pattern = patt

		if patt[-1:] == 'i':
			patternaux = patt
			self.text = self.text.lower()
			pattern = patt.lower()
			pattern = patt[:-2]
		if  patt[-3:] == "g i":
			self.text = self.text.lower()
			pattern = patt.lower()
			pattern = patt[:-4]
			patternaux = patt[:-2]
		if  patt[-1:] == 'g':
			patternaux = patt
			pattern = patt[:-2]

		if n1 == 32:
			pattern1 = pattern[2:]
			matches = self.operacion(pattern1)
		else:
			patter = pattern[3:]
			pattern1, new_word = patter.split('/')
			matches = self.operacion(pattern1)
			if not matches:
				print("No hubo coincidencias por lo tanto no se puede remplazar")
			else:
				print(self.replace(matches[0], matches[1], new_word))
			
		if  patternaux[-1:] == 'g':
			if len(matches[0]) > 0:
				primer_incidencia = matches[0][0]
				return primer_incidencia
			else: 
				return 'No se encontraron coincidencias para el patron '
		else:
			return matches[0]

	def get_text(self, text):
		self.text = text
  
	def operacion(self, pattern):
		a = -1
		for i in range(len(pattern)):
			if pattern[i] == '|':
				a = 4
				break
		if a != 4:
			for i in range(len(pattern)):
				if pattern[i] == '-':
					a = 1
					break
				elif pattern[i] == ']':
					a = 2
					break
				elif pattern[i] == '?':
					a = 3
					break
				elif pattern[i] == '{':
					a = 5
					break
				elif pattern[i] == '*':
					a = 6
					break
				else:
					a = 0

		if a == -1:
			print("Patron no valido")
		elif a == 0:
			return self.busqueda_simple(pattern)
		elif a == 1:
			return self.rangos_letras_numeros(pattern)
		elif a == 2:
			return self.conjunto_letras_corchetes(pattern)
		elif a == 3:
			return self.interrogacion(pattern)
		elif a == 4:
			return self.or_logico(pattern)
		elif a == 5:
			return self.operdador_de_repeticion(pattern)
		elif a == 6:
			return self.comodin(pattern)

	def char_to_index(self, char):
		if type(char) is int:
			n = char
		else:
			n = ord(char)
		return n

	def index_to_char(self, index):
		n = chr(index)
		return n
	
	def replace(self, matches, pattern, new_word):
		string = self.text
		n = 0
		for i in range(len(matches)):
			if matches[i] == 0:
				aux = string[len(pattern):len(string) + 1]
				string = new_word + aux
			else:
				if len(new_word) <= len(pattern):
					n += len(pattern) - len(new_word)
					aux = string[:matches[i] - n]
					aux2 = string[len(aux) + len(pattern): len(string) + 1]
					string = aux + new_word + aux2
				else: #Si se lo quito aun asi lo hace bien
					n += len(new_word) - len(pattern)
					aux = string[:matches[i] + n]
					aux2 = string[len(aux) + len(pattern): len(string) + 1]
					string = aux + new_word + aux2
		self.text = string
		return self.text
        
	def busqueda_simple(self, pattern):
		string = self.text
		BMHBusquedaSimple = BMHMatching1()
		BMHBusquedaSimple.set_text(string) 
		matches = BMHBusquedaSimple.search(pattern)
		return matches, pattern
	
	def rangos_letras_numeros(self, patt):
		#El peor caso es cuando sea [a-z] y este a lado del ultimo digito -> [a-z]q
		print(patt)
		pattern = ""
		i = 0
		while i < len(patt):
			if patt[i] == '[':
				idx = len(patt) - (i+1 + 4)
				p1 = patt[i+1]
				p2 = patt[i+3]
				pattern += '-'
				i += 5
			else:
				pattern += patt[i]
				i += 1
		n1 = self.char_to_index(p1)
		n2 = self.char_to_index(p2)
		string = self.text 
		print(pattern)
		BMHModificado = BMHMatching()
		BMHModificado.set_text(string)
		return BMHModificado.search(idx, n1, n2, pattern), pattern

	def operdador_de_repeticion(self, patt):
		#a{5}cd
		print(patt)
		pattern = ""
		i = 0
		while i < len(patt):
			if patt[i] == '{':
				pattern += patt[i-1] * (int(patt[i+1])-1)
				i += 3
			else:
				pattern += patt[i]
				i += 1 
		return self.busqueda_simple(pattern)

	def or_logico(self, pattern):
		lista_ordenada = []
		patt1, patt2 = pattern.split('|')
		lista1 = self.operacion(patt1)
		lista2 = self.operacion(patt2)
		listac = lista1[0] + lista2[0]

		min_heap = Heap()
		min_heap.array(list(set(listac)))
		while min_heap.get_size() != 0:
			lista_ordenada.append(min_heap.pop())

		if patt1 > patt2:
			return lista_ordenada, patt1
		else:
			return lista_ordenada, patt2
	
	def interrogacion(self, patt):
		patt1 = ""
		patt2 = ""
		i = 0
		lista_ordenada = []

		while i < len(patt):
			if patt[i] == '?':
				if i > 0:
					patt2 = patt2[:-1]
			else:
				patt1 += patt[i]
				patt2 += patt[i]
			i += 1
		string = self.text

		c = []
		j = 0
		h = 0

		s1 = self.busqueda_simple(patt1)
		lista1 = s1[0]
		s2 = self.busqueda_simple(patt2)
		lista2 = s2[0]
		listac = lista1 + lista2

		min_heap = Heap()
		min_heap.array(list(set(listac)))
		while min_heap.get_size() != 0:
			lista_ordenada.append(min_heap.pop())
		return lista_ordenada, patt


	def comodin(self, pattern):
		string = self.text
		patt1, patt2 = pattern.split('*')
		patt = ""
		result_string = []
		lista_ordenada = []

		for i in range(64, 123):
			n = self.index_to_char(i)      
			if patt2 is not None:
				patt = patt1 + n + patt2

			else: 
				patt = patt1 + n
			s = self.busqueda_simple(patt)
			resultado = s[0]
			
			if len(resultado) > 0:
				result_string += resultado
		
		min_heap = Heap()
		min_heap.array(list(set(result_string)))
		while min_heap.get_size() != 0:
			lista_ordenada.append(min_heap.pop())

		return lista_ordenada, pattern
	
	def conjunto_letras_corchetes(self, patt):
		print(patt)
		pattern = ""
		letras = []
		i = 0
		for i in range(len(patt)):
			if patt[i] == '[':
				a1 = i
			if patt[i] == ']':
				a2 = i
				break
		pattern = patt[0:a1] + '-' + patt[a2+1:len(patt)+1]
		for i in range(a1+1, a2):
			letras.append(patt[i])
		print(pattern)
		print(letras)
		
		string = self.text
		BMHModificado2 = BMHMatching2()
		BMHModificado2.set_text(string)
		return BMHModificado2.search(pattern, letras), pattern


Objeto = Regex()
Objeto.get_text("asks TODO aked sTODO as")
print(Objeto.ingresar_tipo_de_busqueda())

"""from colorama import Fore
texto_coloreado = f"{Fore.RED}{self.text[matches[0]:len(pattern)+1]}{Fore.RESET}" + self.text[len(pattern): len(self.text)]

		print(texto_coloreado)"""