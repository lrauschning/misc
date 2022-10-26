use std::collections::HashMap; // could use arrays instead, but hashmap is cleaner
use std::fmt::Display;


// there is an example where the optimal tree uses a suboptimal subtree
// A -> C: 1 // i think this is only the case for asymmetric distance functions?
// C -> A: 1.5
// 
// A1:(A0:(A, A), C)
// A2:(A1:(A0(A, A), C), C)
// C1.5(C1.5(A0(A, A), C), C)


const ALPHABET:[char;4] = ['A', 'C', 'G', 'T'];

/// scoring function, takes two chars and outputs the mutation distance
pub fn S(a:char, b:char) -> usize{
    //if a == b {
    //    0
    //} else {
    //    1
    //}

    if a == b {
        return 0
    }

    // lambda to determine whether a base is purine/pyrimidine
    let basetype = |x| if x=='C' || x =='T' {'Y'} else {'R'};
    if basetype(a) == basetype(b){
        1
    } else {
        2
    }
}


#[derive(Default, Debug)]
struct Node{
    pub seq: char, // u8 could be more appropriate, but this is cleaner
        pub children: [Option<Box<Node>>; 2],
        pub scores: HashMap<char, usize>,
}

impl Display for Node {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("{}", self.seq))?;
        if !self.is_leaf(){
            f.write_str("(")?;
            let mut buffer = Vec::with_capacity(2);
            for ch in self.children.iter().flatten(){
                buffer.push(
                    if let Some(val) = self.scores.get(&ch.seq){
                        format!("{}:{}", ch, val)
                    } else {
                        format!("{}", ch)
                    }
                    )
            }
            f.write_str(&buffer.join(","))?;
            f.write_str(")")?;
        }
    Ok(())
    }
}

impl Node{
    /// constructor for a leaf
    pub fn leaf(ch: char) -> Self{
        Node{
            seq: ch,
            children: [None, None],
            scores: HashMap::new(),
        }
    }

    /// constructor for an inner node, allow annotation with optimal seq later
    pub fn inner(ch1:Node, ch2:Node) -> Node{
        Node{
            seq: '0',
            children: [Some(Box::new(ch1)), Some(Box::new(ch2))],
            scores: HashMap::new(),
        }
    }

    pub fn is_leaf(&self) -> bool{
        self.children.iter().all(Option::is_none)
    }

    /// helper function, get the score corresponding to a character from self.scores
    /// and also do it correctly in leaves
    fn get_score(&self, ch: char) -> usize{
        **self.scores.get(&ch).get_or_insert(&S(ch, self.seq)) // if this is a leaf, substitute
    }

    /// implementation of a variant of the fitch algorithm for parsimony scoring of a mutation tree.
    /// This algorithm has been expanded from the standard fitch algorithm in that it can deal with general mutation cost functions.
    pub fn fitch(&mut self){
        if self.is_leaf(){
            return
        }

        for child in self.children.iter_mut().flatten(){
            child.fitch()
        }

        // calculate new scoring matrix
        let mut scores = HashMap::with_capacity(ALPHABET.len());
        for ch in ALPHABET {
            scores.insert(ch,
                          // select the optimal annotation for each child, given the parent annotation ch
                          self.children.iter().flatten().map(|child| 
                              ALPHABET.iter().map(|&ch_child| S(ch, ch_child)
                              + child.get_score(ch_child)).min().expect("ALPHABET should not be empty!")
                          ).sum());
        }

        self.scores = scores;
        // score the index of the optimal annotation for the subtree starting from this node
        // reverse the tuple to properly sort lexicographically
        if let Some((_, ch)) = self.scores.iter().map(|(x, y)| (y, x)).min() {
            self.seq = *ch
        }
    }

    /// given a tree which has had its scores calculated by a call to fitch(),
    /// annotate each node with the correct sequence label by backtracking
    /// Panics if the node does not have a sequence label in ALPHABET
    pub fn label(&mut self){
        if self.is_leaf(){
            return;
        }

        if !ALPHABET.iter().any(|&x| x == self.seq){
            panic!("Node.label: Node.seq not in ALPHABET!");
        }

        let s = self.seq; // store the current annotation in a variable.
                          // only necessary for the borrow checker not to complain

        for child in self.children.iter_mut().flatten() {
            if !child.is_leaf(){
                //TODO maybe set to prefer existing annotation instead of lexicalic ordering?
                child.seq = ALPHABET.iter().map(|&child_ch| (S(s, child_ch) + child.get_score(child_ch), child_ch)).min().expect("ALPHABET should not be empty!").1;
                child.label(); // propagate up
            }
        }

    }
}


fn main(){
    // some testcases
    let mut tree = Node::inner(Node::leaf('T'), Node::leaf('G'));
    println!("{}", tree);
    tree.fitch();
    tree.label();
    println!("{}", tree);
    // tree from https://evol.bio.lmu.de/_statgen/compevol/phylo02.pdf ex. 1
    let mut tree = Node::inner(Node::inner(Node::inner(Node::inner(Node::leaf('A'), Node::leaf('A')), Node::leaf('G')), Node::inner(Node::leaf('G'), Node::leaf('T'))), Node::inner(Node::leaf('A'), Node::leaf('T')));
    println!("{}", tree);
    tree.fitch();
    println!("{}", tree);
    tree.label();
    println!("{}", tree);
}
