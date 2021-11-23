from collections import defaultdict

class GrammarException(Exception):
    pass

class Grammar:
    def __init__(self):
        self.starting_symbol = None
        self.non_terminals = []
        self.terminals = []
        self.productions = defaultdict(list)
        self.is_cfg = True

    def get_starting_symbol(self):
        return self.starting_symbol

    def get_non_terminals(self):
        return self.non_terminals

    def get_terminals(self):
        return self.terminals

    def get_productions(self):
        return self.productions

    def get_is_cfg(self):
        return self.is_cfg

    def read_grammar(self, file_name):
        f = open(file_name, "r")

        def current_line():
            return f.readline().strip()

        self.starting_symbol = current_line()
        self.terminals = current_line().split(',')
        self.non_terminals = current_line().split(',')
        if self.starting_symbol not in self.non_terminals:
            raise GrammarException("Starting symbol not in nonterminals")
        for raw_line in f.readlines():
            line = raw_line.strip()
            symbol_groups = line.split('->')
            if len(symbol_groups) != 2:
                raise GrammarException("Invalid production rule")
            left_side, right_side = symbol_groups
            left_symbols = left_side.strip().split(' ')
            if len(left_symbols) > 1:
                self.is_cfg = False
                production_left = tuple(left_symbols)
            else:
                production_left = left_symbols[0]
            right_symbols = right_side.strip().split(' ')
            self.productions[production_left].append(right_symbols)


grammar = Grammar()
commands = {
    "read": grammar.read_grammar,
    "terminals": grammar.get_terminals,
    "non terminals": grammar.get_non_terminals,
    "productions": grammar.get_productions,
    "starting symbol": grammar.get_starting_symbol,
    "is cfg": grammar.get_is_cfg,
}
#grammar.read_grammar("g1.txt")
commands["read"]("g1.txt")
current_command = ""
while current_command != "exit":
    current_command = input("Current command\n")
    if current_command in commands:
        if current_command == "read":
            commands[current_command](input("File\n"))
        else:
            print(commands[current_command]())


