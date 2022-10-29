use std::ops::Mul;
use std::ops::Add;
use std::fmt::Display;


pub fn main(){
    // very very simple testcase
    let mut tree = Node::hidden(Node::leaf(b"A", 0.0), Node::leaf(b"A", 0.0), 0.0);
    println!("{:?}", tree);
    tree.felsenstein();
    println!("{:?}", tree);

    // very simple testcase
    let mut tree = Node::hidden(Node::leaf(b"ACG", 1.0), Node::leaf(b"ACG", 1.0), 0.0);
    println!("{:?}", tree);
    tree.felsenstein();
    println!("{:?}", tree);

    // simple testcase
    let mut tree = Node::hidden(Node::leaf(b"A", 0.5), Node::leaf(b"G", 1.0), 0.0);
    println!("{:?}", tree);
    tree.felsenstein();
    println!("{:?}", tree);

    // simple testcase
    let mut tree = Node::hidden(Node::hidden(Node::leaf(b"A", 0.5), Node::leaf(b"A", 0.5), 1.0), Node::leaf(b"G", 1.0), 0.0);
    println!("{:?}", tree);
    tree.felsenstein();
    println!("{:?}", tree);
}

type Base = u8;
const MUT_RATE:f64 = 0.1;
//const SEQ_EV:Fn<> = jc;
const ALPHABET:[char;4] = ['A', 'C', 'G', 'T'];

/// returns the transition probabilities of a jukes-cantor-model
/// with distance d as a Probs object
fn jukes_cantor(x:Base, d:f64) -> Probs{
    let exp = f64::exp(-MUT_RATE*d);
    Probs{
        a: if x == b'A' {
            (1_f64 + 3_f64*exp)/4_f64
        } else {
            (1_f64-exp)/4_f64
        },
        c: if x == b'C' {
            (1_f64 + 3_f64*exp)/4_f64
        } else {
            (1_f64-exp)/4_f64
        },
        g: if x == b'G' {
            (1_f64 + 3_f64*exp)/4_f64
        } else {
            (1_f64-exp)/4_f64
        },
        t: if x == b'T' {
            (1_f64 + 3_f64*exp)/4_f64
        } else {
            (1_f64-exp)/4_f64
        },
    }
}

#[derive(Debug, Clone)]
struct Probs{
    a: f64, c: f64, g:f64, t:f64,
}

impl Display for Probs {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("{{A:{}, C:{}, G:{}, T:{}}}", self.a, self.c, self.g, self.t))
    }
}

impl Add for Probs {
    type Output = Self;

    /// pairwise addition, i.e. calculate the independent union probability
    fn add(self, other: Self) -> Self {
        Self{
            a:self.a+other.a,
            c:self.c+other.c,
            g:self.g+other.g,
            t:self.t+other.t
        }
    }
}

impl Mul for Probs {
    type Output = Self;
    /// pairwise multiplication, i.e. calculate the independent joint probability
    fn mul(self, other: Self) -> Self {
        Self{
            a:self.a*other.a,
            c:self.c*other.c,
            g:self.g*other.g,
            t:self.t*other.t
        }
    }
}

impl Probs{
    fn new(a:f64, c:f64, g:f64, t:f64) -> Self{
        Probs{a, c, g, t}
    }

    fn sum(&self) -> f64{
        self.a + self.c + self.g + self.t
    }

    /// multiply with a scalar
    fn scale(&mut self, v:f64){
        self.apply(|x| v*x)
    }

    /// apply a function to the probability vector, element-wise
    fn apply(&mut self, f:impl Fn(f64) -> f64){
        self.a = f(self.a);
        self.c = f(self.c);
        self.g = f(self.g);
        self.t = f(self.t);
    }

    fn ln(&mut self){
        self.apply(&f64::ln);
    }

    fn exp(&mut self){
        self.apply(&f64::exp);
    }

    fn from_base(b:Base) -> Self{
        match b {
            b'A' => Probs{a:1.0, c:0.0, g:0.0, t:0.0},
            b'C' => Probs{a:0.0, c:1.0, g:0.0, t:0.0},
            b'G' => Probs{a:0.0, c:0.0, g:1.0, t:0.0},
            b'T' => Probs{a:0.0, c:0.0, g:0.0, t:1.0},
            _ => panic!("Not a base!"),
            //TODO maybe handle non-standard bases?
        }
    }
}

#[derive(Debug)]
struct Node {
    pub probseq: Vec<Probs>, // maybe box this?
        pub d: f64, // distance to the PARENT
        pub l: Option<Box<Node>>,
        pub r: Option<Box<Node>>,
}

impl Node {
    fn leaf(seq:&[Base], d:f64) -> Self{
        Node{
            probseq: seq.iter().map(|&x| Probs::from_base(x)).collect::<Vec<Probs>>(),
            d: d, 
            l: None,
            r: None,       
        }
    }

    fn hidden(l:Node, r:Node, d:f64) -> Self{
        //assert!(l.probseq.len() == r.probseq.len());
        Node{
            probseq: Vec::new(),
            d: d,
            l: Some(Box::new(l)),
            r: Some(Box::new(r)),
        }
    }

    //fn proball(&self) -> Probs{
    //    *self.probseq.iter().reduce(|x, y| x*y).expect("")
    //}

    //fn probtotal(&self) -> f64{
    //    self.proball().sum()
    //}

    fn is_leaf(&self) -> bool{
        self.l.is_none() && self.r.is_none() // an internal node needs two children, anyway
    }

    fn felsenstein(&mut self){
        // terminate on leaves
        if self.is_leaf(){
            return;
        }
        let lch = self.l.as_mut().expect("internal node should have two children!");
        let rch = self.r.as_mut().expect("internal node should have two children!");

        // recursively climb the tree
        lch.felsenstein();
        rch.felsenstein();
        assert!(lch.probseq.len() == rch.probseq.len());

        // lambda to calculate the one value of the new Probs object
        let np_base = |b: Base, l:&Probs, r:&Probs| -> f64 {
            (jukes_cantor(b, lch.d)*l.clone()).sum() *(jukes_cantor(b, rch.d)*r.clone()).sum()
        };

        let np = |l:&Probs, r:&Probs| -> Probs {Probs{ // maybe recopy code back into here?
            a: np_base(b'A', l, r), c: np_base(b'C', l, r),
            g: np_base(b'G', l, r), t: np_base(b'T', l, r),
        }};

        self.probseq = std::iter::zip(lch.probseq.iter(), rch.probseq.iter()).map(|(x, y)| np(x, y)).collect::<Vec<Probs>>();
    }
}
