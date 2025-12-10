use itertools::Itertools;
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-9");
    let grid = Grid::from_str(input).unwrap();
    let rectangles = grid.generate_rectangles_sorted();
    let largest_rectangle = rectangles.last().unwrap();
    println!("Part 1: {}", largest_rectangle.area());
}

#[derive(Debug, Eq, PartialEq, Clone)]
struct Tile {
    x: usize,
    y: usize,
}

impl Tile {
    fn new(x: usize, y: usize) -> Tile {
        Tile { x, y }
    }
}

#[derive(Debug, Eq, PartialEq, Clone)]
struct Rectangle {
    corners: [Tile; 2],
    area: usize,
}

impl Rectangle {
    fn new(corners: [Tile; 2]) -> Self {
        let size =
            (&corners[0].x.abs_diff(corners[1].x) + 1) * (&corners[0].y.abs_diff(corners[1].y) + 1);
        Self {
            corners,
            area: size,
        }
    }

    fn area(&self) -> usize {
        self.area
    }
}

#[derive(Debug)]
struct Grid {
    tiles: Vec<Tile>,
}

impl FromStr for Grid {
    type Err = ();
    fn from_str(input: &str) -> Result<Self, Self::Err> {
        let tiles: Vec<Tile> = input
            .trim()
            .lines()
            .map(|line| line.split(',').collect())
            .map(|split: Vec<&str>| Tile::new(split[0].parse().unwrap(), split[1].parse().unwrap()))
            .collect();
        Ok(Self { tiles })
    }
}

impl Grid {
    pub fn generate_rectangles_sorted(&self) -> Vec<Rectangle> {
        self.tiles
            .iter()
            .cloned()
            .combinations(2)
            .map(|combination| Rectangle::new(combination.try_into().unwrap()))
            .sorted_by_key(Rectangle::area)
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-9-test");
        let grid = Grid::from_str(example_input).unwrap();
        let rectangles = grid.generate_rectangles_sorted();
        let largest_rectangle = rectangles.last().unwrap();
        assert_eq!(largest_rectangle.area(), 50);
    }
}
