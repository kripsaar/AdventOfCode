#[derive(Debug, Clone, Eq, PartialEq)]
pub enum Operation {
    Addition,
    Multiplication,
}

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct Problem {
    numbers: Vec<i64>,
    operation: Operation,
}

impl Problem {
    pub fn new(numbers: Vec<i64>, operation: Operation) -> Problem {
        Problem { numbers, operation }
    }

    pub fn solve(&self) -> i64 {
        match self.operation {
            Operation::Addition => self.numbers.iter().sum::<i64>(),
            Operation::Multiplication => self.numbers.iter().product::<i64>(),
        }
    }
}

pub fn sum_of_all_solutions(problems: Vec<Problem>) -> i64 {
    problems.iter().map(Problem::solve).sum()
}

#[derive(Debug, Clone)]
pub struct ProblemBuilder {
    numbers: Vec<i64>,
    operation: Option<Operation>,
}

impl ProblemBuilder {
    pub fn new() -> Self {
        Self {
            numbers: Vec::new(),
            operation: None,
        }
    }

    pub fn add_number(&self, number: i64) -> Self {
        let mut builder = self.clone();
        builder.numbers.push(number);
        builder
    }

    pub fn with_operation(&self, operation: Operation) -> Self {
        let mut builder = self.clone();
        builder.operation = Some(operation);
        builder
    }

    pub fn build(&self) -> Result<Problem, String> {
        if self.operation.is_none() {
            return Err("No operation specified".to_string());
        }
        if self.numbers.len() < 2 {
            return Err("Fewer than 2 numbers in Problem".to_string());
        }
        Ok(Problem::new(
            self.numbers.clone(),
            self.operation.clone().unwrap(),
        ))
    }
}
