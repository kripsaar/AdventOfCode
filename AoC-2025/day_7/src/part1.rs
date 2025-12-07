use std::collections::HashMap;
use std::fmt::{Display, Formatter};
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-7");
    let tachyon_manifold = TachyonManifold::from_str(input).unwrap();
    let (traversed_manifold, split_count) = tachyon_manifold.traverse_and_count_splits();
    println!("{}", traversed_manifold);
    println!("Part 1: {}", split_count);
}

#[derive(Debug, Clone)]
struct TachyonManifold {
    map: HashMap<(usize, usize), char>,
    x_size: usize,
    y_size: usize,
}

impl TachyonManifold {
    fn new(map: HashMap<(usize, usize), char>, x_size: usize, y_size: usize) -> Self {
        Self {
            map,
            x_size,
            y_size,
        }
    }

    fn traverse_and_count_splits(&self) -> (Self, usize) {
        let mut manifold = self.clone();
        let mut split_count = 0;
        for y in 0..self.y_size {
            for x in 0..self.x_size {
                match manifold.map.get(&(x, y)) {
                    Some('S') | Some('|') => {
                        let (new_manifold, was_split) = manifold.step(x, y);
                        manifold = new_manifold;
                        if was_split {
                            split_count += 1;
                        }
                    }
                    _ => continue,
                }
            }
        }
        (manifold, split_count)
    }

    /// Returns new state of the given [TachyonManifold], and true if a beam was split.
    fn step(&self, x: usize, y: usize) -> (Self, bool) {
        match self.map.get(&(x, y)) {
            Some('S') | Some('|') => {}
            _ => return (self.clone(), false),
        };
        if y + 1 == self.y_size {
            return (self.clone(), false);
        }
        let mut map = self.map.clone();
        let mut was_split = false;
        match self.map.get(&(x, y + 1)) {
            Some('^') => {
                if x > 0 {
                    map.insert((x - 1, y + 1), '|');
                }
                if x + 1 < self.x_size {
                    map.insert((x + 1, y + 1), '|');
                }
                was_split = true;
            }
            _ => {
                map.insert((x, y + 1), '|');
            }
        };
        (Self::new(map, self.x_size, self.y_size), was_split)
    }
}

impl Display for TachyonManifold {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.y_size {
            let mut line = "".to_owned();
            for x in 0..self.x_size {
                match self.map.get(&(x, y)) {
                    Some(c) => line.push(*c),
                    None => line.push('.'),
                };
            }
            writeln!(f, "{}", line)?;
        }
        Ok(())
    }
}

impl FromStr for TachyonManifold {
    type Err = ();

    fn from_str(input_str: &str) -> Result<Self, Self::Err> {
        let mut map: HashMap<(usize, usize), char> = HashMap::new();
        let y_size = input_str.trim().lines().count();
        let x_size = input_str.lines().map(|line| line.len()).max().unwrap();
        for (y, line) in input_str.trim().lines().enumerate() {
            for (x, char) in line.char_indices() {
                match char {
                    '.' => continue,
                    char => map.insert((x, y), char),
                };
            }
        }
        Ok(Self::new(map, x_size, y_size))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_and_print() {
        let example_input = include_str!("../resources/input-7-test");
        let tachyon_manifold = TachyonManifold::from_str(example_input).unwrap();
        let printed = format!("{}", tachyon_manifold);
        println!("{}", printed);
        assert_eq!(printed, example_input.replace("\r\n", "\n"));
    }

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-7-test");
        let tachyon_manifold = TachyonManifold::from_str(example_input).unwrap();
        let (traversed_manifold, split_count) = tachyon_manifold.traverse_and_count_splits();
        println!("{}", traversed_manifold);
        assert_eq!(split_count, 21);
    }
}
