# Tema2LFA-NFAtoDFA
[Tema2 Limbaje Formale si Automate (2020-2021, seria CB)] 

Tema a presupun construirea unui program care converteste un NFA intr-un DFA folosind algoritmul de Subset Construction.

#### RULARE
      
> ``` shell
>     python3 main.py <input−file> <output−file>
> ```
> **Fisierul de input** descrie DFA-ul, iar **fisierul de output** contine descrierea NFA-ului rezultat 
din aplicarea algoritmului de Subset Construction.
>
> Formatul fisierelor este urmatorul:
>    - pe prima linie, un intreg ce reprezinta numarul de stari (stare initiala 0)
>    - pe a doua linie, lista de stari finale, separate de cate un spatiu
>    - pe urmatoarele linii, pana la sfarsitul inputului, cate o tranzitie, 
      constand intr-o stare, un simbol, apoi o lista de stari urmatoare

#### IMPLEMENTARE
Am inceput prin citirea datelor de intrare si constructia NFA-ului in `compute_nfa`.
Tranzitiile au fost salvate sub forma unui dictionar in care cheia era starea de
la care pornea tranzitia si elementele erau tupluri de forma `(simbol, stari urmatoare)`.

Apoi a trebuit sa calculez functia de inchidere cu epsilon in `compute_eps_closure`.
Am pornit prin a retine in `direct_enc` inchiderea doar printr-o singura tranzitie
epsilon, urmand apoi ca cu ajutorul lui `compute_eps_helper` sa aflu recursiv
`complete_enc`, adica inchiderea completa a fiecarei stari in raport cu epsilon.
`compute_eps_helper` functioneaza ca un DFS pentru grafuri, tinand in vectorul
visited inchiderea pt fiecare stare.

Pentru a construi DFA-ul, aveam nevoie sa construiesc starile din DFA si tranzitiile
dintre acestea. `compute_dfa_transitions` porneste de la epsilon(0) si descopera
pe rand fiecare stare din DFA, acestea obtinandu-se tinand cont de starile succesor
si inchiderile lor cu epsilon. Tranzitiile se salveaza sub forma de tublu
(ex: pt '123' => a => '03' se salveaza ([1,2,3], 'a', [0, 3]).

Dupa ce s-au obtinut starile si tranzitiilem prin `compute_dfa_final_states` se
afla starile finale din DFA, adica starile care contin in denumirea lor stari finale
din NFA.

Pentru o afisare mai usor de citit se redenumesc starile cand sunt scrise in
fisirul de iesire. Astfel acestea sunt afisate cu indexul pe care il au in
lista de stari `dfa_states` (ex: daca [1, 2, 3] are indexul 3 in dfa_states
starea se transforma in 3). Se procedeaza asa la afisarea starilor finale si
a tranzitiilor.

Functia `compute_dfa` apeleaza toate functiile de mai sus pornind de la NFA-ul
dat si construieste si afiseaza DFA-ul.
