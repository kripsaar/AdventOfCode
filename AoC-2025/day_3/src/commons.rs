use std::cmp::Ordering;
use std::str::FromStr;

pub trait JoltageBank: FromStr {
    fn new(batteries: Vec<u8>) -> Self;
    fn calculate_joltage(&self) -> u64;
}

pub fn parse_batteries_from_line(line: &str) -> Vec<u8> {
    line.trim()
        .chars()
        .map(|c| c.to_string().parse())
        .flatten()
        .collect()
}

pub fn calculate_total_joltage<I>(joltage_banks: Vec<I>) -> u64
where
    I: JoltageBank,
{
    joltage_banks
        .iter()
        .map(|joltage_bank| joltage_bank.calculate_joltage())
        .sum()
}

pub fn parse_input<J>(input: &str) -> Vec<J>
where
    J: JoltageBank,
{
    input.trim().lines().map(J::from_str).flatten().collect()
}

pub fn calculate_joltage(batteries: &[u8], remaining_battery_count: usize) -> u64 {
    let remaining_battery_count = remaining_battery_count - 1;
    let (left_idx, left) = batteries[..(batteries.len() - remaining_battery_count)]
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
    if remaining_battery_count < 1 {
        return left.to_owned() as u64;
    }
    let right = calculate_joltage(&batteries[(left_idx + 1)..], remaining_battery_count);
    format!("{}{}", left, right).parse::<u64>().unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_joltage() {
        let batteries = parse_batteries_from_line("987654321111111");
        assert_eq!(calculate_joltage(&batteries, 2), 98);
        assert_eq!(calculate_joltage(&batteries, 12), 987654321111);
    }
}
