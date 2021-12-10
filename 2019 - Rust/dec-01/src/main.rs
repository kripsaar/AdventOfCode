use std::fs;

fn main() {
    let filename = "input";

    let input_str = fs::read_to_string(filename)
        .expect("Something went wrong with reading the input!");

    let inputs: Vec<_> = input_str.lines()
                        .map(|s: &str| s.parse::<i32>().expect("Oh noes!"))
                        .collect();

    let mut result = 0;
    for input in inputs.iter() {
        let mut fuel: i32 = *input;
        loop {
            fuel = calculate_module_fuel(fuel);
            if fuel <= 0 {
                break;
            }
            result += fuel;
        }
    }
    println!("Result: {}", result);
}

fn calculate_module_fuel(module_mass: i32) -> i32 {
    module_mass / 3 - 2
}