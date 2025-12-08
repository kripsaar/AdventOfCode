use itertools::Itertools;
use std::collections::HashSet;
use std::rc::Rc;
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-8");
    let junction_boxes = parse_input(input);
    let result = connect_junction_boxes(&junction_boxes, 1000);
    println!("Part 1: {}", result);
}

#[derive(Debug, Hash, Eq, PartialEq, Clone)]
struct JunctionBox {
    x: isize,
    y: isize,
    z: isize,
}

impl JunctionBox {
    fn new(x: isize, y: isize, z: isize) -> JunctionBox {
        JunctionBox { x, y, z }
    }

    fn distance_to(&self, other_junction_box: &JunctionBox) -> f64 {
        (((self.x - other_junction_box.x).pow(2)
            + (self.y - other_junction_box.y).pow(2)
            + (self.z - other_junction_box.z).pow(2)) as f64)
            .sqrt()
    }
}

impl FromStr for JunctionBox {
    type Err = String;
    fn from_str(input: &str) -> Result<Self, Self::Err> {
        let coords: Vec<isize> = input.trim().split(',').flat_map(isize::from_str).collect();
        if coords.len() != 3 {
            return Err(format!("Invalid number of components: {}", coords.len()));
        }
        Ok(JunctionBox::new(coords[0], coords[1], coords[2]))
    }
}

#[derive(Debug, Eq, PartialEq, Clone)]
struct Circuit {
    junction_set: HashSet<Rc<JunctionBox>>,
}

impl Circuit {
    fn from_junction_box(junction_box: Rc<JunctionBox>) -> Circuit {
        Circuit {
            junction_set: HashSet::from([junction_box]),
        }
    }

    fn contains(&self, junction: &Rc<JunctionBox>) -> bool {
        self.junction_set.contains(junction)
    }

    fn connect(&mut self, other: Circuit) {
        self.junction_set.extend(other.junction_set);
    }
}

fn parse_input(input: &str) -> Vec<Rc<JunctionBox>> {
    input
        .trim()
        .lines()
        .flat_map(JunctionBox::from_str)
        .map(Rc::new)
        .collect()
}

fn connect_junction_boxes(input: &[Rc<JunctionBox>], limit: usize) -> usize {
    let mut circuits: Vec<Circuit> = input
        .iter()
        .map(|junction_box| Circuit::from_junction_box(junction_box.clone()))
        .collect();
    let mut pairs: Vec<(Rc<JunctionBox>, Rc<JunctionBox>)> = input
        .iter()
        .combinations(2)
        .map(|combo| (combo[0].clone(), combo[1].clone()))
        .sorted_by(|left, right| {
            right
                .0
                .distance_to(&right.1)
                .total_cmp(&(left.0.distance_to(&left.1)))
        })
        .collect();
    for _i in 0..limit {
        if pairs.is_empty() {
            break;
        }
        let pair = pairs.pop().unwrap();
        let left_circuit_index = circuits
            .iter()
            .position(|circuit| circuit.contains(&pair.0))
            .unwrap();
        let mut left_circuit = circuits.remove(left_circuit_index);
        if let Some(right_circuit_index) = circuits
            .iter()
            .position(|circuit| circuit.contains(&pair.1))
        {
            let right_circuit = circuits.remove(right_circuit_index);
            left_circuit.connect(right_circuit);
        };
        circuits.push(left_circuit);
    }
    circuits.sort_by(|left, right| right.junction_set.len().cmp(&left.junction_set.len()));
    circuits.truncate(3);
    circuits
        .iter()
        .map(|circuit| circuit.junction_set.len())
        .product()
}

#[cfg(test)]
mod tests {
    use crate::part1::{connect_junction_boxes, parse_input};

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-8-test");
        let junction_boxes = parse_input(example_input);
        let result = connect_junction_boxes(&junction_boxes, 10);
        assert_eq!(result, 40);
    }
}
