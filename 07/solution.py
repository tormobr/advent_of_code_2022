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
    # Part 1 solution : 
    def part_1(self):
        directories = self.build_tree()

        sizes = [self.dfs(key, directories) for key in directories.keys()]
        return sum(s for s in sizes if s <= 100000)

    # Part 2 solution : 
    def part_2(self):
        directories = self.build_tree()

        total_space = 70000000
        required = 30000000

        total_used = self.dfs("//", directories)
        not_used = total_space - total_used
        to_be_freed = required - not_used

        sizes = [self.dfs(key, directories) for key in directories.keys()]
        return min(s for s in sizes if s >= to_be_freed)

    def build_tree(self):
        data = read_lines("input.txt", f=str)

        directories = defaultdict(lambda: defaultdict(list))
        current_dir = ""
        index = 0

        while index < len(data):
            command = data[index]

            output = self.get_output(data, index)

            if self.check_command(command, "cd"):
                # handle_cd(command, directories, output, current_dir)
                args = self.get_args(command)
                if args == "..":
                    current_dir = "/".join(current_dir.split("/")[:-2]) + "/"
                else:
                    current_dir += args + "/"
            elif self.check_command(command, "ls"):
                # handle_ls(directories, output, current_dir)
                for out in output:
                    if self.is_dir(out):
                        directories[current_dir]["dirs"].append(current_dir + out.split()[1] + "/")
                    else:
                        directories[current_dir]["files"].append(self.get_file(out))

            index += len(output) + 1

        return directories

    def handle_ls(self, directories, output):
        for out in output:
            if self.is_dir(out):
                directories[current_dir]["dirs"].append(current_dir + out.split()[1] + "/")
            else:
                directories[current_dir]["files"].append(self.get_file(out))

    def handle_cd(self, directories, output):
        args = get_args(command)
        if args == "..":
            current_dir = "/".join(current_dir.split("/")[:-2]) + "/"
        else:
            current_dir += args + "/"




    def dfs(self, current_dir, directories):
        files = directories[current_dir]["files"]

        total = 0
        for size, filename in files:
            total += size

        for child in directories[current_dir]["dirs"]:
            total += self.dfs(child, directories)

        return total


    def get_output(self, data, index):
        command = data[index]
        i = index + 1
        out = []
        while i < len(data) and not self.is_command(data[i]):
            out.append(data[i])
            i += 1

        return out

    def get_file(self, s):
        size, name = s.split()
        return int(size), name

    def is_dir(self, s):
        return s.split()[0] == "dir"

    def check_command(self, command, match):
        return command.split()[1] == match

    def get_args(self, s):
        return s.split()[-1]

    def is_command(self, s):
        return s[0] == "$"

if __name__ == "__main__":
    shell = shell()
    pretty_print(shell.part_1(), shell.part_2())
