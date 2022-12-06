
def parse_input(filename: str):
    with open(filename, mode='r') as file:
        return file.readline().strip()

def is_start_marker(marker: str):
    return len(set(marker)) == 14

def find_message_start(buffer: str):
    size = len(buffer)
    start = 0
    end = 14
    while end <= size:
        if is_start_marker(buffer[start:end]):
            return end
        start += 1
        end += 1


filename = 'input-06'
buffer = parse_input(filename)
start = find_message_start(buffer)
print(start)
