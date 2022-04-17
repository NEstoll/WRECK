package wreck;

import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

public class WRECK {
    public static void main(String[] args) throws IOException {
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
        ArrayList<Pair<Pair<String, String>, ArrayList<Pair<Boolean, ArrayList<Integer>>>>> NFA_Tables = new ArrayList<>();
        while (reader.hasNextLine()) {
            String[] line = reader.nextLine().split("\\s+");
            if (line.length < 2) {
                continue;
            }
            String regex = line[0];
            ArrayList<Pair<Boolean, ArrayList<Integer>>> transitionTable = new ArrayList<>();
            //TODO use lga code to generate NFA
            if (line.length == 3) {
                NFA_Tables.add(new Pair<>(new Pair<>(line[1], line[2]), transitionTable));
            } else {
                NFA_Tables.add(new Pair<>(new Pair<>(line[1], null), transitionTable));
            }
        }
        //TODO convert tt to files

    }

    public static class Match {
        public String longest = "";
        public int line = 1;
        public int charNum = 1;

        public Match() {
        }

        public Match(int line, int charNum) {
            this.line = line;
            this.charNum = charNum;
        }
    }
}
