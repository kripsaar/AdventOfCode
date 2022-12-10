import os
from datetime import date

def create(day_number: int):
    date_string = f'{day_number:02d}-12'
    os.mkdir(date_string)
    open(date_string + '/part_one.py', mode='a').close()
    open(date_string + f'/input-{day_number:02d}', mode='a').close()
    open(date_string + f'/input-{day_number:02d}-test', mode='a').close()


today = date.today()

create(today.day)