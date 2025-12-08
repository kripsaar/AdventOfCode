use crate::commons::{connect_junction_boxes, parse_input};

pub fn part2() {
    let input = include_str!("../resources/input-8");
    let junction_boxes = parse_input(input);
    let (_longest_3_product, last_pair) = connect_junction_boxes(&junction_boxes, None);
    let (left, right) = last_pair.unwrap();
    let result = left.x() * right.x();
    println!("Part 2: {}", result);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-8-test");
        let junction_boxes = parse_input(example_input);
        let (_longest_3_product, last_pair) = connect_junction_boxes(&junction_boxes, None);
        let (left, right) = last_pair.unwrap();
        let result = left.x() * right.x();
        assert_eq!(result, 25272);
    }
}
