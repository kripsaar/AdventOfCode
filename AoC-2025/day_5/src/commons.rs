use std::ops::RangeInclusive;
use std::str::FromStr;

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub struct Ingredient {
    id: usize,
}

#[derive(Debug)]
pub struct FreshnessDatabase {
    freshness_ranges: Vec<RangeInclusive<usize>>,
    ingredients: Vec<Ingredient>,
}

impl FromStr for FreshnessDatabase {
    type Err = ();
    fn from_str(str_input: &str) -> Result<Self, Self::Err> {
        let (freshness_range_str, ingredients_str) =
            str_input.split_at(str_input.find("\r\n\r\n").unwrap());

        let freshness_ranges = freshness_range_str
            .trim()
            .lines()
            .map(|line| {
                let limits: Vec<usize> = line
                    .trim()
                    .split("-")
                    .flat_map(|str| str.parse::<usize>())
                    .collect();
                limits[0]..=limits[1]
            })
            .collect();

        let ingredients = ingredients_str
            .trim()
            .lines()
            .map(|line| Ingredient {
                id: line.trim().parse().unwrap(),
            })
            .collect();

        Ok(FreshnessDatabase {
            freshness_ranges,
            ingredients,
        })
    }
}

impl FreshnessDatabase {
    pub fn is_ingredient_fresh(&self, ingredient: &Ingredient) -> bool {
        self.freshness_ranges
            .iter()
            .any(|range| range.contains(&ingredient.id))
    }

    pub fn count_fresh_ingredients(&self) -> usize {
        self.ingredients
            .iter()
            .filter(|ingredient| self.is_ingredient_fresh(ingredient))
            .count()
    }

    pub fn count_all_possible_fresh_ingredients(&self) -> usize {
        let normalized_freshness_database = self.merge_overlapping_ranges();
        normalized_freshness_database
            .freshness_ranges
            .iter()
            .map(|range| range.end() - range.start() + 1)
            .sum()
    }

    pub fn merge_overlapping_ranges(&self) -> FreshnessDatabase {
        let mut old_freshness_ranges = self.freshness_ranges.clone();
        let mut new_freshness_ranges: Vec<RangeInclusive<usize>> = Vec::new();
        old_freshness_ranges.sort_by_key(|range| *range.start());
        let mut left = old_freshness_ranges.first().unwrap().clone();
        for right in &old_freshness_ranges[1..] {
            if left.start() <= right.start() && left.end() >= right.end() {
                // right is completely inside left
                continue;
            }
            if left.end() >= right.start() && right.end() > left.end() {
                left = *left.start()..=*right.end()
            } else {
                new_freshness_ranges.push(left.clone());
                left = right.clone();
            }
        }
        new_freshness_ranges.push(left);
        FreshnessDatabase {
            freshness_ranges: new_freshness_ranges,
            ingredients: self.ingredients.clone(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::commons::FreshnessDatabase;

    #[test]
    fn test_merging_overlapping_ranges() {
        let ranges = vec![1..=10, 3..=5, 8..=15];
        let freshness_database = FreshnessDatabase {
            freshness_ranges: ranges,
            ingredients: vec![],
        };
        let merged = freshness_database.merge_overlapping_ranges();
        assert_eq!(merged.freshness_ranges, vec![1..=15]);
    }
}
