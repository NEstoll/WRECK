from itertools import product
from GrammarParser import GrammarParser
from sets import *

# Create predict sets.
# a. a function that returns the predict set for one production rule
# b. a function that tests for pairwise disjoint sets within grammar
# non terminals.
def predict_set(prod_rule, prod_rules, nonterminals, terminals):
    LHS = prod_rule[0]
    RHS = prod_rule[1]
    T = set()
    F, I = first_set(RHS, T, prod_rules, nonterminals, terminals)
    T = []
    if derives_to_lambda(LHS, T, prod_rules, nonterminals, terminals):
        G, I = follow_set(LHS, set(), prod_rules, nonterminals, terminals)
        F = F.union(G)
    return F

#def test_disjoint_sets():
    

# hardcodes some predict sets from lecture, 
# used to develop build table
def predict_set_stub(prod_rule):
    if prod_rule == ('S', ['A', 'M', '$']):
        return set(['b', 'm', 'n', 'p', 's'])
    elif prod_rule == ('A', ['B', 'C']):
        return set(['b'])
    elif prod_rule == ('A', ['C', 'M']):
        return set(['m', 'n', 'p', 's'])
    elif prod_rule == ('B', ['b', 'g', 'h']):
        return set(['b'])
    elif prod_rule == ('C', ['s', 't']):
        return set(['s'])
    elif prod_rule == ('C', ['lambda']):
        return set(['m', 'n', 'p'])
    elif prod_rule == ('M', ['m']):
        return set(['m'])
    elif prod_rule == ('M', ['n']):
        return set(['n'])
    elif prod_rule == ('M', ['p']):
        return set(['p'])
    else:
        return None

def build_table(production_rules, nonterminals, terminals):
    LHS = 0
    RHS = 1 
    LLTable = {}
    for A in nonterminals:
        LLTable[A] = {}
        for a in terminals:
            LLTable[A][a] = 0
    for A in nonterminals:
        for i, p in enumerate(production_rules):
            if p[LHS] == A:
                #for a in predict_set_stub(p):
                for a in predict_set(p, production_rules, nonterminals, terminals):
                    LLTable[A][a] = i + 1
    return LLTable

""""""
grammar = GrammarParser('lecture_example.txt').parse_grammar()
production_rules = grammar['production rules']
nonterminals = grammar['nonterminals']
terminals = grammar['terminals']

LLTable = build_table(production_rules, nonterminals, terminals)

"""
# print out as in lecture -- example here: https://ibb.co/xHppdr5
symbol_order = ['S', 'A', 'M', 'B', 'C']
terminals = ['b', 'g', 'h', 'm', 'n', 'p', 's', 't', '$']

print("  " + " ".join(terminals))
for S in symbol_order:
    print(S, end=" ")
    for terminal in terminals:
        print(LLTable[S][terminal], end = " ")
    print("")


grammar = GrammarParser('LGA/predict-set-test0.cfg').parse_grammar()
production_rules = grammar['production rules']
nonterminals = grammar['nonterminals']
terminals = grammar['terminals']

LLTable = build_table(production_rules, nonterminals, terminals)

symbol_order = ['START', 'S', 'C', 'A', 'B', 'Q']
terminals = ['a', 'b', 'c', 'd', 'q', '$']

print("  " + " ".join(terminals))
for S in symbol_order:
    print(S, end=" ")
    for terminal in terminals:
        print(LLTable[S][terminal], end = " ")
    print("")

grammar = GrammarParser('LGA/predict-set-test1.cfg').parse_grammar()
production_rules = grammar['production rules']
nonterminals = grammar['nonterminals']
terminals = grammar['terminals']

LLTable = build_table(production_rules, nonterminals, terminals)

symbol_order = ['S', 'A', 'B', 'C', 'E', 'F', 'G', 'H']
terminals = ['b', 'c', 'e', 'g', 'h', 'z', '$']

print("  " + " ".join(terminals))
for S in symbol_order:
    print(S, end=" ")
    for terminal in terminals:
        print(LLTable[S][terminal], end = " ")
    print("")
"""

