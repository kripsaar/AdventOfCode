use crate::commons::{parse_input, sub_with_wrap, Rotation, Safe};
use crate::part2::Rotation::{Left, Right};

pub fn part2() {
    let input = include_str!("../resources/input-1");
    let result = play(input);
    println!("Part 2: {}", result);
}

fn play(input: &str) -> u32 {
    let rotations = parse_input(input);
    let mut safe = Safe::new();
    for rotation in rotations {
        safe = safe.move_dial_part2(rotation);
    }
    safe.zero_counter
}

impl Safe {
    fn move_dial_part2(&self, rotation: Rotation) -> Safe {
        match rotation {
            Left(distance) => self.move_left(distance),
            Right(distance) => self.move_right(distance),
        }
    }

    fn move_left(&self, distance: u32) -> Safe {
        let result = sub_with_wrap(self.current_position, distance, self.position_count);
        Safe {
            current_position: result.result,
            zero_counter: self.zero_counter + result.zero_passes,
            position_count: self.position_count,
        }
    }

    fn move_right(&self, distance: u32) -> Safe {
        let zero_passes = (self.current_position + distance) / self.position_count;
        let zero_counter = self.zero_counter + zero_passes;
        let current_position = (self.current_position + distance) % self.position_count;
        Safe {
            current_position,
            zero_counter,
            position_count: self.position_count,
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
        assert_eq!(result, 6);
    }

    #[test]
    fn real_input() {
        let input = include_str!("../resources/input-1");
        let result = play(input);
        println!("{}", result);
    }
}
