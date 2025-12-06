use crate::commons::Rotation::{Left, Right};

pub struct Safe {
    pub current_position: u32,
    pub position_count: u32,
    pub zero_counter: u32,
}

impl Default for Safe {
    fn default() -> Self {
        Self::new()
    }
}

impl Safe {
    pub fn new() -> Safe {
        Safe {
            zero_counter: 0,
            current_position: 50,
            position_count: 100,
        }
    }
}

pub fn parse_input(input: &str) -> Vec<Rotation> {
    input.lines().filter_map(parse_line).collect()
}

pub enum Rotation {
    Left(u32),
    Right(u32),
}

pub fn parse_line(input_line: &str) -> Option<Rotation> {
    let (first, second) = input_line.split_at(1);
    match first {
        "L" => Some(Left(second.parse().unwrap())),
        "R" => Some(Right(second.parse().unwrap())),
        _ => None,
    }
}

#[derive(Eq, PartialEq, Debug)]
pub struct SubtractedResult {
    pub result: u32,
    pub zero_passes: u32,
}

pub fn sub_with_wrap(left: u32, right: u32, limit: u32) -> SubtractedResult {
    let starter_zero = match left {
        0 => 1,
        _ => 0,
    };
    let left = left as i32;
    let right = right as i32;
    let limit = limit as i32;
    let zero_passes = (limit - (left - right)) / limit;
    SubtractedResult {
        result: ((left - right + (zero_passes * limit)) % limit) as u32,
        zero_passes: (zero_passes - starter_zero) as u32,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sub_with_wrap() {
        assert_eq!(
            sub_with_wrap(50, 5, 100),
            SubtractedResult {
                result: 45,
                zero_passes: 0
            }
        );
        assert_eq!(
            sub_with_wrap(50, 65, 100),
            SubtractedResult {
                result: 85,
                zero_passes: 1
            }
        );
        assert_eq!(
            sub_with_wrap(50, 465, 100),
            SubtractedResult {
                result: 85,
                zero_passes: 5
            }
        );
        assert_eq!(
            sub_with_wrap(50, 725, 100),
            SubtractedResult {
                result: 25,
                zero_passes: 7
            }
        );
        assert_eq!(
            sub_with_wrap(50, 950, 100),
            SubtractedResult {
                result: 0,
                zero_passes: 10
            }
        );
        assert_eq!(
            sub_with_wrap(0, 1, 100),
            SubtractedResult {
                result: 99,
                zero_passes: 0
            }
        );
    }
}
