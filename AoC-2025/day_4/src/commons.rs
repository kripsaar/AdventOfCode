use std::collections::HashMap;
use std::rc::Rc;
use std::str::FromStr;

#[derive(Debug, PartialEq, Eq)]
pub struct Roll {
    x: isize,
    y: isize,
}

pub struct Grid {
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
    pub fn count_reachable_rolls(&self) -> usize {
        self.rolls
            .iter()
            .filter(|roll| self.is_roll_reachable(roll))
            .count()
    }

    pub fn count_reachable_rolls_and_remove(&self) -> (usize, Self) {
        let mut map = self.map.clone();
        let mut rolls = self.rolls.clone();
        let reachable_rolls: Vec<Rc<Roll>> = self
            .rolls
            .iter()
            .filter(|roll| self.is_roll_reachable(roll))
            .cloned()
            .collect();
        let reachable_rolls_count = reachable_rolls.len();
        for reachable_roll in reachable_rolls {
            map.remove(&(reachable_roll.x, reachable_roll.y));
            rolls.retain(|element| *element != reachable_roll);
        }
        (reachable_rolls_count, Grid { map, rolls })
    }

    pub fn count_all_removable_rolls_recursively(&self) -> usize {
        let (reachable_rolls_count, grid) = self.count_reachable_rolls_and_remove();
        if reachable_rolls_count == 0 {
            return 0;
        }
        reachable_rolls_count + grid.count_all_removable_rolls_recursively()
    }

    pub fn is_roll_reachable(&self, roll: &Roll) -> bool {
        let roll_x = roll.x;
        let roll_y = roll.y;
        if !self.map.contains_key(&(roll_x, roll_y)) {
            return false;
        }
        let mut neighbor_count = 0;
        for x in (roll_x - 1)..=(roll_x + 1) {
            for y in (roll_y - 1)..=(roll_y + 1) {
                if (x, y) == (roll_x, roll_y) {
                    continue;
                }
                if self.map.contains_key(&(x, y)) {
                    neighbor_count += 1;
                }
            }
        }
        neighbor_count < 4
    }
}
