use crate::commons::{IdRange, InvalidId};

pub fn part1() {
    let input_2 = include_str!("../resources/input-2");
    let result = IdRange::<InvalidIdPart1>::read_and_evaluate_ids(input_2);
    println!("Part 1: {}", result);
}

struct InvalidIdPart1 {
    id: u64,
}

impl InvalidId for InvalidIdPart1 {
    fn new(id: u64) -> Self {
        InvalidIdPart1 { id }
    }

    fn get_id(&self) -> u64 {
        self.id
    }

    fn next_invalid_id(number: u64) -> Self {
        let number_string = number.to_string();
        let (left_str, right_str) = number_string.split_at(number_string.len() / 2);
        let mut left = left_str.parse().unwrap_or(0);
        let right = right_str.parse().unwrap_or(0);
        if left <= right {
            if left_str.len() < right_str.len() {
                left = format!("1{}", "0".repeat(right_str.len() - 1))
                    .parse()
                    .unwrap();
            } else {
                left += 1;
            }
        }
        let id = format!("{}{}", left, left).parse().unwrap();
        Self { id }
    }

    fn next(&self) -> Self {
        Self::next_invalid_id(self.id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::str::FromStr;

    #[test]
    fn test_next_invalid_id() {
        assert_eq!(InvalidIdPart1::next_invalid_id(0).id, 11);
        assert_eq!(InvalidIdPart1::next_invalid_id(1).id, 11);
        assert_eq!(InvalidIdPart1::next_invalid_id(10).id, 11);
        assert_eq!(InvalidIdPart1::next_invalid_id(11).id, 22);
        assert_eq!(InvalidIdPart1::next_invalid_id(12).id, 22);
        assert_eq!(InvalidIdPart1::next_invalid_id(998).id, 1010);
        assert_eq!(InvalidIdPart1::next_invalid_id(899).id, 1010);
        assert_eq!(InvalidIdPart1::next_invalid_id(1698522).id, 10001000);
        assert_eq!(InvalidIdPart1::next_invalid_id(1188511880).id, 1188511885);
    }

    #[test]
    fn test_range_sums() {
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("11-22")
                .unwrap()
                .add_all_invalid_ids(),
            33
        );
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("95-115")
                .unwrap()
                .add_all_invalid_ids(),
            99
        );
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("998-1012")
                .unwrap()
                .add_all_invalid_ids(),
            1010
        );
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("1188511880-1188511890")
                .unwrap()
                .add_all_invalid_ids(),
            1188511885
        );
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("222220-222224")
                .unwrap()
                .add_all_invalid_ids(),
            222222
        );
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("1698522-1698528")
                .unwrap()
                .add_all_invalid_ids(),
            0
        );
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("446443-446449")
                .unwrap()
                .add_all_invalid_ids(),
            446446
        );
        assert_eq!(
            IdRange::<InvalidIdPart1>::from_str("38593856-38593862")
                .unwrap()
                .add_all_invalid_ids(),
            38593859
        );
    }

    #[test]
    fn example_input() {
        let example = include_str!("../resources/input-2-test");
        let result = IdRange::<InvalidIdPart1>::read_and_evaluate_ids(example);
        assert_eq!(result, 1227775554);
    }
}
