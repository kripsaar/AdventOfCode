pub trait JoltageBank {
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
