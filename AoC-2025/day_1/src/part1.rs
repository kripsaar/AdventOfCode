use crate::commons::Rotation::{Left, Right};
use crate::commons::{parse_input, sub_with_wrap, Rotation, Safe};

pub fn part1() {
    let input = include_str!("../resources/input-1");
    let result = play(input);
    println!("Part 1: {}", result);
}

fn play(input: &str) -> u32 {
    let rotations = parse_input(input);
    let mut safe = Safe::new();
    for rotation in rotations {
        safe = safe.move_dial(rotation);
    }
    safe.zero_counter
}

impl Safe {
    fn move_dial(&self, rotation: Rotation) -> Safe {
        let current_position = match rotation {
            Left(distance) => {
                sub_with_wrap(self.current_position, distance, self.position_count).result
            }
            Right(distance) => (self.current_position + distance) % self.position_count,
        };
        let zero_counter = match current_position {
            0 => self.zero_counter + 1,
            _ => self.zero_counter,
        };
        if current_position >= self.position_count {
            println!("Out of bounds!");
        }
        Safe {
            current_position,
            position_count: self.position_count,
            zero_counter,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_input() {
        let example = include_str!("../resources/input-1-test");
        let result = play(example);
        assert_eq!(result, 3);
    }

    #[test]
    fn real_input() {
        let input = include_str!("../resources/input-1");
        let result = play(input);
        println!("{}", result);
    }
}
