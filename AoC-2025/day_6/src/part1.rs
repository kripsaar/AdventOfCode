use crate::commons::{sum_of_all_solutions, Operation, Problem, ProblemBuilder};

pub fn part1() {
    let input = include_str!("../resources/input-6");
    let problems = parse_input(input);
    let result = sum_of_all_solutions(problems);
    println!("Part 1: {}", result);
}

fn parse_input(input: &str) -> Vec<Problem> {
    let mut problem_builders = Vec::<ProblemBuilder>::new();
    for line in input.lines() {
        let components: Vec<&str> = line.trim().split_whitespace().collect();
        if problem_builders.is_empty() {
            problem_builders.extend(vec![ProblemBuilder::new(); components.len()]);
        }
        components
            .iter()
            .enumerate()
            .for_each(|(index, component)| {
                let builder = &problem_builders[index];
                match *component {
                    "+" => problem_builders[index] = builder.with_operation(Operation::Addition),
                    "*" => {
                        problem_builders[index] = builder.with_operation(Operation::Multiplication)
                    }
                    component => {
                        problem_builders[index] = builder.add_number(component.parse().unwrap())
                    }
                }
            })
    }
    problem_builders
        .iter()
        .map(|builder| builder.build().unwrap())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parsing() {
        let example_input = include_str!("../resources/input-6-test");
        let problems = parse_input(example_input);
        assert_eq!(problems.len(), 4);
    }

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-6-test");
        let problems = parse_input(example_input);
        let result = sum_of_all_solutions(problems);
        assert_eq!(result, 4277556);
    }
}
