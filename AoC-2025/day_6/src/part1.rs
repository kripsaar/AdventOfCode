pub fn part1() {
    let input = include_str!("../resources/input-6");
    let problems = parse_input(input);
    let result = sum_of_all_solutions(problems);
    println!("Part 1: {}", result);
}

#[derive(Debug, Clone, Eq, PartialEq)]
enum Operation {
    Addition,
    Multiplication,
}

#[derive(Debug, Clone, Eq, PartialEq)]
struct Problem {
    numbers: Vec<i64>,
    operation: Operation,
}

impl Problem {
    fn solve(&self) -> i64 {
        match self.operation {
            Operation::Addition => self.numbers.iter().fold(0, |left, right| left + right),
            Operation::Multiplication => self.numbers.iter().fold(1, |left, right| left * right),
        }
    }
}

fn sum_of_all_solutions(problems: Vec<Problem>) -> i64 {
    problems.iter().map(Problem::solve).sum()
}

#[derive(Debug, Clone)]
struct ProblemBuilder {
    numbers: Vec<i64>,
    operation: Option<Operation>,
}

impl ProblemBuilder {
    fn new() -> Self {
        Self {
            numbers: Vec::new(),
            operation: None,
        }
    }

    fn add_number(&self, number: i64) -> Self {
        let mut builder = self.clone();
        builder.numbers.push(number);
        builder
    }

    fn with_operation(&self, operation: Operation) -> Self {
        let mut builder = self.clone();
        builder.operation = Some(operation);
        builder
    }

    fn build(&self) -> Result<Problem, String> {
        if self.operation.is_none() {
            return Err("No operation specified".to_string());
        }
        if self.numbers.len() < 2 {
            return Err("Fewer than 2 numbers in Problem".to_string());
        }
        Ok(Problem {
            numbers: self.numbers.clone(),
            operation: self.operation.clone().unwrap(),
        })
    }
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
