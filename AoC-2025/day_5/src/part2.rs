use crate::commons::FreshnessDatabase;
use std::str::FromStr;

pub fn part2() {
    let input = include_str!("../resources/input-5");
    let freshness_database = FreshnessDatabase::from_str(input).unwrap();
    let result = freshness_database.count_all_possible_fresh_ingredients();
    println!("Part 2: {}", result);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-5-test");
        let freshness_database = FreshnessDatabase::from_str(example_input).unwrap();
        let result = freshness_database.count_all_possible_fresh_ingredients();
        assert_eq!(result, 14);
    }
}
