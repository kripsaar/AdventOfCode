use crate::commons::{
    calculate_joltage, calculate_total_joltage, parse_batteries_from_line, parse_input, JoltageBank,
};
use std::str::FromStr;

pub fn part2() {
    let input_3 = include_str!("../resources/input-3");
    let joltage_banks = parse_input::<JoltageBankPart2>(input_3);
    let total_joltage = calculate_total_joltage(joltage_banks);
    println!("Part 2: {}", total_joltage);
}

struct JoltageBankPart2 {
    batteries: Vec<u8>,
}

impl FromStr for JoltageBankPart2 {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self::new(parse_batteries_from_line(s)))
    }
}

impl JoltageBank for JoltageBankPart2 {
    fn new(batteries: Vec<u8>) -> Self {
        JoltageBankPart2 { batteries }
    }

    fn calculate_joltage(&self) -> u64 {
        calculate_joltage(&self.batteries, 12)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::commons::{calculate_total_joltage, parse_input};

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-3-test");
        let joltage_banks = parse_input::<JoltageBankPart2>(example_input);
        let total_joltage = calculate_total_joltage(joltage_banks);
        assert_eq!(total_joltage, 3121910778619);
    }
}
