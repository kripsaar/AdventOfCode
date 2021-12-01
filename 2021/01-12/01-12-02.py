increase_count = 0
with open('input-01', mode='r') as input:
    previous_sum = None
    first_value = None
    second_value = None
    third_value = None
    for row in input:
        first_value = second_value
        second_value = third_value
        third_value = int(row)
        if first_value is None:
            continue
        current_sum = first_value + second_value + third_value
        if previous_sum is not None:
            if current_sum > previous_sum:
                increase_count += 1
        previous_sum = current_sum

print(increase_count)