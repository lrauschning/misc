public class Runner {
    public static void main(String[] args) {
        try {
            int k = Integer.parseInt(args[0]);
            if (k <= 0) throw new IllegalArgumentException();
            String db = args[1];
            String query = args[2];
            String outputPath = args[3];
            Fasta fasta = new Fasta(k, db, query);
            fasta.computeHashes(outputPath);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
