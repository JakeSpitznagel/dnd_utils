#!/usr/bin/python3.7
import sys

from random import randint
from dataclasses import dataclass
from re import split
from typing import List

def print_help():
    print('expects command line arguments of the form xdy[+z] or optional flags: -[per-roll, help, dist]')
    print('per-roll applies the mod to every roll rather than the total')
    print('dist generates a hitogram of the distribution of values for the given rolls')


def d(times, val, mod=0, flags=[]):
    results = []
    for _ in range(times):
        randval = randint(1, val) + mod if 'per-roll' in flags else randint(1, val)
        results.append(randval)
    if 'per-roll' in flags:
        mod = 0
    return sum(results) + mod, results


# we need to parse out multiroll strings
# then call d(x, y) for each roll
# new data type should be dataclass?
@dataclass
class roll_set:
    rolls: List[any]
    mod: int = 0

@dataclass
class roll:
    count: int
    die: int

def parse_roll(roll_str: str):
    if 'd' in roll_str:
        num, die = roll_str.split('d')
        return roll(int(num) if num != '' else 1, int(die))
    return roll(int(roll_str), 1)

def parse_rolls(roll_str: str) -> str:
    mods = []
    for c in roll_str:
        if c == '+' or c == '-':
            mods.append(c)
    vals = split('\+|-', roll_str)
    rolls = [parse_roll(roll) for roll in vals]


def parse_args():
    '''
        parse args of the form xdy+z into a list of lists of the form [[x1, y1, z1], ..., [xn, yn, zn]]
    '''
    args = []
    flags = []
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            flags.append(arg.lstrip('-'))
            continue
        mod = 0
        parse_rolls(arg)
        if '+' in arg:
            arg, mod = arg.split('+')
        elif '-' in arg:
            arg, mod = arg.split('-')
            mod = '-' + mod
        args.append([int(x) for x in arg.split('d')] + [int(mod)])
    return args, flags


if __name__ == '__main__':
    args, flags = parse_args()
    if 'help' in flags:
        print_help()
        sys.exit()

    if 'dist' in flags:
        from dist import export_plot

    total = 0
    result_list = []
    for arg in args:
        if 'dist' in flags:
            num, die, mod = arg[0], arg[1], arg[2]
            export_plot(num, die, f'plot{num}d{die}plus{mod}.png', mod=mod, per_roll='per-roll' in flags)
        result, rolls = d(*arg, flags=flags)
        total += result
        mod = f'{arg[2]:+}' if arg[2] != 0 else ''
        roll_str = f'({[f"{roll - arg[2]} {mod}".rstrip() for roll in rolls]})' if 'per-roll' in flags else f'({rolls})'
        result_list.append(f'{arg[0]}d{arg[1]}{mod}: {result} ' + roll_str)
    print(*result_list, sep='\n')
    print(f'total: {total}')
