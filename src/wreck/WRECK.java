package wreck;

import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

public class WRECK {
    public static void main(String[] args) throws IOException, InterruptedException {
        Scanner reader = new Scanner(new File(args[0]));
        String firstline = reader.nextLine();
        ArrayList<Character> chars = new ArrayList<>();
        String[] split = firstline.split("\\s+");
        for (int i = 0; i < split.length; i++) {
            String s = split[i];
            while (s.length() > 0) {
                if (s.charAt(0) == 'x') {
                    chars.add((char) Integer.parseInt(s.substring(1, 3), 16));
                    s = s.substring(3);
                } else {
                    chars.add(s.charAt(0));
                    s = s.substring(1);
                }
            }
        }
        ArrayList<Map<Character, ArrayList<Integer>>> NFA_Tables = new ArrayList<>();
        while (reader.hasNextLine()) {
            String[] line = reader.nextLine().split("\\s+");
            if (line.length < 2) {
                continue;
            }
            String regex = line[0];
            Map<Character, ArrayList<Integer>> transitionTable = new HashMap<>();
            for (char c: chars) {
                transitionTable.put(c, new ArrayList<>());
            }
            PrintWriter lgaIn = new PrintWriter("regexOut.txt");
            lgaIn.print(regexFormat(regex));
            lgaIn.close();
            Runtime rt = Runtime.getRuntime();
            Process pr = rt.exec("py src\\PHP\\parse_tree.py regexOut.txt src\\PHP\\LGA22\\llre.cfg out.txt");
            pr.waitFor();
            System.out.println("done" + pr.exitValue());

            //TODO use lga code to generate NFA
            if (line.length == 3) {
                NFA_Tables.add(transitionTable);
            } else {
                NFA_Tables.add(transitionTable);
            }
        }
        //TODO convert tt to files
    }

    public static String regexFormat(String regex) {
        String out = "";
        for (int i = 0; i < regex.length(); i++) {
            switch (regex.charAt(i)) {
                case '(':
                    out += "open (\n";
                    break;
                case ')':
                    out += "close )\n";
                    break;
                case '|':
                    out += "pipe |\n";
                    break;
                case '.':
                    out += "dot .\n";
                    break;
                case '+':
                    out += "plus +\n";
                    break;
                case '-':
                    out += "dash -\n";
                    break;
                case '*':
                    out += "kleene *\n";
                    break;
                case '\\':
                    if (regex.charAt(i+1) == 's') {
                        out += "char  \n";
                        break;
                    }
                    i++;
                default:
                    out += "char " + regex.charAt(i) + "\n";
                    break;
            }
        }
        return out;
    }
}
