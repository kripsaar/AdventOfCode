use crate::commons::Grid;
use std::str::FromStr;

pub fn part2() {
    let input = include_str!("../resources/input-4");
    let grid = Grid::from_str(input).unwrap();
    let result = grid.count_all_removable_rolls_recursively();
    println!("Part 2: {}", result);
}

#[cfg(test)]
mod tests {
    use crate::commons::Grid;
    use std::str::FromStr;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-4-test");
        let grid = Grid::from_str(example_input).unwrap();
        let result = grid.count_all_removable_rolls_recursively();
        assert_eq!(result, 43);
    }
}
