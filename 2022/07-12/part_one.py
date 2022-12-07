from typing import List

class Dir:
    def __init__(self, path: str, subdirs = None, files = None, parent = None):
        self.path = path
        self.parent = parent
        if subdirs:
            self.subdirs = subdirs
        else: 
            self.subdirs = set()
        if files:
            self.files = files
        else:
            self.files = set()

    def __repr__(self) -> str:
        return self.path

    def add_subdir(self, subdir):
        self.subdirs.add(subdir)

    def add_file(self, filename: str, filesize: int):
        self.files.add((filename, filesize))

    def get_size(self) -> int:
        size = 0
        for filename, filesize in self.files:
            size += filesize
        for subdir in self.subdirs:
            size += subdir.get_size()
        return size

def parse_input(filename: str):
    all_dirs = {}
    with open(filename, mode='r') as file:
        path = ""
        curr_dir: Dir = None
        parent: Dir = None
        for line in file.readlines():
            line = line.strip()
            if line == '$ cd ..':
                curr_dir = parent
                path = curr_dir.path
                parent = curr_dir.parent
                continue
            elif line.startswith('$ cd'):
                parent = curr_dir
                path = '/' + (path + '/' + line[5:]).lstrip('/')
                if path in all_dirs:
                    curr_dir = all_dirs[path]
                else:
                    curr_dir = Dir(path, parent = parent)
                    all_dirs[path] = curr_dir
                continue
            elif line == '$ ls':
                continue
            elif line.startswith('dir'):
                dir_name = line[4:]
                dir_path = '/' + (path + '/' + dir_name).lstrip('/')
                subdir: Dir = None
                if dir_path in all_dirs:
                    subdir = all_dirs[dir_path]
                else:
                    subdir = Dir(dir_path, parent = curr_dir)
                    all_dirs[dir_path] = subdir
                curr_dir.add_subdir(subdir)
            else:
                filesize, filename = line.split(' ')
                curr_dir.add_file(filename, int(filesize))
    return all_dirs

def print_dir(dir: Dir):
    print('#########')
    print('dir path: ' + dir.path)
    print('dir subdirs: ' + str(dir.subdirs))
    print()

filename = 'input-07'
all_dirs = parse_input(filename)

for dir in all_dirs.values():
    print_dir(dir)

max_size = 100000
valid_dirs = set()
size_sum = 0
for dir in all_dirs.values():
    size = dir.get_size()
    print()
    print('size of ' + dir.path + ' = ' + str(size))
    if size < max_size:
        valid_dirs.add(dir.path)
        size_sum += size

print(valid_dirs)
print(size_sum)
