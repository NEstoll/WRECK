
def main():
    inputFileName = "Sean_RE_test.txt"
    outputFileName = "Sean_RE_test_res.txt"
    
    inputFile = readFromFile(inputFileName)

    output = scan(inputFile)

    outputFile = open(outputFileName, "w")
    
    for i in output:
        outputFile.write(i)
        outputFile.write('\n')
    outputFile.close()


def scan(inputFile):
    output = []
    lines = inputFile.readline()

    i = 0
    while i < len(lines):
        line = ''

        line += lines[i]
        if (lines[i] == "\\"):
            i += 1
            line += lines[i]
        i += 1
        
        output.append(line)

    for i in range(len(output)):
        token = output[i]
        if token == '|':
            output[i] = 'pipe ' + output[i]
        elif token == '*':
            output[i] = 'kleene ' + output[i]
        elif token == '+':
            output[i] = 'plus ' + output[i]
        elif token == '(':
            output[i] = 'open ' + output[i]
        elif token == ')':
            output[i] = 'close ' + output[i]
        elif token == '.':
            output[i] = 'dot ' + output[i]
        elif token == '-':
            output[i] = 'dash ' + output[i]
        else:
            output[i] = 'char ' + output[i]

    return output


def readFromFile(inputFileName):
    try:
        inputFile = open(inputFileName, "r")
    except OSError:
        sys.stderr.write("Error opening input file")
        sys.exit(1)

    return inputFile
    
main()
