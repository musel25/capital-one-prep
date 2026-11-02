import java.util.*;

// Independent Java version of the exercise. It returns the text the program must print.
class Marker {
    private String[] lines;
    private StringBuilder out;

    private int num(int i) { return Integer.parseInt(lines[i].trim()); }
    private String line(int i) { return lines[i]; }

    // Like Python print(): one space between the parts, then a new line.
    private void say(Object... parts) {
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) text.append(' ');
            text.append(parts[i]);
        }
        out.append(text).append('\n');
    }

    private void run() {
        int price = 3, count = 4; say("Total:", price * count, "dollars");
    }

    public String program(String input) {
        lines = (input == null ? "" : input).replace("\r\n", "\n").split("\n", -1);
        out = new StringBuilder();
        try {
            run();
        } catch (RuntimeException e) {
            return "(This test input does not fit this exercise.)";
        }
        return clean(out.toString());
    }

    // Spaces at the end of a line and empty lines at the end do not count.
    static String clean(String text) {
        if (text == null) return "";
        String[] rows = text.replace("\r\n", "\n").split("\n", -1);
        List<String> kept = new ArrayList<>();
        for (String row : rows) kept.add(row.replaceAll("[ \t]+$", ""));
        while (!kept.isEmpty() && kept.get(kept.size() - 1).isEmpty()) kept.remove(kept.size() - 1);
        return String.join("\n", kept);
    }

    public boolean isCorrect(String input, String output) {
        return program(input).equals(clean(output));
    }
}
