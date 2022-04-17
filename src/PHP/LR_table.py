class State:
    def __init__(self, accepting, reduce, num):
        self.accepting = accepting
        self.reduce = reduce
        self.num = num


def readTable(file):
    LRtable = []
    with open(file, "r") as f:
        chars = f.readline()[2::].rstrip().split(",")
        for i, line in enumerate(f):
            LRtable.append([])
            for s in line[2::].rstrip().split(","):
                if not s:
                    continue
                elif s[0:1] == "s":
                    LRtable[i].append(State(False, False, int(s[3::])))
                else:
                    if s[0:1].islower():
                        LRtable[i].append(State(False, True, int(s[2::])))
                    else:
                        LRtable[i].append(State(True, True, int(s[2::])))
    return (chars, LRtable)
