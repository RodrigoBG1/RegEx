class BMHMatching1:
    def __init__(self):
        self.text = ""
        self.ALPHABET_SIZE = 130
        self.table = []

    def set_text(self, text):
        self.text = text

    def __char_to_index(self, char):
        n = ord(char)
        return n

    def __calculate_bad_match_table(self, pattern):
        self.table = [len(pattern)] * self.ALPHABET_SIZE
        for i in range(len(pattern) - 1):
            n = self.__char_to_index(pattern[i])
            self.table[n-1] = len(pattern) - (i + 1)


    def search(self, pattern):
        # Lista para guardar los matches
        matches = []
        self.__calculate_bad_match_table(pattern)
        patt_size = len(pattern)

        text_idx = patt_size - 1

        while text_idx < len(self.text):
            shared_substr = 0
            while shared_substr < patt_size:
                if self.text[text_idx - shared_substr] == pattern[patt_size-1 - shared_substr]:
                    shared_substr += 1
                else:
                    break
            if shared_substr == patt_size:
                matches.append(text_idx+1 - patt_size)
                
            n = self.__char_to_index(self.text[text_idx])
            text_idx += self.table[n-1]
        
        return matches