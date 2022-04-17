import unittest
from sets import derives_to_lambda, first_set, follow_set

class TestFirstFollowLambda(unittest.TestCase):
    def test_lambda_directly_derives_to_lambda(self):
        prod_rules = [('A', 'lambda')]
        nonterminals = set(['A'])
        terminals = set()

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertTrue(output)

        prod_rules = [('A', 'lambda'), 
                      ('A', 'B'), 
                      ('B', 'b')]
        nonterminals = set(['A', 'B'])
        terminals = set(['b'])

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertTrue(output)

    def test_lambda_derives_to_terminal(self):
        prod_rules = [('A', 'a')]
        nonterminals = set(['A'])
        terminals = set(['a'])

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertFalse(output)

        prod_rules = [('A', 'B'), 
                      ('B', 'C'),
                      ('C', 'c')]
        nonterminals = set(['A', 'B', 'C'])
        terminals = set(['c'])

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertFalse(output)

    def test_lambda_derives_to_terminal(self):
        prod_rules = [('A', 'a')]
        nonterminals = set(['A'])
        terminals = set(['a'])

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertFalse(output)

        prod_rules = [('A', 'B'), 
                      ('B', 'C'),
                      ('C', 'c')]
        nonterminals = set(['A', 'B', 'C'])
        terminals = set(['c'])

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertFalse(output)

    def test_lambda_multiple_symbols(self):
        prod_rules = [('A', ['B', 'C', 'D']), 
                      ('B', 'lambda'), 
                      ('C', 'c'),
                      ('C', 'lambda'), 
                      ('D', 'lambda')]
        nonterminals = set(['A', 'B', 'C', 'D'])
        terminals = set(['c'])

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertTrue(output)

        prod_rules = [('A', ['B', 'C', 'D']), 
                      ('B', 'lambda'), 
                      ('C', 'c'),
                      ('C', 'lambda'), 
                      ('D', 'E'),
                      ('E', ['e', 'f', 'g'])]
        nonterminals = set(['A', 'B', 'C', 'D'])
        terminals = set(['c', 'e', 'f', 'g'])

        output = derives_to_lambda('A', [], prod_rules, nonterminals, terminals)
        self.assertFalse(output)

    def test_first_set_terminal(self):
        prod_rules = [('A', 'a')]
        nonterminals = set(['A'])
        terminals = set('a')

        output, _ = first_set('A', set(), prod_rules, nonterminals, terminals)
        self.assertEqual(output, set(['a']))

    def test_first_set_terminal_2(self):
        prod_rules = [('A', 'n'),
                      ('A', ['B', 'M']), 
                      ('B', 'lambda'), 
                      ('M', 'm')]
        nonterminals = set(['A'])
        terminals = set(['m', 'n'])

        output, _ = first_set('A', set(), prod_rules, nonterminals, terminals)
        self.assertEqual(output, set(['m', 'n']))

    def test_first_set_terminal_3(self):
        prod_rules = [('S', ['A', 'M', '$']), 
                      ('A',  ['B', 'C']),
                      ('A',  ['C', 'M']),
                      ('C', ['lambda']), 
                      ('M',  'm')]
        nonterminals = set(['A', 'B', 'C', 'M'])
        terminals = set(['m', 'n'])

        output, _ = first_set('S', set(), prod_rules, nonterminals, terminals)
        self.assertEqual(output, set(['m']))

    def test_first_set_nonterminal(self):
        prod_rules = [('A', ['B', 'C', 'D']), 
                      ('A', 'a'),
                      ('B', 'lambda'), 
                      ('C', 'c'),
                      ('C', 'lambda'), 
                      ('D', 'lambda'),
                      ('D', 'd')]
        nonterminals = set(['A', 'B', 'C', 'D'])
        terminals = set(['a', 'c', 'd'])

        output, _ = first_set('A', set(), prod_rules, nonterminals, terminals)
        self.assertEqual(output, set(['a', 'c', 'd']))

    def test_follow_set_terminal(self):
        prod_rules = [('A', ['a', 'B', 'c']), 
                      ('B', 'b')]
        nonterminals = set(['A', 'B', 'C'])
        terminals = set(['a', 'c'])

        output, _ = follow_set('B', set(), prod_rules, nonterminals, terminals)
        self.assertEqual(output, set(['c']))

    def test_follow_set_nonterminal(self):
        prod_rules = [('A', ['a', 'B', 'C']), 
                      ('B', 'b'),
                      ('C', 'c')]
        nonterminals = set(['A', 'B', 'C'])
        terminals = set(['a', 'b', 'c'])

        output, _ = follow_set('B', set(), prod_rules, nonterminals, terminals)
        self.assertEqual(output, set(['c']))

        prod_rules = [('A', ['a', 'B', 'C', 'D']), 
                      ('B', 'b'),
                      ('C', 'c'), 
                      ('C', 'lambda'),
                      ('D', 'd')]
        nonterminals = set(['A', 'B', 'C', 'D'])
        terminals = set(['a', 'b', 'c', 'd'])

        output, _ = follow_set('B', set(), prod_rules, nonterminals, terminals)
        self.assertEqual(output, set(['c', 'd']))



if __name__ == '__main__':
    unittest.main()