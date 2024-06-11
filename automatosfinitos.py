from graphviz import Digraph
from IPython.display import display
from collections import deque

class FiniteAutomata:
    """
    Represents a DFA for pattern searching.
    Source: Modification of code provided in https://www.geeksforgeeks.org/pattern-searching-set-5-efficient-constructtion-of-finite-automata/
    
    This class provides functionality for constructing a DFA transition function table
    from a given pattern and searching for patterns in text using the constructed DFA.
    """
    def __init__(self):
        """
        Initializes a FiniteAutomata object.
        """
        self.NO_OF_CHARS = 256
        self.Q = set()
        self.sigma = set()
        self.q_0 = 0
        self.F = set()
        self.delta = {}
        self.TF = []

    def compute_transition_func(self, pat):
        """
        Constructs the transition function table for a given pattern.

        Args:
            pat (str): The pattern string.
        """
        if not pat:
            raise ValueError("Pattern cannot be empty.")

        M = len(pat)
        self.TF = [[0 for _ in range(self.NO_OF_CHARS)] for _ in range(M + 1)]
        lps = 0  # Longest Prefix Suffix

        # Initialize the first row of the TF table
        for x in range(self.NO_OF_CHARS):
            self.TF[0][x] = 0
        self.TF[0][ord(pat[0])] = 1

        # Fill the entries in the rest of the TF table
        for i in range(1, M + 1):
            # Copy the values from the row at index lps
            for x in range(self.NO_OF_CHARS):
                self.TF[i][x] = self.TF[lps][x]

            if i < M:
                # Update the entry corresponding to the current character
                self.TF[i][ord(pat[i])] = i + 1

                # Update lps for the next row to be filled
                lps = self.TF[lps][ord(pat[i])]

        # Update the DFA components
        self.Q = {i for i in range(M + 1)}
        self.sigma = {pat[i] for i in range(M)}
        self.q_0 = 0
        self.F = {M}
        self.delta = {(i, chr(x)): self.TF[i][x] for i in range(M + 1) for x in range(self.NO_OF_CHARS) if
                      self.TF[i][x] != 0}

    def search(self, patterns, txt, preprocessing=True):
        """
        Searches for multiple patterns in a provided text.

        Args:
            patterns (list of str): The list of pattern strings.
            txt (str): The text string to search within.
            preprocessing (bool, optional): Whether to preprocess the text and patterns. Default is True.

        Returns:
            dict: A dictionary where keys are patterns and values are lists of starting indices
            where the pattern was found in the text.
        """
        if not patterns:
            raise ValueError("Patterns list cannot be empty.")

        if not txt:
            raise ValueError("Text string cannot be empty.")

        if preprocessing:
            txt = self.preprocess_text(txt)
            patterns = [self.preprocess_text(pat) for pat in patterns]

        results = {pat: [] for pat in patterns}

        for pat in patterns:
            M = len(pat)
            N = len(txt)
            self.compute_transition_func(pat)

            # Process text using the FA
            j = self.q_0  # State of the FA

            for i in range(N):
                j = self.TF[j][ord(txt[i])]
                if j == M:
                    results[pat].append(i - M + 1)

        return results

    def reset(self):
        """
        Resets the transition function table.
        """
        self.TF = []
        self.Q = set()
        self.sigma = set()
        self.q_0 = 0
        self.F = set()
        self.delta = {}
        print("Transition function table successfully reset!")

    def preprocess_text(self, txt):
        """
        Preprocesses the text for case insensitivity or other cleaning.

        Args:
            txt (str): The text string to preprocess.

        Returns:
            str: The preprocessed text.
        """
        if not txt:
            raise ValueError("Text string cannot be empty.")

        return txt.lower()  # Example for case insensitivity

    def set_alphabet_size(self, size):
        """
        Sets a custom alphabet size.
        
        Args:
            size (int): The number of characters in the alphabet.
        """
        self.NO_OF_CHARS = size
        self.reset()  # Reset the transition function table to apply the new size

    def print_transition_func(self):
        """
        Prints the transition function table for debugging.
        """
        for row in self.TF:
            print(row)

    def print_dfa(self):
        """
        Prints the DFA components.
        """
        print("States (Q):", self.Q)
        print("Alphabet (Sigma):", self.sigma)
        print("Initial state (q_0):", self.q_0)
        print("Accepting states (F):", self.F)
        print("Transition function (Delta):")
        for key in sorted(self.delta):
            print(f"  Delta{key} -> {self.delta[key]}")

    def visualize_dfa(self, filename=None):
        """
        Visualizes the DFA states and transitions using Graphviz.
        
        Args:
            filename (str, optional): The filename to save the .png file. 
            If None, the visualization is only displayed in the notebook. Default is None.
        """
        dot = Digraph()
        
        for state in self.Q:
            if state in self.F:
                dot.node(str(state), shape='doublecircle')
            else:
                dot.node(str(state))

        for (source, char), target in self.delta.items():
            dot.edge(str(source), str(target), label=char)

        if filename:
            dot.render(filename, format='png', cleanup=True)
        else:
            display(dot)

class DFA:
    """
    Represents a Deterministic Finite Automaton (DFA).
    """

    def __init__(self, states, alphabet, transition, initial_state, accepting_states):
        """
        Initializes the DFA.

        Args:
            states (set): Set of states in the DFA.
            alphabet (set): Alphabet of the DFA.
            transition (dict): Transition function of the DFA.
            initial_state (str): Initial state of the DFA.
            accepting_states (set): Set of accepting states in the DFA.

        Raises:
            ValueError: If any of the input parameters are invalid or missing.
        """
        if not isinstance(states, set):
            raise ValueError("States must be a set.")
        if not isinstance(alphabet, set):
            raise ValueError("Alphabet must be a set.")
        if not isinstance(transition, dict):
            raise ValueError("Transition function must be a dictionary.")
        if not isinstance(initial_state, str):
            raise ValueError("Initial state must be a string.")
        if not isinstance(accepting_states, set):
            raise ValueError("Accepting states must be a set.")

        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.initial_state = initial_state
        self.accepting_states = accepting_states

class NFA:
    """
    Represents a Non-Deterministic Finite Automaton (NFA).
    """
    
    def __init__(self, states, alphabet, transition, initial_state, accepting_states):
        """
        Initializes the NFA.

        Args:
            states (set): Set of states in the NFA.
            alphabet (set): Alphabet of the NFA.
            transition (dict): Transition function of the NFA.
            initial_state (str): Initial state of the NFA.
            accepting_states (set): Set of accepting states in the NFA.
        """
        if not isinstance(states, set):
            raise ValueError("States must be a set.")
        if not isinstance(alphabet, set):
            raise ValueError("Alphabet must be a set.")
        if not isinstance(transition, dict):
            raise ValueError("Transition function must be a dictionary.")
        if not isinstance(initial_state, str):
            raise ValueError("Initial state must be a string.")
        if not isinstance(accepting_states, set):
            raise ValueError("Accepting states must be a set.")

        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def epsilon_closure(self, states):
        """
        Computes the epsilon closure of a set of states.

        Args:
            states (set): Set of states.

        Returns:
            set: Epsilon closure of the input set of states.
        """
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.transition and '' in self.transition[state]:
                epsilon_states = self.transition[state]['']
                for epsilon_state in epsilon_states:
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)
        return closure

    def move(self, states, symbol):
        """
        Computes the set of states reachable from a set of states by consuming a symbol.

        Args:
            states (set): Set of states.
            symbol (str): Input symbol.

        Returns:
            set: Set of states reachable from the input set of states by consuming the input symbol.
        """
        reachable_states = set()
        for state in states:
            if state in self.transition and symbol in self.transition[state]:
                reachable_states.update(self.transition[state][symbol])
        return reachable_states

    def simulate(self, input_string):
        """
        Simulates the NFA on an input string.

        Args:
            input_string (str): Input string.

        Returns:
            bool: True if the input string is accepted by the NFA, False otherwise.
        """
        current_states = self.epsilon_closure({self.initial_state})
        for symbol in input_string:
            current_states = self.epsilon_closure(self.move(current_states, symbol))
        return any(state in self.accepting_states for state in current_states)
    
    def visualize_nfa_transitions(self, filename=None):
        """
        Visualizes the NFA transitions using Graphviz.
    
        Args:
            filename (str, optional): The filename to save the .png file. 
            If None, the visualization is only displayed in the notebook. Default is None.
        """
        dot = Digraph()
    
        for state in self.states:
            if state in self.accepting_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        for source, transitions in self.transition.items():
            for symbol, target_states in transitions.items():
                for target_state in target_states:
                    dot.edge(source, target_state, label=symbol)

        if filename:
            dot.render(filename, format='png', cleanup=True)
        else:
            display(dot)


    def to_dfa(self):
        """
        Converts the NFA to a DFA using the subset construction algorithm.

        Returns:
            DFA: Deterministic Finite Automaton representing the equivalent DFA of the NFA.
        """
        dfa_states = set()  # Set of DFA states
        dfa_transition = {}  # Transition function of DFA
        dfa_initial_state = frozenset(self.epsilon_closure({self.initial_state}))  # Initial state of DFA
        dfa_accepting_states = set()  # Set of accepting states in DFA

        # Queue for processing states
        queue = deque([dfa_initial_state])
        processed_states = set()  # Set to keep track of processed states

        while queue:
            current_dfa_state = queue.popleft()
            dfa_states.add(current_dfa_state)
            processed_states.add(current_dfa_state)

            for symbol in self.alphabet:
                next_nfa_states = set()
                for nfa_state in current_dfa_state:
                    next_nfa_states |= self.move(nfa_state, symbol)
                next_dfa_state = frozenset(self.epsilon_closure(next_nfa_states))

                if next_dfa_state not in dfa_states:
                    queue.append(next_dfa_state)

                if current_dfa_state not in dfa_transition:
                    dfa_transition[current_dfa_state] = {}
                dfa_transition[current_dfa_state][symbol] = next_dfa_state

        # Determine accepting states in DFA
        for state in dfa_states:
            if any(nfa_state in self.accepting_states for nfa_state in state):
                dfa_accepting_states.add(state)

        return DFA(dfa_states, self.alphabet, dfa_transition, dfa_initial_state, dfa_accepting_states)