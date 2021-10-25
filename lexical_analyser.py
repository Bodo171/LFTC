#1 a
import re

from symbol_table import SymbolTable


class LexicalError(SyntaxError):
    pass


with open("token.in","r") as token_in:
    fixed_tokens = token_in.readlines()
    fixed_tokens.sort(key=lambda token: len(token), reverse=True)


def is_reserved_token(token: str):
    return token in fixed_tokens


def is_string_constant(token: str) -> bool:
    return bool(re.match("'([0-9]|[a-z][A-Z]_)*'", token))


def is_numeric_constant(token: str) -> bool:
    return token == "0" or bool(re.match("-?[1-9][0-9]*", token))


def is_constant(token: str) -> bool:
    return is_string_constant(token) or is_numeric_constant(token)


def is_symbol(token: str) -> bool:
    return bool(re.match("([a-z]|[A-Z])([a-z][A-Z][0-9])*", token))


def detect(token_group: str) -> str:
    detected_len = 0
    while is_constant(token_group[:detected_len]) or is_symbol(token_group[:detected_len]):
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


f = open("program.txt", "r")
st = SymbolTable()
program_internal_form = []
lines = f.readlines()
for line_index, raw_line in enumerate(lines):
    line = raw_line.strip()
    for current_token_group in line.split():
        current_pos = 0
        while current_pos < len(current_token_group):
            current_token = detect(current_token_group[current_pos:])
            current_pos += len(current_token)
            if is_reserved_token(current_token):
                add_to_pif(program_internal_form, -1)
            elif is_constant(current_token) or is_symbol(current_token):
                add_to_pif(program_internal_form, st.retrieve_position(current_token))
            else:
                raise LexicalError("Lexical error invalid token at line {}".format(line_index))



