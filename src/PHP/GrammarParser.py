class GrammarParser():

    def __init__(self, input_grammar_file):
        self.PIPECHAR = "|"
        self.PRODCHAR = "->"
        self.ENDCHAR = "$"
        with open(input_grammar_file) as f:
            self.contents = [line.split() for line in f]

    def parse_grammar(self):
        nonterminals = set()
        all_symbols = set()
        start_symbol = None
        production_rules = []
        prev_symbol = None

        def is_nonterminal(symbol):
            return any(ele.isupper() for ele in symbol)

        for line in self.contents:
            if all(l.isspace() for l in line):
                continue
            if line[0] != self.PIPECHAR:
                if line[1] != self.PRODCHAR:
                    raise ValueError("Need prod symbol")
                elif not is_nonterminal(line[0]):
                    print(line)
                    raise ValueError("LHS must be nonterminal")
                else:
                    nonterminals.add(line[0])
                    all_symbols.add(line[0])
                    prev_symbol = line[0]
                    if line[-1] == self.ENDCHAR:
                        start_symbol = line[0]
                    possibilities = ' '.join(line[2:]).split(self.PIPECHAR)
                    for possibility in possibilities:
                        production_rules.append((line[0], possibility.split()))
                    for symbol in line[2:]:
                        if is_nonterminal(symbol):
                            nonterminals.add(symbol)
                    all_symbols.update(line[2:])
            else:
                if prev_symbol is None:
                    raise ValueError("Pipe op must follow symbol")
                else:
                    possibilities = ' '.join(line[1:]).split(self.PIPECHAR)
                    for possibility in possibilities:
                        production_rules.append((prev_symbol, possibility.split()))
                    all_symbols.update(line[1:])

        terminals = all_symbols.difference(nonterminals)
        terminals.remove('lambda')

        rules = []
        for i, prod_rule in enumerate(production_rules):
            LHS = prod_rule[0]
            RHS = prod_rule[1]
            rules.append('('+str(i+1)+')'+ ' ' + LHS + ' ' + self.PRODCHAR + ' ' + " ".join(RHS))

        return ({"start symbol": start_symbol,
                  "nonterminals": nonterminals,
                  "terminals": terminals,
                  "all symbols": all_symbols,
                  "production rules": production_rules,
                  "string rules": rules,
                  })