def read_input(filename: str):
    sum = 0
    with open(filename, mode='r') as file:
        for line in file.readlines():
            first_digit = None
            second_digit = None
            for char in line:
                if not char.isdigit():
                    continue
                if first_digit is None:
                    first_digit = char
                second_digit = char
            number = int(first_digit + second_digit)
            print(number)
            sum += number
    print()
    print(sum)

read_input("input-01")