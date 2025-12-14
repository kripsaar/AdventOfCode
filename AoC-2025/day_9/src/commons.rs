use itertools::Itertools;
use std::cmp::Ordering;
use std::collections::HashSet;
use std::str::FromStr;

#[derive(Debug, Eq, PartialEq, Clone, Hash, Copy)]
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
    upper_left: Tile,
    upper_right: Tile,
    lower_left: Tile,
    lower_right: Tile,
    area: usize,
}

impl Rectangle {
    pub fn new(corners: [Tile; 2]) -> Self {
        let size =
            (&corners[0].x.abs_diff(corners[1].x) + 1) * (&corners[0].y.abs_diff(corners[1].y) + 1);
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
        Self {
            corners,
            upper_left,
            upper_right,
            lower_left,
            lower_right,
            area: size,
        }
    }

    pub fn contains(&self, tile: &Tile) -> bool {
        let contains_x = self.upper_left.x < tile.x && tile.x < self.upper_right.x;
        let contains_y = self.upper_left.y < tile.y && tile.y < self.lower_left.y;
        contains_x && contains_y
    }

    pub fn intersects(&self, line: &Line) -> bool {
        if self.contains(&line.start) || self.contains(&line.end) {
            return true;
        }
        match line.is_horizontal() {
            true => {
                if line.start.x <= self.upper_left.x
                    && self.upper_right.x <= line.end.x
                    && self.upper_left.y < line.start.y
                    && line.start.y < self.lower_left.y
                {
                    return true;
                }
                let left = Line::new(&[self.upper_left, self.lower_left]);
                let right = Line::new(&[self.upper_right, self.lower_right]);
                left.intersects(line) || right.intersects(line)
            }
            false => {
                if line.start.y <= self.upper_left.y
                    && self.lower_left.y <= line.end.y
                    && self.upper_left.x < line.start.x
                    && line.start.x < self.upper_right.x
                {
                    return true;
                }
                let top = Line::new(&[self.upper_left, self.upper_right]);
                let bottom = Line::new(&[self.lower_left, self.lower_right]);
                top.intersects(line) || bottom.intersects(line)
            }
        }
    }

    /// Create a new rectangle where every tile is red or green.
    /// For this, it is enough to check if each edge is entirely colored.
    /// Idea: check intersections with borderlines
    /// -> if any line ever exits colored area, our rectangle is invalid
    pub fn new_valid(corners: [Tile; 2], lines: &HashSet<Line>) -> Option<Self> {
        let new = Self::new(corners);

        if lines.iter().any(|line| new.intersects(line)) {
            return None;
        }

        Some(new)
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
                        start: *left,
                        end: *right,
                    }
                } else {
                    Line {
                        start: *right,
                        end: *left,
                    }
                }
            }
            Ordering::Less => Line {
                start: *left,
                end: *right,
            },
            Ordering::Greater => Line {
                start: *right,
                end: *left,
            },
        }
    }

    pub fn is_horizontal(&self) -> bool {
        self.start.y == self.end.y
    }

    pub fn intersects(&self, other: &Line) -> bool {
        if !(self.is_horizontal() ^ other.is_horizontal()) {
            return false;
        }
        match self.is_horizontal() {
            true => {
                let y_intersection = other.start.y < self.start.y && other.end.y > self.end.y;
                let x_intersection = self.start.x < other.start.x && self.end.x > other.end.x;
                y_intersection && x_intersection
            }
            false => {
                let y_intersection = self.start.y < other.start.y && self.end.y > other.end.y;
                let x_intersection = other.start.x < self.start.x && other.end.x > self.end.x;
                y_intersection && x_intersection
            }
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
            *tiles.last().unwrap(),
            *tiles.first().unwrap(),
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

    pub fn generate_valid_rectangles_sorted(&self) -> Vec<Rectangle> {
        self.tiles
            .iter()
            .cloned()
            .combinations(2)
            .flat_map(|combination| {
                Rectangle::new_valid(combination.try_into().unwrap(), &self.lines)
            })
            .sorted_by_key(Rectangle::area)
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_line_intersection() {
        let left = Line::new(&[Tile::new(12, 1), Tile::new(15, 1)]);
        let right = Line::new(&[Tile::new(14, 0), Tile::new(14, 5)]);
        let result = left.intersects(&right);
        assert!(result);

        let left = Line::new(&[Tile::new(12, 1), Tile::new(15, 1)]);
        let right = Line::new(&[Tile::new(14, 1), Tile::new(15, 5)]);
        let result = left.intersects(&right);
        assert!(!result);

        let left = Line::new(&[Tile::new(12, 1), Tile::new(15, 1)]);
        let right = Line::new(&[Tile::new(11, 1), Tile::new(16, 1)]);
        let result = left.intersects(&right);
        assert!(!result);

        let left = Line::new(&[Tile::new(12, 1), Tile::new(12, 5)]);
        let right = Line::new(&[Tile::new(12, 0), Tile::new(12, 3)]);
        let result = left.intersects(&right);
        assert!(!result);

        let left = Line::new(&[Tile::new(3, 4), Tile::new(3, 7)]);
        let right = Line::new(&[Tile::new(0, 6), Tile::new(5, 6)]);
        let result = left.intersects(&right);
        assert!(result);
    }

    #[test]
    fn test_rectangle_intersection() {
        let rectangle = Rectangle::new([Tile::new(10, 10), Tile::new(20, 20)]);
        let outside_line = Line::new(&[Tile::new(5, 10), Tile::new(5, 20)]);
        let result = rectangle.intersects(&outside_line);
        assert!(!result);
        let touching_line_x = Line::new(&[Tile::new(8, 10), Tile::new(15, 10)]);
        let result = rectangle.intersects(&touching_line_x);
        assert!(!result);
        let touching_line_y = Line::new(&[Tile::new(20, 15), Tile::new(20, 22)]);
        let result = rectangle.intersects(&touching_line_y);
        assert!(!result);
        let line_inside = Line::new(&[Tile::new(12, 15), Tile::new(18, 15)]);
        let result = rectangle.intersects(&line_inside);
        assert!(result);
        let line_intersects_left = Line::new(&[Tile::new(5, 13), Tile::new(17, 13)]);
        let result = rectangle.intersects(&line_intersects_left);
        assert!(result);
        let line_bisects_vertically = Line::new(&[Tile::new(17, 2), Tile::new(17, 30)]);
        let result = rectangle.intersects(&line_bisects_vertically);
        assert!(result);
        let line_bisects_horizontally = Line::new(&[Tile::new(10, 15), Tile::new(20, 15)]);
        let result = rectangle.intersects(&line_bisects_horizontally);
        assert!(result);
    }
}
