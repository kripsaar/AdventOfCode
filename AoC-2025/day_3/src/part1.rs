use crate::commons::{
    calculate_joltage, calculate_total_joltage, parse_batteries_from_line, parse_input, JoltageBank,
};
use std::str::FromStr;

pub fn part1() {
    let input_3 = include_str!("../resources/input-3");
    let joltage_banks = parse_input::<JoltageBankPart1>(input_3);
    let total_joltage = calculate_total_joltage(joltage_banks);
    println!("Part 1: {}", total_joltage);
}

struct JoltageBankPart1 {
    batteries: Vec<u8>,
}

impl FromStr for JoltageBankPart1 {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self::new(parse_batteries_from_line(s)))
    }
}

impl JoltageBank for JoltageBankPart1 {
    fn new(batteries: Vec<u8>) -> Self {
        JoltageBankPart1 { batteries }
    }

    fn calculate_joltage(&self) -> u64 {
        calculate_joltage(&self.batteries, 2)
    }
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
        let joltage_banks = parse_input::<JoltageBankPart1>(example_input);
        let total_joltage = calculate_total_joltage(joltage_banks);
        assert_eq!(total_joltage, 357);
    }
}
