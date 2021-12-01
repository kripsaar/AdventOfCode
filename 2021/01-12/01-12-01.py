increase_count = 0
with open('input-01', mode='r') as input:
    last_value = 9999999
    for row in input:
        if int(row) > last_value:
            increase_count += 1
        last_value = int(row)

print(increase_count)