use crate::commons::MachineDescription;
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-10");
    let machines: Vec<MachineDescription> = input
        .trim()
        .lines()
        .flat_map(MachineDescription::from_str)
        .collect();
    let init_steps: Vec<usize> = machines
        .iter()
        .map(MachineDescription::initialize_indicator_lights)
        .collect();
    let result: usize = init_steps.iter().sum();
    println!("Part 1: {}", result);
}

#[cfg(test)]
mod tests {
    use crate::commons::MachineDescription;
    use std::str::FromStr;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-10-test");
        let machines: Vec<MachineDescription> = example_input
            .trim()
            .lines()
            .flat_map(MachineDescription::from_str)
            .collect();
        let init_steps: Vec<usize> = machines
            .iter()
            .map(MachineDescription::initialize_indicator_lights)
            .collect();
        let result: usize = init_steps.iter().sum();
        assert_eq!(result, 7);
    }
}
