use std::ops::RangeInclusive;
use std::str::FromStr;

pub struct Ingredient {
    id: usize,
}

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
                    .map(|str| str.parse::<usize>())
                    .flatten()
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
            .find(|range| range.contains(&ingredient.id))
            .is_some()
    }

    pub fn count_fresh_ingredients(&self) -> usize {
        self.ingredients
            .iter()
            .filter(|ingredient| self.is_ingredient_fresh(ingredient))
            .count()
    }
}
