use std::env;

/// efficient rust implementation of the mortal fibonacci rabbit problem on Rosalind

fn main(){
    let args : Vec<String> = env::args().collect();
    let n : usize = args[1].parse().unwrap();
    let m : usize = args[2].parse().unwrap();

    // 0: buffer, 1: young rabbits, 2-m+1: mature rabbits
    let mut fib: Vec<usize>= vec![0; m+1];
    fib[1]=1;

    // simulation loop
    for _ in 1..n{
        fib[0]=0;
        for i in 2..=m{
            fib[0]+=fib[i];
        }
        for i in (1..=m).rev() {
            fib[i]=fib[i-1];
        }
    }
    //dbg!(fib);
    println!("{}", fib.iter().sum::<usize>()-fib[0]);
}
