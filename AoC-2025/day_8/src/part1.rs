use crate::commons::{connect_junction_boxes, parse_input};

pub fn part1() {
    let input = include_str!("../resources/input-8");
    let junction_boxes = parse_input(input);
    let (result, _last_pair) = connect_junction_boxes(&junction_boxes, Some(1000));
    println!("Part 1: {}", result);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-8-test");
        let junction_boxes = parse_input(example_input);
        let (result, _last_pair) = connect_junction_boxes(&junction_boxes, Some(10));
        assert_eq!(result, 40);
    }
}
