use crate::commons::{IdRange, InvalidId};

pub fn part2() {
    let input_2 = include_str!("../resources/input-2");
    let result = IdRange::<InvalidIdPart2>::read_and_evaluate_ids(input_2);
    println!("Part 2: {}", result);
}

struct InvalidIdPart2 {
    id: u64,
}

impl InvalidId for InvalidIdPart2 {
    fn new(id: u64) -> Self {
        InvalidIdPart2 { id }
    }

    fn get_id(&self) -> u64 {
        self.id
    }

    fn next_invalid_id(number: u64) -> Self {
        let number_string = number.to_string();
        let mut larger_invalid_ids = Vec::<u64>::new();
        let mut repeat = number_string.len() + 1;
        let mut i = 1;
        loop {
            let id_string = format!("{}", i).repeat(repeat);
            if id_string.len() < number_string.len() {
                i *= 10;
                continue;
            }
            if id_string.len() > number_string.len() + 1 {
                repeat -= 1;
                i /= 10;
                if repeat < 2 {
                    break;
                }
                continue;
            }
            let id = match id_string.parse() {
                Ok(id) => id,
                Err(_) => panic!(),
            };
            if id > number {
                larger_invalid_ids.push(id);
            }
            i += 1;
        }
        let next_id = match larger_invalid_ids.iter().min() {
            Some(id) => *id,
            None => panic!(),
        };
        InvalidIdPart2::new(next_id)
    }

    fn next(&self) -> Self {
        Self::next_invalid_id(self.id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::commons::IdRange;
    use std::str::FromStr;

    #[test]
    fn test_next_invalid_id() {
        assert_eq!(InvalidIdPart2::next_invalid_id(0).id, 11);
        assert_eq!(InvalidIdPart2::next_invalid_id(1).id, 11);
        assert_eq!(InvalidIdPart2::next_invalid_id(10).id, 11);
        assert_eq!(InvalidIdPart2::next_invalid_id(11).id, 22);
        assert_eq!(InvalidIdPart2::next_invalid_id(12).id, 22);
        assert_eq!(InvalidIdPart2::next_invalid_id(99).id, 111);
        assert_eq!(InvalidIdPart2::next_invalid_id(101).id, 111);
        assert_eq!(InvalidIdPart2::next_invalid_id(998).id, 999);
        assert_eq!(InvalidIdPart2::next_invalid_id(899).id, 999);
        assert_eq!(InvalidIdPart2::next_invalid_id(999).id, 1010);
        assert_eq!(InvalidIdPart2::next_invalid_id(1000).id, 1010);
        assert_eq!(InvalidIdPart2::next_invalid_id(1010).id, 1111);
        assert_eq!(InvalidIdPart2::next_invalid_id(9999).id, 11111);
        assert_eq!(InvalidIdPart2::next_invalid_id(123123122).id, 123123123);
        assert_eq!(InvalidIdPart2::next_invalid_id(1212121211).id, 1212121212);
        assert_eq!(InvalidIdPart2::next_invalid_id(1111110).id, 1111111);
        assert_eq!(InvalidIdPart2::next_invalid_id(1698522).id, 2222222);
        assert_eq!(InvalidIdPart2::next_invalid_id(1188511880).id, 1188511885);
    }

    #[test]
    fn test_range_sums() {
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("11-22")
                .unwrap()
                .add_all_invalid_ids(),
            33
        );
        let res = IdRange::<InvalidIdPart2>::from_str("95-115")
            .unwrap()
            .add_all_invalid_ids();
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("95-115")
                .unwrap()
                .add_all_invalid_ids(),
            99 + 111
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("998-1012")
                .unwrap()
                .add_all_invalid_ids(),
            999 + 1010
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("1188511880-1188511890")
                .unwrap()
                .add_all_invalid_ids(),
            1188511885
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("222220-222224")
                .unwrap()
                .add_all_invalid_ids(),
            222222
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("1698522-1698528")
                .unwrap()
                .add_all_invalid_ids(),
            0
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("446443-446449")
                .unwrap()
                .add_all_invalid_ids(),
            446446
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("38593856-38593862")
                .unwrap()
                .add_all_invalid_ids(),
            38593859
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("824824821-824824827")
                .unwrap()
                .add_all_invalid_ids(),
            824824824
        );
        assert_eq!(
            IdRange::<InvalidIdPart2>::from_str("2121212118-2121212124")
                .unwrap()
                .add_all_invalid_ids(),
            2121212121
        );
    }

    #[test]
    fn example_input() {
        let example = include_str!("../resources/input-2-test");
        let result = IdRange::<InvalidIdPart2>::read_and_evaluate_ids(example);
        assert_eq!(result, 4174379265);
    }
}
