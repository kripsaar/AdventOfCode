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
    
class Ratings:
    def __init__(self, x: range, m: range, a: range, s: range) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def score(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

class WorkflowCondition:
    def __init__(self, condition: str, on_passed: str) -> None:
        self.condition = condition
        self.on_passed = on_passed

    def __repr__(self) -> str:
        if not self.condition:
            return f'{self.on_passed}'
        return f'{self.condition}:{self.on_passed}'
    
    def branch(self, ratings: Ratings):
        if not self.condition:
            return {True: ratings, False: None}
        
        comparator = '<' if '<' in self.condition else '>'
        variable_name, comparison_value = self.condition.split(comparator)
        comparison_value = int(comparison_value)

        if comparator == '<':
            if variable_name == 'x':
                # x < 1200
                if ratings.x.start >= comparison_value:
                    return {True: None, False: ratings}
                if ratings.x.stop <= comparison_value:
                    return {True: ratings, False: None}
                true_x_range = range(ratings.x.start, comparison_value)
                false_x_range = range(comparison_value, ratings.x.stop)
                return {True: Ratings(true_x_range, ratings.m, ratings.a, ratings.s),
                        False: Ratings(false_x_range, ratings.m, ratings.a, ratings.s)}
            if variable_name == 'm':
                if ratings.m.start >= comparison_value:
                    return {True: None, False: ratings}
                if ratings.m.stop <= comparison_value:
                    return {True: ratings, False: None}
                true_m_range = range(ratings.m.start, comparison_value)
                false_m_range = range(comparison_value, ratings.m.stop)
                return {True: Ratings(ratings.x, true_m_range, ratings.a, ratings.s),
                        False: Ratings(ratings.x, false_m_range, ratings.a, ratings.s)}
            if variable_name == 'a':
                if ratings.a.start >= comparison_value:
                    return {True: None, False: ratings}
                if ratings.a.stop <= comparison_value:
                    return {True: ratings, False: None}
                true_a_range = range(ratings.a.start, comparison_value)
                false_a_range = range(comparison_value, ratings.a.stop)
                return {True: Ratings(ratings.x, ratings.m, true_a_range, ratings.s),
                        False: Ratings(ratings.x, ratings.m, false_a_range, ratings.s)}
            else:
                if ratings.s.start >= comparison_value:
                    return {True: None, False: ratings}
                if ratings.s.stop <= comparison_value:
                    return {True: ratings, False: None}
                true_s_range = range(ratings.s.start, comparison_value)
                false_s_range = range(comparison_value, ratings.s.stop)
                return {True: Ratings(ratings.x, ratings.m, ratings.a, true_s_range),
                        False: Ratings(ratings.x, ratings.m, ratings.a, false_s_range)}
        else:
            if variable_name == 'x':
                if ratings.x.stop <= comparison_value + 1:
                    return {True: None, False: ratings}
                if ratings.x.start > comparison_value:
                    return {True: ratings, False: None}
                true_x_range = range(comparison_value + 1, ratings.x.stop)
                false_x_range = range(ratings.x.start, comparison_value + 1)
                return {True: Ratings(true_x_range, ratings.m, ratings.a, ratings.s),
                        False: Ratings(false_x_range, ratings.m, ratings.a, ratings.s)}
            if variable_name == 'm':
                if ratings.m.stop <= comparison_value + 1:
                    return {True: None, False: ratings}
                if ratings.m.start > comparison_value:
                    return {True: ratings, False: None}
                true_m_range = range(comparison_value + 1, ratings.m.stop)
                false_m_range = range(ratings.m.start, comparison_value + 1)
                return {True: Ratings(ratings.x, true_m_range, ratings.a, ratings.s),
                        False: Ratings(ratings.x, false_m_range, ratings.a, ratings.s)}
            if variable_name == 'a':
                if ratings.a.stop <= comparison_value + 1:
                    return {True: None, False: ratings}
                if ratings.a.start > comparison_value:
                    return {True: ratings, False: None}
                true_a_range = range(comparison_value + 1, ratings.a.stop)
                false_a_range = range(ratings.a.start, comparison_value + 1)
                return {True: Ratings(ratings.x, ratings.m, true_a_range, ratings.s),
                        False: Ratings(ratings.x, ratings.m, false_a_range, ratings.s)}
            else:
                if ratings.s.stop <= comparison_value + 1:
                    return {True: None, False: ratings}
                if ratings.s.start > comparison_value:
                    return {True: ratings, False: None}
                true_s_range = range(comparison_value + 1, ratings.s.stop)
                false_s_range = range(ratings.s.start, comparison_value + 1)
                return {True: Ratings(ratings.x, ratings.m, ratings.a, true_s_range),
                        False: Ratings(ratings.x, ratings.m, ratings.a, false_s_range)}

    
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

initial_ratings = Ratings(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
in_workflow_copy = workflows['in'].copy()
workflow_condition_list = [(in_workflow_copy, in_workflow_copy.pop(0), initial_ratings)]
score = 0
while workflow_condition_list:
    current_workflow, current_workflow_condition, state = workflow_condition_list.pop(0)
    results = current_workflow_condition.branch(state)
    if results[True]:
        if current_workflow_condition.on_passed == 'A':
            score += results[True].score()
        elif current_workflow_condition.on_passed != 'R':
            next_workflow = workflows[current_workflow_condition.on_passed].copy()
            workflow_condition_list.append((next_workflow, next_workflow.pop(0), results[True]))
    if results[False]:
        workflow_condition_list.append((current_workflow, current_workflow.pop(0), results[False]))

print(score)
