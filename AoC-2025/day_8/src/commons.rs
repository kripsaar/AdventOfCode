use itertools::Itertools;
use std::collections::HashSet;
use std::rc::Rc;
use std::str::FromStr;

#[derive(Debug, Hash, Eq, PartialEq, Clone)]
pub struct JunctionBox {
    x: isize,
    y: isize,
    z: isize,
}

impl JunctionBox {
    pub fn new(x: isize, y: isize, z: isize) -> JunctionBox {
        JunctionBox { x, y, z }
    }

    pub fn x(&self) -> isize {
        self.x
    }

    pub fn distance_to(&self, other_junction_box: &JunctionBox) -> f64 {
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
pub struct Circuit {
    junction_set: HashSet<Rc<JunctionBox>>,
}

impl Circuit {
    pub fn from_junction_box(junction_box: Rc<JunctionBox>) -> Circuit {
        Circuit {
            junction_set: HashSet::from([junction_box]),
        }
    }

    pub fn len(&self) -> usize {
        self.junction_set.len()
    }

    pub fn contains(&self, junction: &Rc<JunctionBox>) -> bool {
        self.junction_set.contains(junction)
    }

    pub fn connect(&mut self, other: Circuit) {
        self.junction_set.extend(other.junction_set);
    }
}

pub fn parse_input(input: &str) -> Vec<Rc<JunctionBox>> {
    input
        .trim()
        .lines()
        .flat_map(JunctionBox::from_str)
        .map(Rc::new)
        .collect()
}

pub fn connect_junction_boxes(
    input: &[Rc<JunctionBox>],
    limit: Option<usize>,
) -> (usize, Option<(Rc<JunctionBox>, Rc<JunctionBox>)>) {
    let mut circuits: Vec<Circuit> = input
        .iter()
        .map(|junction_box| Circuit::from_junction_box(junction_box.clone()))
        .collect();
    let pairs: Vec<(Rc<JunctionBox>, Rc<JunctionBox>)> = input
        .iter()
        .combinations(2)
        .map(|combo| (combo[0].clone(), combo[1].clone()))
        .sorted_by(|left, right| {
            left.0
                .distance_to(&left.1)
                .total_cmp(&(right.0.distance_to(&right.1)))
        })
        .collect();
    let mut i = 0;
    let mut last_pair = None;
    for pair in pairs {
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
        last_pair = Some(pair);
        i += 1;
        if limit == Some(i) {
            println!("Limit [{}] reached!", i);
            break;
        }
        if circuits.len() == 1 {
            println!("Connected every junction box into one circuit!",);
            break;
        }
    }
    circuits.sort_by_key(|right| std::cmp::Reverse(right.len()));
    circuits.truncate(3);
    let longest_3_product = circuits.iter().map(|circuit| circuit.len()).product();
    (longest_3_product, last_pair)
}
