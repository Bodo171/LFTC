#1 a
import re
import json

from symbol_table import SymbolTable
from finite_automata import FiniteAutomaton

class LexicalError(SyntaxError):
    pass


identifier_automaton = FiniteAutomaton("identifier.in")
numeric_constant_automaton = FiniteAutomaton("numeric_constant.in")
string_constant_automaton = FiniteAutomaton("string_constant.in")


with open("token.in","r") as token_in:
    fixed_tokens = list(map(lambda c_line: c_line.strip(), token_in.readlines()))
    fixed_tokens.sort(key=lambda token: len(token), reverse=True)
    print(fixed_tokens)


def is_reserved_token(token: str):
    return token in fixed_tokens


def is_string_constant(token: str) -> bool:
    return string_constant_automaton.accept(token)


def is_numeric_constant(token: str) -> bool:
    return numeric_constant_automaton.accept(token)


def is_constant(token: str) -> bool:
    return is_string_constant(token) or is_numeric_constant(token)


def is_symbol(token: str) -> bool:
    return identifier_automaton.accept(token)


def detect(token_group: str) -> str:
    detected_len = 1
    if token_group[0] == '"':
        while detected_len < len(token_group) and token_group[detected_len] != '"':
            detected_len += 1
        return token_group[:detected_len + 1]
    while (is_constant(token_group[:detected_len]) or is_symbol(token_group[:detected_len]))\
            and detected_len <= len(token_group):
        detected_len += 1
    detected_len -= 1
    # some keywords are matched as symbols but does not matter at this step
    if detected_len:
        return token_group[:detected_len]
    for token in fixed_tokens:
        if token_group[:len(token)] == token:
            return token
    return token_group


def add_to_pif(pif, row):
    pif.append(row)

print(is_numeric_constant("1000"))
print(numeric_constant_automaton.transition_representation())
f = open("program.txt", "r", encoding="utf8")
st = SymbolTable()
program_internal_form = []
lines = f.readlines()
for line_index, raw_line in enumerate(lines):
    line = raw_line.strip()
    for current_token_group in line.split():
        current_pos = 0
        while current_pos < len(current_token_group):
            current_token = detect(current_token_group[current_pos:])
            print("Current token",current_token, len(current_token))
            current_pos += len(current_token)
            if is_reserved_token(current_token):
                add_to_pif(program_internal_form, (current_token, -1))
            elif is_constant(current_token) or is_symbol(current_token):
                add_to_pif(program_internal_form, (current_token, st.retrieve_position(current_token)))
            else:
                raise LexicalError("Lexical error invalid token at line {}: {}".format(line_index, current_token))
            print(current_pos, len(current_token_group))
with open("PIF.out", "w") as pif_file:
    pif_file.write(json.dumps(program_internal_form, indent=2))
with open("ST.out", "w") as st_file:
    st_file.write(str(st))
print("Lexically correct")

