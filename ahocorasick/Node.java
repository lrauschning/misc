//package ahoc;

import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Queue;
import java.util.ArrayDeque;
import java.util.stream.Stream;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Node{
	public final Character val;
	// this is unique for each leaf and uninteresting for any internal Node
	public final String pattern;
	public Node failure;
	public HashMap<Character, Node> children;
	public Node parent; // optional

	public Node(Character val, String pattern){
		this.val = val;
		this.pattern = pattern;
		this.children = new HashMap<Character, Node>(4);
	}

	private Node(Character val, String pattern, Node parent){
		this(val, pattern);
		this.parent=parent;
	}

	public boolean isRoot(){
		return val == null; // this encodes a root node
	}

	@Override
	public String toString(){
		StringBuilder sb = new StringBuilder("Node:\n");
		sb.append("\t val:");
		if(val != null){
		sb.append(val.charValue());
		sb.append("\n\t failure:");
		sb.append(failure.val == null ? "root" : failure.pattern);
		} else 
			sb.append("root");
		sb.append("\n\t children:\n<<<\n");
		// recursively call children
		for(Node ch: children.values())
			sb.append(ch.toString());
		
		sb.append(">>>\n");
		return sb.toString();
	}

	// maybe change from String?
	public HashMap<String, List<Integer>> search(String text){
		HashMap<String, List<Integer>> occs = new HashMap<String, List<Integer>>(4);
		Node curr = this;
		char c = 0;
		for(int i=0; i<text.length(); i++){
			c = text.charAt(i);

			while(!curr.children.containsKey(c) && !curr.isRoot())
				curr = curr.failure;

			if(curr.children.containsKey(c))
				curr = curr.children.get(c);
			
			//System.out.println("search loop: i: "+i+", pstart: "+pstart+", Node: "+ (curr.isRoot() ? "root" : curr.val));
			
			// handle a pattern match
			if(curr.children.isEmpty()){ // if we are at a leaf
				int pos = i - curr.pattern.length() + 1;
				if(occs.containsKey(curr.pattern))
					occs.get(curr.pattern).add(pos);
				else{
					ArrayList<Integer> patoccs = new ArrayList<Integer>();
					patoccs.add(pos);
					occs.put(curr.pattern, patoccs);
				}
			}
		}

		return occs;
	}

	// constructs an aho-corasick search tree, with this node as the root
	public void init(Stream<String> patterns){
		// init the tree
		//for(String pat: patterns){
		patterns.forEach(pat -> {
			Node curr = this;
			for(char c: pat.toCharArray()){
				if(curr.children.containsKey(c)){
					curr = curr.children.get(c);
				} else {
					Node born = new Node(c, pat, curr);
					curr.children.put(c, born);
					curr = born;
				}
			}
		});

		// calculate the failure links
		// maintain a queue, in order to do a breadth-first traversal
		Queue<Node> qu = new ArrayDeque<Node>();

		// init level 1
		for(Node lev1: this.children.values()){
			lev1.failure = this;
			qu.addAll(lev1.children.values());
		}

		Node cand; // stores the candidate failure link
		Node curr; // stores the node currently being looked at
		// begin the failure linking
		while(!qu.isEmpty()){
			curr = qu.remove();
			qu.addAll(curr.children.values());

			cand = curr.parent.failure;
			while(!cand.isRoot() && !cand.children.containsKey(curr.val))
				cand = cand.failure;

			if(cand.children.containsKey(curr.val))
				curr.failure = cand.children.get(curr.val);
			else
				curr.failure = this;	
		}
		}



	public static void main(String[] args){
		Stream<String> patterns = null;
		String text = null;
		Node root = new Node(null, null);
		try{
			text = Files.readString(Path.of(args[0]));
			patterns = Files.lines(Path.of(args[1]));
		} catch(IOException e){
			System.out.println("Error reading files!");
			e.printStackTrace();
		}

		root.init(patterns);
		//System.out.println(root.toString());

		var occs = root.search(text);

		System.out.println("p_i\tindex");
		for(var l: occs.entrySet()){
			System.out.print(l.getKey());
			System.out.print("\t");
			System.out.println(l.getValue());
		}
	}
}
