class BMHMatching:
    def __init__(self):
        self.text = ""
        self.ALPHABET_SIZE = 130
        self.table = []

    def set_text(self, text):
        self.text = text

    def __char_to_index(self, char):
        n = ord(char)
        return n

    def __calculate_bad_match_table(self, idx, p1, p2, pattern):
        self.table = [len(pattern)] * self.ALPHABET_SIZE
        for i in range(p1, (p2+1)):
            self.table[i-1] = idx

        for i in range(len(pattern) - 1):
                if pattern[i] == '-':
                    continue
                else:
                    n = self.__char_to_index(pattern[i])
                    if len(pattern) - (i + 1) < self.table[n-1]:
                        self.table[n-1] = len(pattern) - (i + 1)
                    else:
                        continue
        #for i in range(self.ALPHABET_SIZE):
            #print(i + 1, ":", self.table[i])

    def search(self, idx, p1, p2, pattern):
        # Lista para guardar los matches
        matches = []
        self.__calculate_bad_match_table(idx, p1, p2, pattern)
        patt_size = len(pattern)

        text_idx = patt_size - 1

        while text_idx < len(self.text):
            shared_substr = 0
            while shared_substr < patt_size:
                if self.text[text_idx - shared_substr] == pattern[patt_size-1 - shared_substr]:
                    shared_substr += 1
                elif pattern[patt_size-1 - shared_substr] == '-':
                    if type(self.text[text_idx - shared_substr]) is int:
                        n = self.text[text_idx - shared_substr]
                    else:
                        n = self.__char_to_index(self.text[text_idx - shared_substr])
                    if n >= p1 and n <= p2:
                       shared_substr += 1
                    else:
                        break 
                else:
                    break
            if shared_substr == patt_size:
                matches.append(text_idx+1 - patt_size)
                
            n = self.__char_to_index(self.text[text_idx])
            text_idx += self.table[n-1]
            
        return matches