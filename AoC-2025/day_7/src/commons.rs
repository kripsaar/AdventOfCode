use std::collections::HashMap;
use std::fmt::{Display, Formatter};
use std::str::FromStr;

#[derive(Debug, Clone)]
pub struct TachyonManifold {
    map: HashMap<(usize, usize), String>,
    x_size: usize,
    y_size: usize,
}

impl TachyonManifold {
    pub fn new(map: HashMap<(usize, usize), String>, x_size: usize, y_size: usize) -> Self {
        Self {
            map,
            x_size,
            y_size,
        }
    }

    pub fn map(&self) -> &HashMap<(usize, usize), String> {
        &self.map
    }

    pub fn x_size(&self) -> usize {
        self.x_size
    }

    pub fn y_size(&self) -> usize {
        self.y_size
    }

    pub fn traverse_and_count_splits(&self) -> (Self, usize) {
        let mut manifold = self.clone();
        let mut split_count = 0;
        for y in 0..self.y_size() {
            for x in 0..self.x_size() {
                match manifold.map().get(&(x, y)) {
                    Some(string) => {
                        if string == "^" {
                            continue;
                        }
                        let (new_manifold, was_split) = manifold.step(x, y);
                        manifold = new_manifold;
                        if was_split {
                            split_count += 1;
                        }
                    }
                    None => continue,
                }
            }
        }
        (manifold, split_count)
    }

    /// Returns new state of the given [TachyonManifold], and true if a beam was split.
    pub fn step(&self, x: usize, y: usize) -> (Self, bool) {
        if y + 1 == self.y_size() {
            return (self.clone(), false);
        }
        match self.map().get(&(x, y)) {
            Some(string) => {
                if string == "^" {
                    return (self.clone(), false);
                }
                let current_value = if string == "S" {
                    1
                } else {
                    string.parse().unwrap()
                };
                let mut map = self.map().clone();
                let was_split = Self::insert_into_map(&mut map, x, y + 1, current_value);
                (Self::new(map, self.x_size(), self.y_size()), was_split)
            }
            None => (self.clone(), false),
        }
    }

    pub fn insert_into_map(
        map: &mut HashMap<(usize, usize), String>,
        x: usize,
        y: usize,
        current_value: usize,
    ) -> bool {
        match map.get(&(x, y)) {
            Some(string) => {
                if string == "^" {
                    Self::insert_into_map(map, x - 1, y, current_value);
                    Self::insert_into_map(map, x + 1, y, current_value);
                    return true;
                }
                if let Ok(number) = string.parse::<usize>() {
                    map.insert((x, y), (number + current_value).to_string());
                }
            }
            None => {
                map.insert((x, y), format!("{}", current_value).to_string());
            }
        }
        false
    }

    pub fn sum_of_timelines(&self) -> usize {
        let mut sum = 0;
        let y = self.y_size() - 1;
        for x in 0..self.x_size() {
            if let Some(string) = self.map().get(&(x, y)) {
                if let Ok(number) = string.parse::<usize>() {
                    sum += number;
                }
            }
        }
        sum
    }
}

impl Display for TachyonManifold {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.y_size {
            let mut line = "".to_owned();
            for x in 0..self.x_size {
                match self.map.get(&(x, y)) {
                    Some(string) => match string.as_str() {
                        "S" | "^" => line.push_str(string),
                        _ => line.push('|'),
                    },
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
        let mut map: HashMap<(usize, usize), String> = HashMap::new();
        let y_size = input_str.trim().lines().count();
        let x_size = input_str.lines().map(|line| line.len()).max().unwrap();
        for (y, line) in input_str.trim().lines().enumerate() {
            for (x, char) in line.char_indices() {
                match char {
                    '.' => continue,
                    char => map.insert((x, y), format!("{}", char)),
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
}
