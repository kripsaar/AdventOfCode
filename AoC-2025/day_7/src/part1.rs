use crate::commons::TachyonManifold;
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-7");
    let tachyon_manifold = TachyonManifold::from_str(input).unwrap();
    let (traversed_manifold, split_count) = tachyon_manifold.traverse_and_count_splits();
    println!("{}", traversed_manifold);
    println!("Part 1: {}", split_count);
}

impl TachyonManifold {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-7-test");
        let tachyon_manifold = TachyonManifold::from_str(example_input).unwrap();
        let (traversed_manifold, split_count) = tachyon_manifold.traverse_and_count_splits();
        println!("{}", traversed_manifold);
        assert_eq!(split_count, 21);
    }
}
