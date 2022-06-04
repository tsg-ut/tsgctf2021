use std::env;
use rug::Integer;
use std::cmp::min;
use rayon::prelude::*;

const PRECISION: u32 = 6000;
const CHUNK_SIZE: u64 = 1000000;

fn pow(base: u32, exp: u32, r#mod: u32) -> u32 {
    let m: u64 = r#mod.into();
    let mut b: u64 = ((base as u64) % m).into();
    let mut p: u64 = 1;
    let mut e: u64 = exp.into();
    while e != 0 {
        if e % 2 == 1 {
            p = (p * b) % m;
        }
        e >>= 1;
        b = (b * b) % m;
    }
    p as u32
}

fn main() {
    let args: Vec<String> = env::args().take(2).collect();
    if args.len() < 2 {
        eprintln!("Usage: ./fast_ln2 <digits>");
        return
    }
    let n = args[1].parse::<u64>().unwrap();
    eprintln!("Calculating {}-{}th digit of ln2 in binary form...", n, n + PRECISION as u64);

    let mut ans: Integer = (0..=((n - 1) / CHUNK_SIZE)).into_par_iter().map(|i| {
        let start = i * CHUNK_SIZE + 1;
        let end = min((i + 1) * CHUNK_SIZE, n);
        let mut chunk_ans = Integer::from(0);
        let max_number = Integer::from(1) << PRECISION;
        for k in start..=end {
            if k % 10000000 == 0 {
                eprintln!("Itertion: {} / {}", k, n);
            }
            let numerator = pow(2, (n - k) as u32, k as u32);
            let denominator = k;
            let result = (Integer::from(numerator) << PRECISION) / denominator;
            chunk_ans += result;
            while chunk_ans >= max_number {
                chunk_ans -= max_number.clone();
            }
        }
        chunk_ans
    }).sum();

    let mut k = n;
    let mut prev_ans = Integer::from(1);
    let max_number = Integer::from(1) << PRECISION;
    while prev_ans != ans {
        k += 1;
        prev_ans = ans.clone();
        ans += (Integer::from(1) << (n as i32 - k as i32 + PRECISION as i32)) / k;
        while ans >= max_number {
            ans -= max_number.clone();
        }
    }

    println!("{:0>6000}", ans.to_string_radix(2));
}
