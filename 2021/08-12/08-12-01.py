def parse_input(filename: str):
    outputs = []
    with open(filename, mode="r") as input:
        for line in input:
            outputs.append(line.split("|")[1].strip().split(" "))
    return outputs

outputs = parse_input("input-08")
targets = [2, 3, 4, 7]
count = 0
for output in outputs:
    for item in output:
        if len(item) in targets:
            count += 1

print(count)
