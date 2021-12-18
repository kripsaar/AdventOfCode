import re
import textwrap

type_map = {4: "literal", 6: "operator"}
binary_to_packet = {}

class Packet:
    def __init__(self, binary: str, children: list = None):
        binary_to_packet[binary] = self
        self.binary = binary
        self.version = int(binary[0:3], 2)
        type_code = int(binary[3:6], 2)
        self.type = type_map[type_code] if type_code in type_map else "operator"
        self.content = binary[6:]
        self.children = children if children is not None else []
        self.value = 0
        self.length = 6
        self.parse_content()

    def __repr__(self) -> str:
        return self.binary

    def __str__(self) -> str:
        string = f"""{{
    Version: {self.version}
    Type: {self.type}"""
        if self.type == "literal":
            string += f"""
    Value: {self.value}
}}"""
        else:
            children_string = "\n".join([str(child) for child in self.children])
            string += f"""
    Children:
    [
{textwrap.indent(children_string, "        ")}
    ]
}}"""
        return string

    def calculate_version_sum(self):
        # print()
        # print(f"Sum calculation")
        # print()
        # print(f"Self: {self.binary}")
        # print(f"Children: {self.children}")
        # print()
        return self.version + sum([child.calculate_version_sum() for child in self.children])

    def get_content(self):
        if self.type == "literal":
            return self.parse_literal(self.content)
        else:
            return self.calculate_version_sum()

    def parse_content(self):
        if self.type == "literal":
            self.parse_literal()
        elif self.type == "operator":
            self.parse_operator()

    def parse_operator(self):
        length_id = int(self.content[0])
        content_offset = 1
        self.length += 1
        termination_condition = 0
        if length_id == 0:
            content_offset += 15
            self.length += 15
            termination_condition = int(self.content[1:16], 2)
        elif length_id == 1:
            content_offset += 11
            self.length += 11
            termination_condition = int(self.content[1:12], 2)
        content = self.content[content_offset:]
        while(len(content) > 0):
            child = Packet(content)
            self.length += child.length
            self.children.append(child)
            if length_id == 0:
                if sum([child.length for child in self.children]) >= termination_condition:
                    return
            if length_id == 1:
                if len(self.children) == termination_condition:
                    return
            content = content[child.length:]

    def parse_literal(self):
        chunks = re.findall(".{5}", self.content)
        result_binary = ""
        for chunk in chunks:
            to_continue = chunk[0]
            result_binary += chunk[1:]
            self.length += 5
            if to_continue == "0":
                break
        self.value = int(result_binary, 2)

def parse_input(filename: str):
    with open(filename, mode="r") as input:
        hex_string = input.read().strip()
        binary_length = len(hex_string) * 4
        binary = bin(int(hex_string, 16))[2:].zfill(binary_length)
        
        return binary

def run(filename: str):
    print(f"Running for filename {filename}")
    binary = parse_input(filename)
    print(f"Full binary: {binary}")
    outer_packet = Packet(binary)
    # print(outer_packet)
    print(f"Version sum: {outer_packet.get_content()}")

run("input-16-1")
run("input-16-2")
run("input-16-3")
run("input-16-4")

run("input-16")