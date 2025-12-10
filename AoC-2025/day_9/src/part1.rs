use crate::commons::Grid;
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-9");
    let grid = Grid::from_str(input).unwrap();
    let rectangles = grid.generate_unchecked_rectangles_sorted();
    let largest_rectangle = rectangles.last().unwrap();
    println!("Part 1: {}", largest_rectangle.area());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-9-test");
        let grid = Grid::from_str(example_input).unwrap();
        let rectangles = grid.generate_unchecked_rectangles_sorted();
        let largest_rectangle = rectangles.last().unwrap();
        assert_eq!(largest_rectangle.area(), 50);
    }
}
