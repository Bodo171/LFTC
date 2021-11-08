import json


class AutomatonError(Exception):
    pass


class FiniteAutomaton:
    def __init__(self):
        self._states = set()
        self._alphabet = set()
        self._initial_state = None
        self._final_states = set()
        self._transitions = {}

    def add_state(self, state):
        if state in self._states:
            raise AutomatonError("State already exists")
        self._states.add(state)
        self._transitions[state] = {}

    def add_to_alphabet(self, character):
        self._alphabet.add(character)

    def add_transition(self, first_state: str, second_state: str, transition: str):
        if len({first_state, second_state} and self._states) < 2:
            raise AutomatonError("Invalid state")
        self._transitions[first_state][transition] = second_state

    def add_final_state(self, state):
        if state not in self._states:
            raise AutomatonError("State does not exists")
        if state in self._final_states:
            raise AutomatonError("State is already final")
        self._final_states.add(state)

    def set_initial_state(self, state):
        if state not in self._states:
            raise AutomatonError("State does not exists")
        self._initial_state = state

    def accept(self, string):
        current_state = self._initial_state
        for character in string:
            if character not in self._transitions[current_state]:
                return False
            current_state = self._transitions[current_state][character]
        return current_state in self._final_states

    def load_from_file(self, file_name: str):
        try:
            with open(file_name, "r") as f:
                representation = json.load(f)
                for letter in representation["alphabet"]:
                    self.add_to_alphabet(letter)
                for state in representation["states"]:
                    self.add_state(state)
                self.set_initial_state(representation["initialState"])
                for state in representation["finalStates"]:
                    self.add_final_state(state)
                transitions = representation["transitions"]
                for transition in transitions:
                    for letter in transition[2]:
                        self.add_transition(transition[0], transition[1], letter)
        except Exception as e:
            raise AutomatonError("Invalid file format" + str(e))

    def transition_representation(self):
        acc = ""
        for state_from, transitions in self._transitions.items():
            for transition_char, state_to in transitions.items():
                acc += "{}-'{}'->{}\n".format(state_from, transition_char, state_to)
        return acc

    def get_attribute(self, attribute: str):
        if attribute == "transitions":
            return self.transition_representation()
        return getattr(self, "_"+attribute)


my_automaton = FiniteAutomaton()
my_automaton.load_from_file("FA.in")
print(my_automaton.accept("aBc5"))
print(my_automaton.accept("5aBc5"))
menu = {
    "1": "states",
    "2": "initial_state",
    "3": "final_states",
    "4": "alphabet",
    "5": "transitions",
}
for key, value in menu.items():
    print("{}. Display {}".format(key, value))
command = ""
while command != "x":
    command = input()
    if command in menu:
        print(my_automaton.get_attribute(menu[command]))
