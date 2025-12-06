use crate::commons::Grid;
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-4");
    let grid = Grid::from_str(input).unwrap();
    let result = grid.count_reachable_rolls();
    println!("Part 1: {}", result);
}

#[cfg(test)]
mod tests {
    use crate::part1::Grid;
    use std::str::FromStr;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-4-test");
        let grid = Grid::from_str(example_input).unwrap();
        let result = grid.count_reachable_rolls();
        assert_eq!(result, 13);
    }
}
