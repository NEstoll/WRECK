package wreck;

import java.io.*;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class WRECK {
    static Map<Character, Integer> charMap;
    static char lambda;

    public static void main(String[] args) throws IOException, InterruptedException {
        Scanner reader = new Scanner(new File(args[0]));
        PrintWriter out = new PrintWriter(args[1]);
        String firstline = reader.nextLine();
        out.println(firstline);
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
        ArrayList<ArrayList<ArrayList<Integer>>> NFA_Tables = new ArrayList<>();
        while (reader.hasNextLine()) {
            String[] line = reader.nextLine().split("\\s+");
            if (line.length < 2) {
                continue;
            }
            String regex = line[0];
            charMap = new HashMap<>();
            for (int i = 0; i < chars.size(); i++) {
                char c = chars.get(i);
                charMap.put(chars.get(i), i);
            }
            lambda = 'l';
            while (chars.contains(lambda)) {
                lambda++;
            }
            charMap.put(lambda, chars.size());
            ArrayList<ArrayList<ArrayList<Integer>>> transitionTable = new ArrayList<>();
            addRow(transitionTable);
            addRow(transitionTable);

            PrintWriter lgaIn = new PrintWriter("_regexOut.txt");
            lgaIn.print(regexFormat(regex));
            lgaIn.close();
            Runtime rt = Runtime.getRuntime();
            Process pr = rt.exec("python3 PHP/parse_tree.py _regexOut.txt PHP/LGA22/llre.cfg _out.txt");
            pr.waitFor();
            //System.out.println("done" + pr.exitValue());
			if (pr.exitValue() != 0) {
				System.exit(2);
			}
            Scanner tree = new Scanner(new File("_out.txt"));
            String next = tree.nextLine();
            Map<Integer, TreeNode> states = new HashMap<>();
            while (!next.equals("")) {
                states.put(Integer.parseInt(next.split(" ")[0]), new TreeNode(next.split(" ")[1]));
                next = tree.nextLine();
            }
            while (tree.hasNextLine()) {
                next = tree.nextLine();
                int from = Integer.parseInt(next.split(" ")[0]);
                String[] s = next.split(" ");
                for (int i = 1, sLength = s.length; i < sLength; i++) {
                    int to = Integer.parseInt(s[i]);
                    states.get(from).addChildren(states.get(to));
                }
            }
            TreeNode root = states.get(0);

            //TODO generate tt from re tree
            makeNFA(root, transitionTable, charMap, 0, 1);

            line[0] = line[1] + ".tt";
            for (String s : line) {
                out.print(s + " ");
            }
            out.println();


            PrintWriter NFA = new PrintWriter(line[1] + ".nfa");
            String charString = "";
            for (char c : chars) {
                charString += "x" + String.format("%02x", (int) c) + " ";
            }
            charString.trim();
            NFA.println(transitionTable.size() + " " + lambda + " " + charString);
            Map<Integer, Character> inverse = charMap.entrySet().stream().collect(Collectors.toMap(Map.Entry::getValue, Map.Entry::getKey));
            for (int i = 0; i < transitionTable.size(); i++) {
                ArrayList<ArrayList<Integer>> row = transitionTable.get(i);

                boolean extra = true;
                for (int k = 0, rowSize = row.size(); k < rowSize; k++) {
                    ArrayList<Integer> l = row.get(k);
                    for (Integer j : l) {
                        if (i == 1) {
                            NFA.print("+ ");
                        } else {
                            NFA.print("- ");
                        }
                        NFA.println(i + " " + j + " x" + String.format("%02x", ((int) inverse.get(k))));
                        extra = false;
                    }
                }
                if (extra) {
                    if (i == 1) {
                        NFA.print("+ ");
                    } else {
                        NFA.print("- ");
                    }
                    NFA.println(i + " " + i);
                }
            }
            NFA.close();
        }
        out.close();
        //TODO convert tt to files
    }

    public static void addRow(ArrayList<ArrayList<ArrayList<Integer>>> transitionTable) {
        transitionTable.add(new ArrayList<>());
        for (Character c : charMap.keySet()) {
            transitionTable.get(transitionTable.size() - 1).add(new ArrayList<>());
        }

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
                    if (regex.charAt(i + 1) == 's') {
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


    static void makeNFA(TreeNode root, ArrayList<ArrayList<ArrayList<Integer>>> tt, Map<Character, Integer> charMap, int start, int end) {
        switch (root.value) {
            case "+":
                addRow(tt);
                int temp = tt.size() - 1;
                makeNFA(root.children.get(0), tt, charMap, start, temp);
                makeNFA(root.children.get(0), tt, charMap, temp, temp);
                tt.get(temp).get(charMap.get(lambda)).add(end);
                break;
            case "*":
                addRow(tt);
                int t = tt.size() - 1;
                tt.get(start).get(charMap.get(lambda)).add(t);
                makeNFA(root.children.get(0), tt, charMap, t, t);
                tt.get(t).get(charMap.get(lambda)).add(end);
                break;
            case "lambda":
                tt.get(start).get(charMap.get(lambda)).add(end);
                break;

            case "-":
                if (root.children.get(0).value.charAt(0) > root.children.get(1).value.charAt(0)) {
                    //semantic error
					System.exit(3);
                } else {
                    for (char c = root.children.get(0).value.charAt(0); c <= root.children.get(1).value.charAt(0); c++) {
                        tt.get(start).get(charMap.get(c)).add(end);
                    }
                }
                break;
            case ".":
                for (char c : charMap.keySet()) {
                    if (c != lambda) {
                        tt.get(start).get(charMap.get(c)).add(end);
                    }
                }
                break;
            case "SEQ":
                int prev = start;
                for (TreeNode n : root.children) {
                    addRow(tt);
                    int next = tt.size() - 1;
                    makeNFA(n, tt, charMap, prev, next);
                    prev = next;
                }
                tt.get(prev).get(charMap.get(lambda)).add(end);
                break;
            case "ALT":
                for (TreeNode n : root.children) {
                    makeNFA(n, tt, charMap, start, end);
                }
                break;
            default:
                tt.get(start).get(charMap.get(root.value.charAt(0))).add(end);
        }
    }
}
