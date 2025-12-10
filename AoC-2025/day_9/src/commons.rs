use itertools::Itertools;
use std::cmp::Ordering;
use std::collections::HashSet;
use std::str::FromStr;

#[derive(Debug, Eq, PartialEq, Clone, Hash)]
pub struct Tile {
    x: usize,
    y: usize,
}

impl Tile {
    pub fn new(x: usize, y: usize) -> Tile {
        Tile { x, y }
    }
}

#[derive(Debug, Eq, PartialEq, Clone)]
pub struct Rectangle {
    corners: [Tile; 2],
    area: usize,
}

impl Rectangle {
    pub fn new(corners: [Tile; 2]) -> Self {
        let size =
            (&corners[0].x.abs_diff(corners[1].x) + 1) * (&corners[0].y.abs_diff(corners[1].y) + 1);
        Self {
            corners,
            area: size,
        }
    }

    /// Create a new rectangle where every tile is red or green.
    /// For this, it is enough to check if each edge is entirely colored.
    /// Idea: check intersections with borderlines
    /// -> if any line ever exits colored area, our rectangle is invalid
    pub fn new_valid(corners: &[Tile], lines: &HashSet<Line>) -> Self {
        let upper_left = Tile::new(
            corners[0].x.min(corners[1].x),
            corners[0].y.min(corners[1].y),
        );
        let upper_right = Tile::new(
            corners[0].x.max(corners[1].x),
            corners[0].y.min(corners[1].y),
        );
        let lower_left = Tile::new(
            corners[0].x.min(corners[1].x),
            corners[0].y.max(corners[1].y),
        );
        let lower_right = Tile::new(
            corners[0].x.max(corners[1].x),
            corners[0].y.max(corners[1].y),
        );

        todo!()
    }

    pub fn area(&self) -> usize {
        self.area
    }
}

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
pub struct Line {
    start: Tile,
    end: Tile,
}

impl Line {
    pub fn new(points: &[Tile]) -> Self {
        let (left, right) = (&points[0], &points[1]);
        match &left.x.cmp(&right.x) {
            Ordering::Equal => {
                if left.y < right.y {
                    Line {
                        start: left.clone(),
                        end: right.clone(),
                    }
                } else {
                    Line {
                        start: right.clone(),
                        end: left.clone(),
                    }
                }
            }
            Ordering::Less => Line {
                start: left.clone(),
                end: right.clone(),
            },
            Ordering::Greater => Line {
                start: right.clone(),
                end: left.clone(),
            },
        }
    }

    pub fn contains(&self, point: &Tile) -> bool {
        if self.start.x == self.end.x {
            point.x == self.start.x && point.y >= self.start.y && point.y <= self.end.y
        } else {
            point.y == self.start.y && point.x >= self.start.x && point.x <= self.end.x
        }
    }
}

#[derive(Debug)]
pub struct Grid {
    tiles: Vec<Tile>,
    lines: HashSet<Line>,
}

impl FromStr for Grid {
    type Err = ();
    fn from_str(input: &str) -> Result<Self, Self::Err> {
        let tiles: Vec<Tile> = input
            .trim()
            .lines()
            .map(|line| line.split(',').collect())
            .map(|split: Vec<&str>| {
                let (left, right) = (split[0].parse().unwrap(), split[1].parse().unwrap());
                Tile::new(left, right)
            })
            .collect();
        let mut lines: HashSet<Line> = tiles.windows(2).map(Line::new).collect();
        lines.insert(Line::new(&[
            tiles.last().unwrap().clone(),
            tiles.first().unwrap().clone(),
        ]));
        Ok(Self { tiles, lines })
    }
}

impl Grid {
    pub fn generate_unchecked_rectangles_sorted(&self) -> Vec<Rectangle> {
        self.tiles
            .iter()
            .cloned()
            .combinations(2)
            .map(|combination| Rectangle::new(combination.try_into().unwrap()))
            .sorted_by_key(Rectangle::area)
            .collect()
    }
}
