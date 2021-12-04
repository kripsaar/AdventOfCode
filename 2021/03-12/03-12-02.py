
def count_bits(list, column_index):
    bit_count = {0 : 0, 1 : 0}
    for line in list:
        bit_count[int(line[column_index])] += 1
    return bit_count

def reduce(lines_list, column_index, oxygen):
    bit_count = count_bits(lines_list, column_index)
    keep_char = ''
    if oxygen and bit_count[1] >= bit_count[0]:
        keep_char = '1'
    elif (not oxygen) and bit_count[1] < bit_count[0]:
        keep_char = '1'
    else:
        keep_char = '0'
    new_lines_list = []
    for line in lines_list:
        if line[column_index] == keep_char:
            new_lines_list.append(line)
    return new_lines_list

lines = []
line_length = 0
with open('input-03', mode='r') as input:
    first_line = input.readline().strip()
    line_length = len(first_line)
    input.seek(0)
    lines = input.read().splitlines()

oxygen_list = lines
scrubber_list = lines
for column_index in range(line_length):
    if len(oxygen_list) > 1:
        oxygen_list = reduce(oxygen_list, column_index, True)
    if len(scrubber_list) > 1:
        scrubber_list = reduce(scrubber_list, column_index, False)

oxygen_rating = oxygen_list[0]
scrubber_rating = scrubber_list[0]

print(f"Oxygen generator rating: {oxygen_rating}")
print(f"CO2 scrubber rating: {scrubber_rating}")
print(f"Product: {int(oxygen_rating, 2) * int(scrubber_rating, 2)}")
