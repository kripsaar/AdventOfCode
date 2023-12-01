import re

digit_regex = "[0-9]|one|two|three|four|five|six|seven|eight|nine"

digit_dict = {"0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9", "one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9"}

def parse_digit(digit_str: str) -> str:
    return digit_dict[digit_str]

def read_input(filename: str):
    sum = 0
    with open(filename, mode='r') as file:
        for line in file.readlines():
            digits = re.findall(digit_regex, line)
            first_digit = digits[0]
            second_digit = digits[-1]
            number = int(parse_digit(first_digit) + parse_digit(second_digit))
            print(number)
            sum += number
    print()
    print(sum)

read_input("input-01")