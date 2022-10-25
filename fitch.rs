use std::collections::HashMap; // could use arrays instead, but hashmap is cleaner
use std::fmt::Display;


const ALPHABET:[char;4] = ['A', 'C', 'G', 'T'];

/// scoring function, takes two bytes from a string slice and outputs the mutation distance
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
    pub seq: char, // u8 would be more appropriate, but this is cleaner
        pub children: [Option<Box<Node>>; 2],
        pub scores: HashMap<char, usize>,
}

impl Display for Node {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("{}", self.seq))?;
        if !self.is_leaf(){
            f.write_str("(")?;
            let mut buffer = Vec::with_capacity(2);
            for x in &self.children{
                if let Some(ch) = x{
                    buffer.push(
                    if let Some(val) = self.scores.get(&ch.seq){
                        format!("{}:{}", ch, val)
                    } else {
                        format!("{}", ch)
                    }
                    )
                }
            }
            f.write_str(&buffer.join(","))?;
            f.write_str(")")?;
        }
        return Ok(())
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

    /// constructor for an internal node, allow annotation with optimal seq later
    pub fn internal<'a>(ch1:Node, ch2:Node) -> Node{
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

        for ch in self.children.iter_mut(){
            if let Some(child) = ch{
                child.fitch()
            }
        }

        // calculate new scoring matrix
        let mut scores = HashMap::with_capacity(ALPHABET.len());
        for ch in ALPHABET {
            scores.insert(ch,
                self.children.iter().map(|x| if let Some(child) = x {
                    // select the optimal annotation for each child, given the parent annotation ch
                    ALPHABET.iter().map(|&ch_child| S(ch, ch_child) + child.get_score(ch_child)).min().expect("")
                } else {0}).sum());
        }

        self.scores = scores;
        // reverse the tuple to properly sort lexicographically
        if let Some((_, ch)) = self.scores.iter().map(|(x, y)| (y, x)).min() {
            self.seq = *ch
        }
    }
}


fn main(){
    // some testcases
    let mut tree = Node::internal(Node::leaf('A'), Node::leaf('G'));
    println!("{}", tree);
    tree.fitch();
    println!("{}", tree);
    let mut tree = Node::internal(Node::internal(Node::leaf('A'), Node::leaf('G')), Node::leaf('G'));
    println!("{}", tree);
    tree.fitch();
    println!("{}", tree);
    let mut tree = Node::internal(Node::internal(Node::leaf('A'), Node::internal(Node::leaf('G'), Node::leaf('G'))), Node::leaf('G'));
    println!("{}", tree);
    tree.fitch();
    println!("{}", tree);

}
