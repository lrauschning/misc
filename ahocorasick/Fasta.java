import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.TreeMap;

public class Fasta {

    int k;
    String db;
    String query;

    public Fasta(int k, String db, String query) {
        this.k = k;
        this.db = db;
        this.query = query;
    }

    public void computeHashes(String outputPath) {
        TreeMap<String, ArrayList<Integer>> db_kmers = new TreeMap<>();
        for (int i = 0; i <= this.db.length() - this.k; i++) {
            String act_tuple_db = this.db.substring(i, i + this.k);
            if (db_kmers.containsKey(act_tuple_db)) {
                db_kmers.get(act_tuple_db).add(i);
            } else {
                ArrayList<Integer> list = new ArrayList<>();
                list.add(i);
                db_kmers.put(act_tuple_db, list);
            }
        }

        TreeMap<String, ArrayList<Integer>> offset_list = new TreeMap<>();
        for (int i = 0; i <= this.query.length() - this.k; i++) {
            String act_tuple_query = this.query.substring(i, i + this.k);
            if (db_kmers.containsKey(act_tuple_query)) {

                // Deep copy necessary - Java sucks
                ArrayList<Integer> act_offset = new ArrayList<>(db_kmers.get(act_tuple_query));

                for (int j = 0; j < act_offset.size(); j++) {
                    int actValue = act_offset.get(j);
                    act_offset.set(j, actValue - i);
                }
                if (offset_list.containsKey(act_tuple_query)) {
                    offset_list.get(act_tuple_query).addAll(act_offset);
                } else {
                    offset_list.put(act_tuple_query, act_offset);
                }
            }
        }
        writeOffsetList(offset_list, outputPath);
        writeOffsetVector(offset_list, outputPath);
    }

    private void writeOffsetList(TreeMap<String, ArrayList<Integer>> offset_list, String outputPath) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(outputPath + ".list"))) {
            for (String key : offset_list.keySet()) {
                bw.write(key + "\t" + offset_list.get(key) + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void writeOffsetVector(TreeMap<String, ArrayList<Integer>> offset_list, String outputPath) {
        TreeMap<Integer, Integer> offset_vector = new TreeMap<>();
        for (ArrayList<Integer> list : offset_list.values()) {
            for (int el : list) {
                if (offset_vector.containsKey(el)) {
                    offset_vector.put(el, offset_vector.get(el) + 1);
                } else {
                    offset_vector.put(el, 1);
                }
            }
        }
        ArrayList<Integer> offset_vector_idx = new ArrayList<>();
        for (int i = -this.query.length() + this.k; i <= db.length() - k; i++) {
            offset_vector_idx.add(i);
        }
        ArrayList<Integer> offset_vector_list = new ArrayList<>();
        for (int el : offset_vector_idx) {
            offset_vector_list.add(offset_vector.getOrDefault(el, 0));
        }

        try (BufferedWriter bw = new BufferedWriter(new FileWriter(outputPath + ".vector"))) {
            bw.write("[");
            if (offset_vector_idx.size() > 0) {
                bw.write("" + offset_vector_idx.get(0));
                for (int i = 1; i < offset_vector_idx.size(); i++) {
                    bw.write(", " + offset_vector_idx.get(i));
                }
            }
            bw.write("]\n");
            bw.write("[");
            if (offset_vector_list.size() > 0) {
                bw.write("" + offset_vector_list.get(0));
                for (int i = 1; i < offset_vector_list.size(); i++) {
                    bw.write(", " + offset_vector_list.get(i));
                }
            }
            bw.write("]\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
