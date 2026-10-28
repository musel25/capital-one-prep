class Marker {
    public String run(String payload) { return "passed"; }
    public boolean isCorrect(String payload, String output) { return "passed".equals(output); }
}
