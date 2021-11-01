class SymbolTable:
    def __init__(self, modulo=10**5 + 7):
        self.mod = modulo
        self._hash_table = [[] for _ in range(modulo)]

    @staticmethod
    def get_val(symbol_str: str) -> int:
        return sum(ord(c) for c in symbol_str)

    def get_hash_function(self, symbol_str: str) -> int:
        return self.get_val(symbol_str) % self.mod

    def retrieve_position(self, symbol_str: [str, int]) -> tuple:
        if type(symbol_str) == int:
            symbol_str = str(symbol_str)
        hash_position = self.get_hash_function(symbol_str)
        for index, other_symbol in enumerate(self._hash_table[hash_position]):
            if other_symbol == symbol_str:
                return hash_position, index
        self._hash_table[hash_position].append(symbol_str)
        return hash_position, len(self._hash_table[hash_position]) - 1

    def __str__(self):
        acc = ""
        for hash_key in range(self.mod):
            if self._hash_table[hash_key]:
                acc += "Hash key {}: ".format(hash_key)
                acc += " ".join(self._hash_table[hash_key])
                acc += "\n"
        return acc

"""
print("Small table")
st = SymbolTable(2)
for symbol in ['aa', 'b123', 'x1'] * 2:
    print(st.retrieve_position(symbol))

print("Large table")
large_st = SymbolTable()
for symbol in ['aaa', 'b123', 'x1'] * 3:
    print(large_st.retrieve_position(symbol))


print("Constant table")
large_st = SymbolTable()
for symbol in ['127', '128', 139] * 2:
    print(large_st.retrieve_position(symbol))
"""
