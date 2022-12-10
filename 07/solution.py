import math
from collections import deque, defaultdict
from functools import reduce
from operator import mul
import itertools
import numpy as np
import re

import sys
sys.path.insert(0,'..')
from advent_lib import *


class shell():
    def __init__(self):
        self.cwd = ""
        self.commands = {
            "cd": self.handle_cd,
            "ls": self.handle_ls
        }
        self.build_tree()

    # -------------------------------------------------------- Parsing ----------------------------------------------------------
    def build_tree(self):
        self.cwd = ""
        data = read_lines("input.txt", f=str)

        self.directories = defaultdict(lambda: defaultdict(list))

        index = 0
        while index < len(data):
            command = data[index]
            output = self.get_output(data, index)

            self.commands[self.get_command_str(command)](command, output)
            index += len(output) + 1 # index jump to next command

    def handle_ls(self, command, output):
        for out in output:
            is_dir = self.is_dir(out)

            key = "dirs" if is_dir else "files"
            to_add = self.move_dir_down(self.get_dir_info(out)) if is_dir else self.get_file_info(out)
            self.directories[self.cwd][key].append(to_add)

    def handle_cd(self, command, output):
        args = self.get_args(command)
        self.cwd = self.move_dir_up() if args[0] == ".." else self.move_dir_down(args[0])

    def move_dir_up(self):
        return "/".join(self.cwd.split("/")[:-2]) + "/"

    def move_dir_down(self, new_dir):
        new_current_dir = self.cwd + new_dir
        new_current_dir += "/" if new_current_dir != "/" else ""
        return new_current_dir

    def get_command_str(self, s):
        return s.split()[1]

    def get_output(self, data, index):
        command = data[index]
        i = index + 1
        out = []
        while i < len(data) and not self.is_command(data[i]):
            out.append(data[i])
            i += 1

        return out

    def get_dir_info(self, s):
        _, name = s.split()
        return name

    def get_file_info(self, s):
        size, name = s.split()
        return int(size), name

    def is_dir(self, s):
        return re.match("^dir", s)

    def get_args(self, s):
        return s.split()[2: ]

    def is_command(self, s):
        return re.match("^\$", s)

    # -------------------------------------------------------- Calculations ----------------------------------------------------------
    def get_all_dir_sizes(self):
        return [self.get_dir_size(key) for key in self.directories.keys()]

    def get_dir_size(self, current_dir):
        files_sizes = map(lambda x: x[0], self.directories[current_dir]["files"])
        dir_size = sum(size for size in files_sizes)

        for child in self.directories[current_dir]["dirs"]:
            dir_size += self.get_dir_size(child)

        return dir_size

if __name__ == "__main__":
    shell = shell()

    # Solution to part 1
    sizes = shell.get_all_dir_sizes()
    part1 = sum(s for s in sizes if s <= 100000)

    # Solution to part 2
    total_space = 70000000
    required = 30000000
    total_used = shell.get_dir_size("/")
    not_used = total_space - total_used
    to_be_freed = required - not_used
    part2 = min(s for s in sizes if s >= to_be_freed)

    pretty_print(part1, part2) 
