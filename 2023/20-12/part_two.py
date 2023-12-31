from collections import deque
from math import lcm

class Module:
    def __init__(self, name: str, destinations: list[str]) -> None:
        self.name = name
        self.destinations = destinations

    def receive(self, high_pulse: bool, source: str) -> list[tuple[str, bool]]:
        return []
    
    def __repr__(self) -> str:
        return f'{self.name} -> {", ".join(self.destinations)}'
    
    def __hash__(self) -> int:
        return self.__repr__().__hash__()

class FlipFlop(Module):
    def __init__(self, name: str, destinations: list[str]) -> None:
        self.is_on = False
        super().__init__(name, destinations)

    def receive(self, high_pulse: bool, source: str) -> list[tuple[str, bool]]:
        if high_pulse:
            return []
        
        self.is_on = not self.is_on
        signals = [(destination, self.is_on) for destination in self.destinations]
        return signals
    
    def __repr__(self) -> str:
        return f'%{super().__repr__()} [{"ON" if self.is_on else "OFF"}]'
    
class Conjunction(Module):
    def __init__(self, name: str, destinations: list[str], sources: list[str]) -> None:
        self.memory = {}
        for source in sources:
            self.memory[source] = False
        super().__init__(name, destinations)

    def set_sources(self, sources: list[str]):
        self.memory = {}
        for source in sources:
            self.memory[source] = False

    def receive(self, high_pulse: bool, source: str) -> list[tuple[str, bool]]:
        self.memory[source] = high_pulse
        signal_type = True
        if all(self.memory.values()):
            signal_type = False
        signals = [(destination, signal_type) for destination in self.destinations]
        return signals
    
    def __repr__(self) -> str:
        memory_str = '; '.join([f'{mem_key}: {"HIGH" if mem_val else "LOW"}' for mem_key, mem_val in self.memory.items()])
        return f'&{super().__repr__()} [{memory_str}]'
    
class Broadcaster(Module):
    def __init__(self, name: str, destinations: list[str]) -> None:
        super().__init__(name, destinations)

    def receive(self, high_pulse: bool, source: str) -> list[tuple[str, bool]]:
        return [(destination, high_pulse) for destination in self.destinations]
    
def parse_input(filename: str):
    modules = {}
    conjunctions: list[Conjunction] = []
    sources: dict[str, list[str]] = {}
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            name, destinations = line.split(' -> ')
            destinations = destinations.split(', ')
            mod_type: str
            if name == 'broadcaster':
                mod_type = 'broadcaster'
            else:
                mod_type = name[0]
                name = name[1:]
            module: Module
            if mod_type == 'broadcaster':
                module = Broadcaster('broadcaster', destinations)
            elif mod_type == '%':
                module = FlipFlop(name, destinations)
            else:
                module = Conjunction(name, destinations, [])
                conjunctions.append(module)
            
            # collect sources
            for destination in destinations:
                if destination not in sources:
                    sources[destination] = []
                sources[destination].append(name)

            modules[name] = module

    # postprocessing to add sources to conjunctions
    for conjunction in conjunctions:
        conjunction.set_sources(sources[conjunction.name])

    return modules

def run_sequence(modules: dict[str, Module]):
    pulses = deque([('button', 'broadcaster', False)])
    low_pulse_count = 0
    high_pulse_count = 0
    rx_low = 0
    dc_low_out = False
    jh_low_out = False
    zq_low_out = False
    qm_low_out = False
    while pulses:
        source, dest_str, is_high_pulse = pulses.popleft()
        if is_high_pulse:
            high_pulse_count += 1
        else:
            low_pulse_count += 1
        if dest_str == 'rx' and not is_high_pulse:
            print('######')
            print(f'ls -0-> rx (Total pulse count = {low_pulse_count + high_pulse_count})')
            print('######')
            rx_low += 1
        if dest_str not in modules:
            continue
        if not is_high_pulse:
            if source == 'dc':
                dc_low_out = True
            elif source == 'jh':
                jh_low_out = True
            elif source == 'zq':
                zq_low_out = True
            elif source == 'qm':
                qm_low_out = True
        destination = modules[dest_str]
        sent_pulses = destination.receive(is_high_pulse, source)
        for next_dest, next_is_high_pulse in sent_pulses:
            pulses.append((dest_str, next_dest, next_is_high_pulse))
    return dc_low_out, jh_low_out, zq_low_out, qm_low_out

def build_state(modules: dict[str, Module]) -> str:
    return ','.join([str(hash(module)) for module in modules.values()])



def find_rx(modules: dict[str, Module]):
    dc_loop = 0
    jh_loop = 0
    qm_loop = 0
    zq_loop = 0
    idx = 0
    while True:
        idx += 1
        dc_low_out, jh_low_out, zq_low_out, qm_low_out = run_sequence(modules)
        if dc_low_out and dc_loop == 0:
            dc_loop = idx
        if jh_low_out and jh_loop == 0:
            jh_loop = idx
        if zq_low_out and zq_loop == 0:
            zq_loop = idx
        if qm_low_out and qm_loop == 0:
            qm_loop = idx

        if dc_loop > 0 and jh_loop > 0 and zq_loop > 0 and qm_loop > 0:
            break

    return lcm(dc_loop, jh_loop, zq_loop, qm_loop)

def run_sequences(modules: dict[str, Module], run_count: int):
    initial_state = build_state(modules)
    visited_states = [initial_state]
    state_counts = {initial_state: (0, 0)}
    low_pulse_count = 0
    high_pulse_count = 0
    rx_low = 0
    for idx in range(run_count):
        run_low_pulse_count, run_high_pulse_count, run_rx_low = run_sequence(modules)
        low_pulse_count += run_low_pulse_count
        high_pulse_count += run_high_pulse_count
        rx_low += run_rx_low
        state = build_state(modules)

        if state not in visited_states:
            visited_states.append(state)
            state_counts[state] = (low_pulse_count, high_pulse_count)
            continue

        distance = idx + 1 - visited_states.index(state)
        remainder = (run_count - (idx + 1)) % distance
        loops_remaining = int((run_count - (idx + 1)) / distance)

        delta_low = low_pulse_count - state_counts[state][0]
        delta_high = high_pulse_count - state_counts[state][1]

        low_pulse_count += delta_low * loops_remaining
        high_pulse_count += delta_high * loops_remaining

        rem_low, rem_high = run_sequences(modules, remainder)
        low_pulse_count += rem_low
        high_pulse_count += rem_high

        return low_pulse_count, high_pulse_count
    
    return low_pulse_count, high_pulse_count

modules = parse_input('input-20')

rx_button_count = find_rx(modules)
print(rx_button_count)

# 0
# &dc
# &qm
# &jh
# &za

# 1
# &tx -> high
# &dd
# &nz
# &ph

# 0
# &ls -> rx