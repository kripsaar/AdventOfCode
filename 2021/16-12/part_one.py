import re

type_map = {4: "literal", 6: "operator"}
literal_package_pattern = "^(?:.{3}(?:100(?:1.{4})*(?:0.{4})|.{3}0.{15}|.{3}1.{11}))+(.{3}100(?:1.{4})*(?:0.{4}))"
parent_package_pattern = ".*(.{3}(?!100).{3}(?:0.{15}|1.{11}).*[LITERAL].*)"
binary_to_packet = {}

class Packet:
    def __init__(self, binary: str, children: list = None, parent: object = None):
        binary_to_packet[binary] = self
        self.binary = binary
        self.version = int(binary[0:3], 2)
        type_code = int(binary[3:6], 2)
        self.type = type_map[type_code] if type_code in type_map else "operator"
        self.content = binary[6:]
        self.children = children if children is not None else []
        self.parent = parent
        if self.type != "literal":
            self.handle_operator()

    def calculate_version_sum(self):
        print()
        print(f"Sum calculation")
        print()
        print(f"Self: {self.binary}")
        print(f"Children: {self.children}")
        print()
        return self.version + sum([child.calculate_version_sum() for child in self.children])


    def get_content(self):
        if self.type == "literal":
            return self.parse_literal(self.content)
        else:
            return self.calculate_version_sum()

    def __repr__(self) -> str:
        return self.binary

    def __str__(self) -> str:
        return self.binary

    def parse_literal(self, binary: str):
        chunks = re.findall(".....", binary)
        result_binary = ""
        for chunk in chunks:
            to_continue = chunk[0]
            result_binary += chunk[1:]
            if to_continue == "0":
                break
        result = int(result_binary, 2)
        return result

    def find_smallest_parent(self, full_binary):
        parents = re.findall(parent_package_pattern.replace("[LITERAL]", self.binary), full_binary)
        if len(parents) == 0:
            return None
        parents.sort(key=len)
        return parents[0]

    def handle_operator(self):
        binary = self.content
        length_id = int(binary[0])
        literals = self.find_literal_subpackages(self.binary)
        print(f"Found literals: {literals}")
        binary_worklist = literals
        while len(binary_worklist) > 0:
            current_binary = binary_worklist.pop(0)
            current = binary_to_packet.setdefault(current_binary, Packet(current_binary))
            parent_binary = current.find_smallest_parent(self.binary)
            print(f"Current: {current_binary}")
            print(f"Parent: {parent_binary}")
            if parent_binary is not None:
                if self.binary.startswith(parent_binary):
                    self.children.append(current)
                else:
                    binary_worklist.append(parent_binary)
            if length_id == 0:
                sub_packets_length = int(binary[1:16], 2)
                if sum([len(child.binary) for child in self.children]) >= sub_packets_length:
                    return
            if length_id == 1:
                sub_packets_count = int(binary[1:12], 2)
                if len(self.children) == sub_packets_count:
                    return
        

    def find_literal_subpackages(self, binary: str):
        literals = []
        found_literals = re.findall(literal_package_pattern, binary)
        while len(found_literals) > 0:
            literal = found_literals[0]
            literals.append(literal)
            binary = binary[:binary.find(literal)]
            found_literals = re.findall(literal_package_pattern, binary)
        return literals


def parse_input(filename: str):
    with open(filename, mode="r") as input:
        hex_string = input.read().strip()
        binary_length = len(hex_string) * 4
        binary = bin(int(hex_string, 16))[2:].zfill(binary_length)
        
        return binary

binary = parse_input("input-16-test")
print(binary)
outer_packet = Packet(binary)
print(outer_packet.get_content())