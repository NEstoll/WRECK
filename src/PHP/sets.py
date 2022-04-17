from GrammarParser import GrammarParser

LAMBDA = 'lambda'

def derives_to_lambda(L, T, prod_rules, nonterminals, terminals):
    for p in prod_rules:
        if p[0] == L:
            if p in T:
                continue
            if p[1] == LAMBDA or p[1] == [LAMBDA]:
                return True
            terminal_symbol = False
            for symbol in p[1]:
                if symbol in terminals:
                    terminal_symbol = True
            if terminal_symbol:
                continue      
            all_derive_lambda = False
            for symbol in p[1]:
                T.append(p)
                all_derive_lambda = derives_to_lambda(symbol, T, prod_rules, nonterminals, terminals)
                T.pop()
                if not all_derive_lambda:
                    return False
            
            if all_derive_lambda:
                return True
    
    return False
    
def first_set(sequence, T, prod_rules, nonterminals, terminals):
    if isinstance(sequence, list):
        X = sequence[0]
    else:
        X = sequence

    if X in terminals:
        return (set([X]), T)
    
    F = set()
    if X not in T:
        T.add(X)
        for p in prod_rules:
            if p[0] == X:
                G, I = first_set(p[1], T, prod_rules, nonterminals, terminals)
                F = F.union(G)
        
    if derives_to_lambda(X, [], prod_rules, nonterminals, terminals) and len(sequence[1:]) > 0:
        G, I = first_set(sequence[1:], T, prod_rules, nonterminals, terminals)
        F = F.union(G)
    
    return F, T

def follow_set(A, T, prod_rules, nonterminals, terminals):
    if A in T:
        return (set(), T)
    
    T.add(A)
    F = set()
    for p in prod_rules:
        for i, r in enumerate(p[1]):
            if r == A:
                pi = p[1][(i+1):]
                if len(pi) > 0:
                    G, I = first_set(pi, set(), prod_rules, nonterminals, terminals)
                    F = F.union(G)
                alltolambda = True
                for symbol in pi:
                    if not derives_to_lambda(symbol, [], prod_rules, nonterminals, terminals):
                        alltolambda = False
                        break
                if (len(pi) == 0  or (set(pi).isdisjoint(terminals) and alltolambda)):
                    G, I = follow_set(p[0], T, prod_rules, nonterminals, terminals)
                    F = F.union(G)

    return F, T

"""
grammar = GrammarParser('Zoe_example.txt').parse_grammar()
productionRules = grammar['production rules']
nonterminals = grammar['nonterminals']
terminals = grammar['terminals']


for nonterminal in nonterminals:
    print(first_set([nonterminal], set(), productionRules, nonterminals, terminals)[0])
    print("First set for nonterminal", nonterminal)
    print("--------------------------------------")


for nonterminal in nonterminals:
    print("Follow set for nonterminal", nonterminal)
    print(follow_set(nonterminal, set(), productionRules, nonterminals, terminals)[0])
    print("--------------------------------------")
"""