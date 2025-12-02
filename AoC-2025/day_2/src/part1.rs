use std::num::ParseIntError;
use std::str::FromStr;

pub fn part1() {
    let input_1 = include_str!("../resources/input-2");
    let result = read_and_evaluate_ids(input_1);
    println!("Part 1: {}", result);
}

fn read_and_evaluate_ids(input_str: &str) -> u64 {
    let id_ranges = parse_input(input_str);
    id_ranges
        .iter()
        .map(|id_range| id_range.add_all_invalid_ids())
        .sum()
}

fn parse_input(input_str: &str) -> Vec<IdRange> {
    input_str
        .trim()
        .split(",")
        .map(IdRange::from_str)
        .flatten()
        .collect()
}

struct IdRange {
    start: u64,
    end: u64,
}

impl FromStr for IdRange {
    type Err = ParseIntError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let split: Vec<u64> = s
            .split("-")
            .map(|str| str.parse::<u64>().unwrap())
            .collect();
        Ok(IdRange::new(split[0], split[1]))
    }
}

impl IdRange {
    fn new(start: u64, end: u64) -> IdRange {
        IdRange { start, end }
    }

    fn add_all_invalid_ids(&self) -> u64 {
        let mut result = 0;
        let mut invalid_id = InvalidId { id: self.start - 1 };
        loop {
            invalid_id = invalid_id.next();
            if invalid_id.id > self.end {
                break;
            }
            result += invalid_id.id
        }

        result
    }
}

struct InvalidId {
    id: u64,
}

impl InvalidId {
    fn next_invalid_id(number: u64) -> InvalidId {
        let number_string = number.to_string();
        let (left_str, right_str) = number_string.split_at(number_string.len() / 2);
        let mut left = left_str.parse().unwrap_or_else(|_| 0);
        let right = right_str.parse().unwrap_or_else(|_| 0);
        if left <= right {
            if left_str.len() < right_str.len() {
                left = format!("1{}", "0".repeat(right_str.len() - 1))
                    .parse()
                    .unwrap();
            } else {
                left = left + 1;
            }
        }
        let id = format!("{}{}", left, left).parse().unwrap();
        InvalidId { id }
    }

    fn next(&self) -> InvalidId {
        Self::next_invalid_id(self.id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_next_invalid_id() {
        assert_eq!(InvalidId::next_invalid_id(0).id, 11);
        assert_eq!(InvalidId::next_invalid_id(1).id, 11);
        assert_eq!(InvalidId::next_invalid_id(10).id, 11);
        assert_eq!(InvalidId::next_invalid_id(11).id, 22);
        assert_eq!(InvalidId::next_invalid_id(12).id, 22);
        assert_eq!(InvalidId::next_invalid_id(998).id, 1010);
        assert_eq!(InvalidId::next_invalid_id(899).id, 1010);
        assert_eq!(InvalidId::next_invalid_id(1698522).id, 10001000);
        assert_eq!(InvalidId::next_invalid_id(1188511880).id, 1188511885);
    }

    #[test]
    fn test_range_sums() {
        assert_eq!(
            IdRange::from_str("11-22").unwrap().add_all_invalid_ids(),
            33
        );
        assert_eq!(
            IdRange::from_str("95-115").unwrap().add_all_invalid_ids(),
            99
        );
        assert_eq!(
            IdRange::from_str("998-1012").unwrap().add_all_invalid_ids(),
            1010
        );
        assert_eq!(
            IdRange::from_str("1188511880-1188511890")
                .unwrap()
                .add_all_invalid_ids(),
            1188511885
        );
        assert_eq!(
            IdRange::from_str("222220-222224")
                .unwrap()
                .add_all_invalid_ids(),
            222222
        );
        assert_eq!(
            IdRange::from_str("1698522-1698528")
                .unwrap()
                .add_all_invalid_ids(),
            0
        );
        assert_eq!(
            IdRange::from_str("446443-446449")
                .unwrap()
                .add_all_invalid_ids(),
            446446
        );
        assert_eq!(
            IdRange::from_str("38593856-38593862")
                .unwrap()
                .add_all_invalid_ids(),
            38593859
        );
    }

    #[test]
    fn example_input() {
        let example = include_str!("../resources/input-2-test");
        let result = read_and_evaluate_ids(example);
        assert_eq!(result, 1227775554);
    }
}
