use crate::commons::{parse_batteries_from_line, JoltageBank};
use std::cmp::Ordering;
use std::num::ParseIntError;
use std::str::FromStr;

pub fn part1() {
    let input_3 = include_str!("../resources/input-3");
    let joltage_banks = parse_input(input_3);
    let total_joltage = calculate_total_joltage(joltage_banks);
    println!("Part 1: {}", total_joltage);
}

fn calculate_total_joltage<I>(joltage_banks: Vec<I>) -> u64
where
    I: JoltageBank,
{
    joltage_banks
        .iter()
        .map(|joltage_bank| joltage_bank.calculate_joltage())
        .sum()
}

struct JoltageBankPart1 {
    batteries: Vec<u8>,
}

impl JoltageBank for JoltageBankPart1 {
    fn new(batteries: Vec<u8>) -> Self {
        JoltageBankPart1 { batteries }
    }

    fn calculate_joltage(&self) -> u64 {
        let (left_idx, left) = self.batteries[..(self.batteries.len() - 1)]
            .iter()
            .enumerate()
            .max_by(|(left_idx, left_value), (right_idx, right_value)| {
                match left_value.cmp(right_value) {
                    Ordering::Greater => Ordering::Greater,
                    Ordering::Less => Ordering::Less,
                    Ordering::Equal => match left_idx.cmp(right_idx) {
                        Ordering::Equal => Ordering::Equal,
                        Ordering::Greater => Ordering::Less,
                        Ordering::Less => Ordering::Greater,
                    },
                }
            })
            .unwrap();
        let right = self.batteries[(left_idx + 1)..].iter().max().unwrap();
        format!("{}{}", left, right).parse::<u64>().unwrap()
    }
}

impl FromStr for JoltageBankPart1 {
    type Err = ParseIntError;
    fn from_str(str: &str) -> Result<Self, Self::Err> {
        Ok(JoltageBankPart1::new(parse_batteries_from_line(str)))
    }
}

fn parse_input(input: &str) -> Vec<JoltageBankPart1> {
    input
        .trim()
        .lines()
        .map(JoltageBankPart1::from_str)
        .flatten()
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_joltage_calculation() {
        let battery = JoltageBankPart1::from_str("987654321111111").unwrap();
        assert_eq!(battery.calculate_joltage(), 98);
        let battery = JoltageBankPart1::from_str("811111111111119").unwrap();
        assert_eq!(battery.calculate_joltage(), 89);
        let battery = JoltageBankPart1::from_str("234234234234278").unwrap();
        assert_eq!(battery.calculate_joltage(), 78);
        let battery = JoltageBankPart1::from_str("818181911112111").unwrap();
        assert_eq!(battery.calculate_joltage(), 92);
        let battery = JoltageBankPart1::from_str("111111111111119").unwrap();
        assert_eq!(battery.calculate_joltage(), 19);
        let battery = JoltageBankPart1::from_str("111111111111199").unwrap();
        assert_eq!(battery.calculate_joltage(), 99);
        let battery = JoltageBankPart1::from_str("111111111111899").unwrap();
        assert_eq!(battery.calculate_joltage(), 99);
        let battery = JoltageBankPart1::from_str("111111111111897").unwrap();
        assert_eq!(battery.calculate_joltage(), 97);
        let battery = JoltageBankPart1::from_str("111199971111111").unwrap();
        assert_eq!(battery.calculate_joltage(), 99);
    }

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-3-test");
        let joltage_banks = parse_input(example_input);
        let total_joltage = calculate_total_joltage(joltage_banks);
        assert_eq!(total_joltage, 357);
    }
}
