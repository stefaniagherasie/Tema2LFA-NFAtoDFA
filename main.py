import sys


class NFA:

    def __init__(self):
        self.num_states = 0
        self.final_states = []
        self.states = []
        self.symbols = []
        self.start_state = 0
        self.transitions = {}

    # Functie recursiva care construieste in visited inchiderea cu epsilon
    # a fiecarei stari din NFA, pornind de la encodarile directe ale acestora
    def compute_eps_helper(self, direct_enc, state, visited):
        visited.append(state)
        for next_state in direct_enc[state]:
            if next_state not in visited:
                self.compute_eps_helper(direct_enc, next_state, visited)
        return

    # Functie care construieste inchiderea fiecarei stari din NFA
    def compute_eps_closure(self):
        # direct_enc contine starile accesibile printr-o singura tranzitie epsilon
        # complet_enc contine inchiderea cu epsilon a fiecarei stari
        direct_enc = {}
        complet_enc = {}
        for state in range(0, self.num_states):
            direct_enc[state] = []
            complet_enc[state] = []

        # Pentru fiecare stare se calculeaza direct_enc
        for state in self.states:
            direct_enc[state] = []
            transition = self.transitions[state]
            for i in range(0, len(transition)):
                if transition[i][0] == 'eps':
                    direct_enc[state] = transition[i][1]

        # Nu mai este nevoie de tranzitia 'eps' si pentru a ne ajuta mai
        # departe o sterg de acum din symbols
        if 'eps' in self.symbols:
            self.symbols.remove('eps')

        # Se calculeaza inchiderea cu epsilon pentru fiecare stare,
        # folosind vectorul visited si helper-ul
        for state in self.states:
            visited = []
            self.compute_eps_helper(direct_enc, state, visited)
            visited.sort()
            complet_enc[state] = visited

        return complet_enc

    # Construieste NFA-ul, citind informatiile din fisierul de intrare
    def compute_nfa_from_file(self):
        input_file = open(str(sys.argv[1]), "r")

        # Se obtine numarul de stari sin starile finale
        self.num_states = int(input_file.readline())
        self.final_states = [int(x) for x in input_file.readline().split()]
        for state in range(0, self.num_states):
            self.transitions[state] = []
            self.states.append(state)

        # Se citesc, pe rand, toate tranzitiile
        while True:
            line = input_file.readline().strip()
            if line == '':
                break
            line = line.split()

            # Se obtine starea de pornire si simbolul
            start_state = int(line[0])
            symbol = str(line[1])
            if symbol not in self.symbols:
                self.symbols.append(symbol)

            # Se obtin starile rezultat si se adauga toate tranzitiile obtinute
            end_states = [int(x) for x in line[2:]]
            transition = (symbol, end_states)
            self.transitions[start_state].append(transition)

        input_file.close()
        return


class DFA:

    def __init__(self):
        self.num_states = 0
        self.final_states = []
        self.dfa_transitions = []
        self.dfa_states = []

    # Obtine starile urmatoare corespunzatoare unei liste de stari,
    # folosind trazitiile de pe un anumit simbol
    def get_next_dfa_states(self, symbol, states, transitions):
        # Am folosit set() pentru a evita dublicatele
        next_dfa_states = set()

        for state in states:
            for transition in transitions[state]:
                if transition[0] == symbol:
                    next_states = transition[1]
                    next_dfa_states.update(next_states)
        next_dfa_states = list(next_dfa_states)
        return next_dfa_states

    # Obtine tranzitiile din DFA, in acelasi timp construind starile DFA-ului
    def compute_dfa_transitions(self, nfa):
        # Se obtin valorile inchiderilor cu epsilon din NFA
        epsilon = nfa.compute_eps_closure()

        # Pentru fiecare stare din DFA se considera epsilon(stare) ca stari succesor
        # Consideram 0 starea initiala, epsilon(0) fiind prima stare din DFA
        self.dfa_states.append(epsilon[0])

        # Se parcurg toate starile din DFA
        for dfa_state in self.dfa_states:
            # Pentru fiecare simbol se afla starea urmatoare
            for symbol in nfa.symbols:
                # Se obtin ca lista starile urmatoare
                next_states = self.get_next_dfa_states(symbol, dfa_state, nfa.transitions)

                # Se concateneaza si epsilon de fiecare stare
                for next_st in next_states:
                    next_states = next_states + epsilon[next_st]
                # Pentru a evita dublicatele
                next_states = list(set(next_states))

                # Se adauga tranzitia sub forma de tuplu (stare1, simbol, stare2)
                new_transition = (dfa_state, symbol, next_states)
                self.dfa_transitions.append(new_transition)

                # Se adauga starea obtinuta in lista de stari din DFA
                # daca nu a fost intalnita deja
                if next_states not in self.dfa_states:
                    self.dfa_states.append(next_states)
        return

    # Obtine starile finale din DFA, adica starile care contin o stare finala a NFA-ului
    def compute_dfa_final_states(self, nfa):
        for dfa_state in self.dfa_states:
            for final_state in nfa.final_states:
                if final_state in dfa_state:
                    self.final_states.append(dfa_state)
        return

    def write_dfa_in_file(self):
        # Se deschide fisierul de iesire
        output_file = open(str(sys.argv[2]), "w")

        # Se scrie numarul de stari din DFA
        output_file.write(str(self.num_states))
        output_file.write('\n')

        # Se scriu starile finale cu noua notatie
        # Starile primesc ca nou nume indexul lor din self.dfa_states
        code = self.dfa_states.index(self.final_states[0])
        output_file.write(str(code))
        for final_state in self.final_states[1:]:
            code = self.dfa_states.index(final_state)
            output_file.write(" " + str(code))
        output_file.write('\n')

        # Se scriu tranzitiile in fisier
        for trans in self.dfa_transitions:
            code1 = self.dfa_states.index(trans[0])
            code2 = self.dfa_states.index(trans[2])
            transition = str(code1) + " " + trans[1] + " " + str(code2) + '\n'
            output_file.write(transition)

        output_file.close()
        return

    # Obtine specificatiile DFA-ului si il construieste
    def compute_dfa(self, nfa):
        self.compute_dfa_transitions(nfa)
        self.compute_dfa_final_states(nfa)
        self.num_states = len(dfa.dfa_states)
        self.write_dfa_in_file()


if __name__ == '__main__':
    # Construim NFA-ul prin citirea din fisier
    nfa = NFA()
    nfa.compute_nfa_from_file()

    # Construim DFA-ul pe baza NFA-ului primit
    dfa = DFA()
    dfa.compute_dfa(nfa)
