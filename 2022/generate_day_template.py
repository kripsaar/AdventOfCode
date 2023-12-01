import os
import requests
import sys
from datetime import date
from pathlib import Path

template = """

def parse_input(filename: str):

    with open(filename, mode = 'r') as file:
        return

filename = '{input_name}'
parse_input(filename)
"""

def create_input(date_string, day_number: int):
    url = f'https://adventofcode.com/2022/day/{day_number}/input'
    cookies = {'session': '53616c7465645f5f31f27679ada5b9aa8079618df16e8226c38868c10f045a6891a5d60b40246e54ade9d336bff140f358f7abefb2706ea8a496678b355ef82d'}
    response = requests.get(url, cookies=cookies)
    with open(date_string + f'/input-{day_number:02d}', mode='w') as input_file:
        input_file.write(response.text.rstrip('\n'))

def write_template(day_number: int, filename: str):
    if Path(filename).is_file():
        # Already exists, nothing to do
        return
    with open(filename, mode='a') as file:
        file.write(template.format(input_name=f'input-{day_number:02d}-test'))


def create(day_number: int):
    date_string = f'{day_number:02d}-12'
    os.makedirs(date_string, exist_ok=True)
    write_template(day_number, date_string + '/part_one.py')
    open(date_string + f'/input-{day_number:02d}-test', mode='a').close()
    create_input(date_string, day_number)

day_number = date.today().day 

if len(sys.argv) > 1 and sys.argv[1].isnumeric():
    day_number = int(sys.argv[1])

create(day_number)