use crate::commons::TachyonManifold;
use std::str::FromStr;

pub fn part2() {
    let input = include_str!("../resources/input-7");
    let tachyon_manifold = TachyonManifold::from_str(input).unwrap();
    let (traversed_manifold, _split_count) = tachyon_manifold.traverse_and_count_splits();
    let result = traversed_manifold.sum_of_timelines();
    println!("Part 2: {}", result);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-7-test");
        let tachyon_manifold = TachyonManifold::from_str(example_input).unwrap();
        let (traversed_manifold, _split_count) = tachyon_manifold.traverse_and_count_splits();
        let result = traversed_manifold.sum_of_timelines();
        assert_eq!(result, 40);
    }
}
