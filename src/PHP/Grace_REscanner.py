def read_file(FNAME):
    text = -1
    try:
        with open(FNAME, "r") as f:
            text = f.read()
        f.close()
    except E:
        print(E)
        quit()
    return text

def scan(input):
    output = []
    current = 0
    while True:
        val = input[current]
        t = None
        if val == '|':
            t = "pipe"
        elif val == '*':
            t = "kleene"
        elif val == '+':
            t = "plus"
        elif val == "(":
            t = "open"
        elif val == ")":
            t = "close"
        elif val == '.':
            t = "dot"
        elif val == '-':
            t = "dash"
        elif val == '\\':
            actual_next = input[current + 1]
            val = None
            if actual_next == 'n':
                val = "x0a"
            elif actual_next == 's':
                val = "x20"
            else:
                val = actual_next
            t = "char"
            current = current+1
        else:
            t = "char"
        output.append((t,val))
        current = current + 1
        if current >= len(input):
            break
    return output

def write_tokens(output, FNAME):
    try:
        with open(FNAME, "w") as f:
            for line in output:
                line_str = line[0] + " " + line[1] + "\n"
                f.write(line_str)
        f.close()
    except:
        print("error trying to write")
        exit()

def main():
    input = read_file("Grace_test.txt")
    output = scan(input)
    write_tokens(output, "Grace_test_res.txt")

main()