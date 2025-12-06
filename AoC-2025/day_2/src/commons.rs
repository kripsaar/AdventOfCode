use std::marker::PhantomData;
use std::num::ParseIntError;
use std::str::FromStr;

pub struct IdRange<I>
where
    I: InvalidId,
{
    start: u64,
    end: u64,
    phantom_data: PhantomData<I>,
}

impl<I> FromStr for IdRange<I>
where
    I: InvalidId,
{
    type Err = ParseIntError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let split: Vec<u64> = s
            .split("-")
            .map(|str| str.parse::<u64>().unwrap())
            .collect();
        Ok(IdRange::<I>::new(split[0], split[1]))
    }
}

impl<I> IdRange<I>
where
    I: InvalidId,
{
    pub fn new(start: u64, end: u64) -> Self {
        Self {
            start,
            end,
            phantom_data: Default::default(),
        }
    }

    pub fn read_and_evaluate_ids(input_str: &str) -> u64 {
        let id_ranges = Self::parse_input(input_str);
        id_ranges
            .iter()
            .map(|id_range| id_range.add_all_invalid_ids())
            .sum()
    }

    pub fn parse_input(input_str: &str) -> Vec<IdRange<I>> {
        input_str
            .trim()
            .split(",")
            .flat_map(Self::from_str)
            .collect()
    }

    pub fn add_all_invalid_ids(&self) -> u64 {
        let mut result = 0;
        let mut invalid_id = I::new(self.start - 1);
        loop {
            invalid_id = invalid_id.next();
            if invalid_id.get_id() > self.end {
                break;
            }
            result += invalid_id.get_id()
        }

        result
    }
}

pub trait InvalidId {
    fn new(id: u64) -> Self;
    fn get_id(&self) -> u64;
    fn next_invalid_id(number: u64) -> Self;
    fn next(&self) -> Self;
}
