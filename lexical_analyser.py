#1 a
import re

from symbol_table import SymbolTable


class LexicalError(SyntaxError):
    pass


with open("token.in","r") as token_in:
    fixed_tokens = list(map(lambda c_line: c_line.strip(), token_in.readlines()))
    fixed_tokens.sort(key=lambda token: len(token), reverse=True)
    print(fixed_tokens)


def is_reserved_token(token: str):
    return token in fixed_tokens


def is_string_constant(token: str) -> bool:
    return bool(re.match('^"[0-9a-zA-Z_]*"$', token))
    #return bool(re.match('^"([0-9]|[a-z]|[A-Z]|[_])*"$', token)


def is_numeric_constant(token: str) -> bool:
    return token == "0" or bool(re.match("^-?[1-9][0-9]*$", token))


def is_constant(token: str) -> bool:
    return is_string_constant(token) or is_numeric_constant(token)


def is_symbol(token: str) -> bool:
    return bool(re.match("^[a-zA-Z][a-zA-Z0-9]*$", token))


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
                add_to_pif(program_internal_form, -1)
            elif is_constant(current_token) or is_symbol(current_token):
                add_to_pif(program_internal_form, st.retrieve_position(current_token))
            else:
                raise LexicalError("Lexical error invalid token at line {}: {}".format(line_index, current_token))
            print(current_pos, len(current_token_group))
with open("PIF.out", "w") as pif_file:
    pif_file.write(str(program_internal_form))
with open("ST.out", "w") as st_file:
    st_file.write(str(st))
print("Lexically correct")

