use anyhow::anyhow;
use std::cmp::PartialEq;
use std::collections::VecDeque;
use std::fmt::{Display, Formatter};
use std::str::FromStr;

#[derive(Debug, Clone)]
pub struct MachineIndicatorLightState {
    machine_description: MachineDescription,
    current_state: IndicatorLights,
    press_count: usize,
}

impl MachineIndicatorLightState {
    pub fn new(machine_description: MachineDescription) -> MachineIndicatorLightState {
        let current_state = IndicatorLights {
            bitwise_state: 0,
            length: machine_description.indicator_light_diagram.length,
        };
        MachineIndicatorLightState {
            machine_description,
            current_state,
            press_count: 0,
        }
    }

    pub fn generate_steps(&self) -> VecDeque<(MachineIndicatorLightState, ButtonWiringSchematic)> {
        self.machine_description
            .button_wiring_schematics
            .iter()
            .cloned()
            .map(|button| (self.clone(), button))
            .collect()
    }

    pub fn is_finished_initializing(&self) -> bool {
        self.current_state == self.machine_description.indicator_light_diagram
    }

    pub fn press(&mut self, button: &ButtonWiringSchematic) -> anyhow::Result<()> {
        if !self
            .machine_description
            .button_wiring_schematics
            .contains(button)
        {
            return Err(anyhow!(
                "Current Machine [{}] does not contain button [{}]",
                self.machine_description,
                button
            ));
        }
        self.current_state.press(button);
        self.press_count += 1;
        Ok(())
    }
}

#[derive(Debug, Clone)]
pub struct MachineDescription {
    indicator_light_diagram: IndicatorLights,
    button_wiring_schematics: Vec<ButtonWiringSchematic>,
    joltage_requirements: JoltageRequirement,
}

impl MachineDescription {
    pub fn initialize_indicator_lights(&self) -> usize {
        let initial_state = MachineIndicatorLightState::new(self.clone());
        let mut working_deque = initial_state.generate_steps();
        loop {
            let (mut state, button) = working_deque.pop_front().unwrap();
            let result = state.press(&button);
            if let Err(err) = result {
                println!("{:?}", err);
                continue;
            }
            if state.is_finished_initializing() {
                return state.press_count;
            }
            working_deque.extend(state.generate_steps());
        }
    }
}

impl FromStr for MachineDescription {
    type Err = String;
    fn from_str(line: &str) -> Result<Self, Self::Err> {
        let mut indicator_light_diagram = IndicatorLights::default();
        let mut button_wiring_schematics = Vec::new();
        let mut joltage_requirements = JoltageRequirement::default();
        for component in line.trim().split(" ") {
            if component.contains("[") {
                indicator_light_diagram = IndicatorLights::from_str(component)?;
            } else if component.contains("(") {
                button_wiring_schematics.push(ButtonWiringSchematic::from_str(component)?);
            } else if component.contains("{") {
                joltage_requirements = JoltageRequirement::from_str(component)?;
            } else {
                return Err(format!("Unknown Component: {}", component));
            }
        }
        Ok(MachineDescription {
            indicator_light_diagram,
            button_wiring_schematics,
            joltage_requirements,
        })
    }
}

impl Display for MachineDescription {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{} ", self.indicator_light_diagram)?;
        let mut schematics = Vec::new();
        for schematic in &self.button_wiring_schematics {
            schematics.push(format!("{}", schematic));
        }
        write!(f, "{} ", schematics.join(" "))?;
        write!(f, "{}", self.joltage_requirements)
    }
}

#[derive(Debug, Default, Clone, PartialEq, Eq)]
pub struct IndicatorLights {
    bitwise_state: u16,
    length: usize,
}

impl FromStr for IndicatorLights {
    type Err = String;
    fn from_str(str: &str) -> Result<Self, Self::Err> {
        let mut bitwise_state = 0u16;
        let str = str.trim_matches(['[', ']']);
        let length = str.len();
        for (index, char) in str.chars().enumerate() {
            let val = match char {
                '#' => 1,
                _ => 0,
            };
            bitwise_state |= val << index;
        }
        Ok(Self {
            bitwise_state,
            length,
        })
    }
}

impl Display for IndicatorLights {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "[")?;
        for i in 0..self.length {
            if self.bitwise_state & (1 << i) != 0 {
                write!(f, "#")?;
            } else {
                write!(f, ".")?;
            }
        }
        write!(f, "]")
    }
}

impl IndicatorLights {
    pub fn press(&mut self, button: &ButtonWiringSchematic) {
        self.bitwise_state ^= button.bitwise_schematic;
    }
}

#[derive(Debug, Default, Clone, PartialEq)]
pub struct ButtonWiringSchematic {
    bitwise_schematic: u16,
}

impl FromStr for ButtonWiringSchematic {
    type Err = String;
    fn from_str(str: &str) -> Result<Self, Self::Err> {
        let mut bitwise_schematic = 0u16;
        let str = str.trim_matches(['(', ')']);
        let indexes: Vec<usize> = str.split(",").flat_map(|s| s.parse::<usize>()).collect();
        for index in indexes {
            bitwise_schematic |= 1 << index;
        }
        Ok(Self { bitwise_schematic })
    }
}

impl Display for ButtonWiringSchematic {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let mut indexes = Vec::new();
        for i in 0..16 {
            if self.bitwise_schematic & (1 << i) != 0 {
                indexes.push(format!("{}", i));
            }
        }
        write!(f, "({})", indexes.join(","))
    }
}

#[derive(Debug, Default, Clone)]
pub struct JoltageRequirement {
    joltages: Vec<usize>,
}

impl FromStr for JoltageRequirement {
    type Err = String;
    fn from_str(str: &str) -> Result<Self, Self::Err> {
        let str = str.trim_matches(['{', '}']);
        let joltages: Vec<usize> = str.split(",").flat_map(|s| s.parse::<usize>()).collect();
        Ok(Self { joltages })
    }
}

impl Display for JoltageRequirement {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{{")?;
        let joltages: Vec<String> = self
            .joltages
            .iter()
            .map(|joltage| format!("{}", joltage))
            .collect();
        write!(f, "{}", joltages.join(","))?;
        write!(f, "}}")
    }
}

#[cfg(test)]
mod tests {
    use crate::commons::MachineDescription;
    use std::str::FromStr;

    #[test]
    fn test_parse_and_print() {
        let test_input = include_str!("../resources/input-10-test");
        let machines: Vec<MachineDescription> = test_input
            .trim()
            .lines()
            .flat_map(MachineDescription::from_str)
            .collect();
        for machine in machines {
            println!("{}", machine)
        }
    }
}
