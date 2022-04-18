from build_table import build_table
from GrammarParser import GrammarParser
from collections import deque
import sys
import os.path
import copy


# Base class for nodes in parse tree
# Children classes should be created to implement SDT procedures
class TreeNode:
    def __init__(self, nodeName, nodeType, value):
        self.name = nodeName
        self.type = nodeType
        self.children = []
        self.parent = self
        self.id = -1
        if value is None:
            self.value = ''
        else:
            self.value = value

    def SDT(self):
        return


# Example child class with a simple SDT procedure
class Seq(TreeNode):
    def __init__(self, type, value):
        super().__init__(type, value)

    def SDT(self):
        if len(self.children) == 1:
            self.type = "lambda"
            self.value = "lambda"
            self.children = []
        self.type = self.children[0].type
        self.value = self.children[0].value
        self.children = []
        return


##flatten
def flatten(Node):
    hold = []
    for x in Node.children:
        if not isinstance(x, str):
            if (x.data == Node.data):
                for y in x.children:
                    y.parent = Node
                    hold.append(y)
            else:
                hold.append(x)
    Node.children = hold
    print("test")


def rotate(Node):
    size = len(Node.children)
    hold = []

    for x in range(0, size):
        hold.append(0)

    count = 1
    for x in Node.children:
        hold[count] = x
        count += 1
        if count == size:
            count = 0
    Node.children = hold
    print("test")

# https://graphviz.org/
# usage
# cd ParseVisualization
# cat parsetree.txt | ./tree-to-graphvis | dot -Tpng -o parsetree.png
def WriteTreeToFile(node: TreeNode, Output_File_Name="ParseVisualization/parsetree.txt"):
    # do a BFS on the ParseTree to get
    node_id = 0
    node.node_id = node_id
    Q = deque()  # Queue for BFS, parse trees are DAGS so no need to track visited
    Q.append(node)
    node_identifiers: list[str] = []  #(NodeID, NodeID-ValueForNode)
    edge_identifers: list[str] = []  # NodeID Edge1 Edge2 Edge3

    while len(Q) > 0:
        current_node = Q.popleft()
        if current_node.id == -1:
            current_node.id = node_id
            node_id += 1
        node_identifiers.append(f'{str(current_node.id)} {current_node.name}')
        edges = []
        # current_node points to node1,node2,node...
        for child_node in current_node.children:
            if type(child_node) is TreeNode:
                child_node.id = node_id
                node_id += 1
                edges.append(str(child_node.id))
            elif type(child_node) is str:  # have to handle str node in 1 step
                node_identifiers.append(f'{str(node_id)} {child_node}')
                edges.append(f'{str(node_id)}')
                node_id += 1
        Q.extend(child_node for child_node in current_node.children if type(child_node) is TreeNode)
        if len(edges) > 0:
            edge_identifers.append(f'{current_node.id} {" ".join(edges)}')

    with open(Output_File_Name, "w") as f:
        for node in node_identifiers:
            f.write(f'{node}\n')
        f.write('\n')
        for edge in edge_identifers:
            f.write(f'{edge}\n')

def printTree(Node):
    out = '['
    out += Node.name
    for x in Node.children:
        if x.type == "Leaf":
        #if isinstance(x, str):
            out += '[' + x.name + ":" + x.value + ']'
        else:
            out += printTree(x)
    out += ']'
    return out


def LLTreeParse(ts, LLT, P, start, N, term):
    RootT = TreeNode("Root", "Node", None)
    Current = RootT
    K = []
    K.append(start)
    while len(K) > 0:
        x = K.pop()
        ts_values = ts[0].split()
        if x in N:
            if x in LLT:
                # if LLT[x][ts[0]] > 0:
                if LLT[x][ts_values[0]] > 0:
                    p = LLT[x][ts_values[0]]
                    K.append('*')
                    R = copy.copy(P[p - 1][1])
                    while len(R) > 0:
                        K.append(R.pop())
                    match x:  # Add cases to match for SDT
                        case _:
                            # n = TreeNode(x)
                            n = TreeNode(x, 'Node', None)
                    n.parent = Current
                    Current.children.append(n)
                    Current = Current.children[len(Current.children) - 1]
        elif x in term:
            if x != 'lambda' and x != '$':
                if x != ts_values[0]:
                    raise ValueError("not expected token")
                x = ts_values[0]
                ts = ts[1:]
            #Current.children.append(x)
            if len(ts_values) < 2:
                n = TreeNode(x, 'Leaf', '')
            else:
                n = TreeNode(x, 'Leaf', ts_values[1])
            Current.children.append(n)
        elif x == 'lambda':
            n = TreeNode(x, 'Leaf', x)
            Current.children.append(n)
        elif x == '*':
            Current.SDT()
            Current = Current.parent
        else:
            raise ValueError("unknown token in tokenstream")

    return RootT.children[0]


holdToken = []
if len(sys.argv) < 3:
    print("Must pass input files as argument.")
    sys.exit(1)

file = sys.argv[1]

cfgFile = sys.argv[2]

if not os.path.isfile(file):
    print("Input file does not exist.")
    sys.exit(1)

with open(file) as f:
    holdToken = [line.rstrip('\n') for line in f]

holdToken.append('$')
grammar = GrammarParser(cfgFile).parse_grammar()
production_rules = grammar['production rules']
nonterminals = grammar['nonterminals']
terminals = grammar['terminals']
start = grammar['start symbol']

LLTable = build_table(production_rules, nonterminals, terminals)

Root = LLTreeParse(holdToken, LLTable, production_rules, start, nonterminals, terminals)

# flatten(Root.children[0].children[0].children[1]) ##for testing flatten logic

# rotate(Root) ##for testing rotate logic

WriteTreeToFile(Root, sys.argv[3])

out = printTree(Root)

print(out)
