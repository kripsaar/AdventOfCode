import os
import requests
import sys
from datetime import date

session_key = "SESSION_KEY_GOES_HERE"

def create_input(date_string, day_number: int):
    url = f'https://adventofcode.com/2023/day/{day_number}/input'
    cookies = {'session': session_key}
    response = requests.get(url, cookies=cookies)
    with open(date_string + f'/input-{day_number:02d}', mode='w') as input_file:
        input_file.write(response.text.rstrip('\n'))

def create(day_number: int):
    date_string = f'{day_number:02d}-12'
    os.mkdir(date_string)
    open(date_string + '/part_one.py', mode='a').close()
    open(date_string + f'/input-{day_number:02d}-test', mode='a').close()
    create_input(date_string, day_number)

day_number = date.today().day 

if len(sys.argv) > 1 and sys.argv[1].isnumeric():
    day_number = int(sys.argv[1])

create(day_number)