class Part:
    def __init__(self, x: int, m: int, a: int, s: int) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s
    
    def __repr__(self) -> str:
        return f'{{x={self.x},m={self.m},a={self.a},s={self.s}}}'
    
    def score(self) -> int:
        return self.x + self.m + self.a + self.s

class WorkflowCondition:
    def __init__(self, condition: str, on_passed: str) -> None:
        self.condition = condition
        self.on_passed = on_passed

    def __repr__(self) -> str:
        if not self.condition:
            return f'{self.on_passed}'
        return f'{self.condition}:{self.on_passed}'
    
    def evaluate(self, part: Part) -> str:
        if not self.condition:
            return self.on_passed

        comparator = '<' if '<' in self.condition else '>'
        variable_name, comparison_value = self.condition.split(comparator)
        comparison_value = int(comparison_value)
        variable_value: int

        if variable_name == 'x':
            variable_value = part.x
        elif variable_name == 'm':
            variable_value = part.m
        elif variable_name == 'a':
            variable_value = part.a
        else:
            variable_value = part.s

        passed = False
        if comparator == '<':
            passed = variable_value < comparison_value
        else:
            passed = variable_value > comparison_value

        if passed:
            return self.on_passed
        else:
            return None

def parse_input(filename: str):
    workflows: dict[str, list[WorkflowCondition]] = {}
    parts: list[Part] = []
    with open(filename, 'r') as file:
        workflow_lines, part_lines = file.read().split('\n\n')
        workflow_lines = workflow_lines.strip()
        part_lines = part_lines.strip()

        for workflow_line in workflow_lines.splitlines():
            workflow_line = workflow_line.strip()
            name, rest = workflow_line.split('{')
            workflow_list: list[WorkflowCondition] = []
            rest = rest.strip('}')
            workflow_strs = rest.split(',')
            for workflow_str in workflow_strs:
                if ':' not in workflow_str:
                    workflow_list.append(WorkflowCondition(None, workflow_str))
                    continue
                condition, on_passed = workflow_str.split(':')
                workflow_list.append(WorkflowCondition(condition, on_passed))
            workflows[name] = workflow_list
        
        for part_line in part_lines.splitlines():
            part_line = part_line.strip().strip('}{')
            x, m, a, s = 0, 0, 0, 0
            for part_component in part_line.split(','):
                name, value = part_component.split('=')
                value = int(value)
                if 'x' in name:
                    x = value
                elif 'm' in name:
                    m = value
                elif 'a' in name:
                    a = value
                else:
                    s = value
            parts.append(Part(x, m, a, s))
    return workflows, parts

workflows, parts = parse_input('input-19')

accepted_sum = 0
for part in parts:
    current_workflow = workflows['in'].copy()
    while current_workflow:
        workflow_condition = current_workflow.pop(0)
        result = workflow_condition.evaluate(part)
        if not result:
            continue
        if result == 'R':
            break
        if result == 'A':
            accepted_sum += part.score()
            break
        current_workflow = workflows[result].copy()

print(accepted_sum)