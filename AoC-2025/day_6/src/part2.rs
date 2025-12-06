use crate::commons::{sum_of_all_solutions, Operation, Problem, ProblemBuilder};

pub fn part2() {
    let input = include_str!("../resources/input-6");
    let problems = parse_input(input);
    let result = sum_of_all_solutions(problems);
    println!("Part 2: {}", result);
}

fn parse_input(input: &str) -> Vec<Problem> {
    let mut problems = Vec::<Problem>::new();
    let mut index = 0;
    let limit = input.lines().map(|line| line.len()).max().unwrap();
    let mut builder = ProblemBuilder::new();
    while index < limit {
        let mut column = "".to_owned();
        for line in input.lines() {
            match line.chars().nth(index) {
                Some(char) => column.push(char),
                None => continue,
            }
        }
        if column.trim().is_empty() {
            problems.push(builder.build().unwrap());
            builder = ProblemBuilder::new();
            index += 1;
            continue;
        }
        if column.contains("+") {
            builder = builder.with_operation(Operation::Addition);
            column = column.replace("+", "");
        }
        if column.contains("*") {
            builder = builder.with_operation(Operation::Multiplication);
            column = column.replace("*", "");
        }
        builder = builder.add_number(column.trim().parse::<i64>().unwrap());

        index += 1;
    }
    if let Ok(problem) = builder.build() {
        problems.push(problem);
    }
    problems
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
        assert_eq!(result, 3263827);
    }
}
