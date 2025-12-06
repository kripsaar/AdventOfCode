use std::collections::HashMap;
use std::rc::Rc;
use std::str::FromStr;

pub fn part1() {
    let input = include_str!("../resources/input-4");
    let grid = Grid::from_str(input).unwrap();
    let result = grid.count_reachable_rolls();
    println!("Part 1: {}", result);
}

struct Roll {
    x: isize,
    y: isize,
}

struct Grid {
    map: HashMap<(isize, isize), Rc<Roll>>,
    rolls: Vec<Rc<Roll>>,
}

impl FromStr for Grid {
    type Err = ();
    fn from_str(str_input: &str) -> Result<Self, Self::Err> {
        let mut map: HashMap<(isize, isize), Rc<Roll>> = HashMap::new();
        let mut rolls: Vec<Rc<Roll>> = Vec::new();
        str_input.lines().enumerate().for_each(|(y, line)| {
            line.chars().enumerate().for_each(|(x, ch)| {
                if ch == '@' {
                    let x = x as isize;
                    let y = y as isize;
                    let roll = Rc::new(Roll { x, y });
                    rolls.push(roll.clone());
                    map.insert((x, y), roll);
                }
            })
        });
        Ok(Grid { map, rolls })
    }
}

impl Grid {
    fn count_reachable_rolls(&self) -> usize {
        self.rolls
            .iter()
            .filter(|roll| is_roll_reachable(roll, &self))
            .count()
    }
}

fn is_roll_reachable(roll: &Roll, grid: &Grid) -> bool {
    let roll_x = roll.x;
    let roll_y = roll.y;
    if !grid.map.contains_key(&(roll_x, roll_y)) {
        return false;
    }
    let mut neighbor_count = 0;
    for x in (roll_x - 1)..=(roll_x + 1) {
        for y in (roll_y - 1)..=(roll_y + 1) {
            if (x, y) == (roll_x, roll_y) {
                continue;
            }
            if grid.map.contains_key(&(x, y)) {
                neighbor_count += 1;
            }
        }
    }
    neighbor_count < 4
}

#[cfg(test)]
mod tests {
    use crate::part1::Grid;
    use std::str::FromStr;

    #[test]
    fn test_example() {
        let example_input = include_str!("../resources/input-4-test");
        let grid = Grid::from_str(example_input).unwrap();
        let result = grid.count_reachable_rolls();
        assert_eq!(result, 13);
    }
}
