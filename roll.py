#!/usr/bin/python3.7
import sys

from random import randint


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
            export_plot(num, die, f'plot{num}d{die}plus{mod}.png', mod=mod, per_roll='per_roll' in flags)
        result, rolls = d(*arg, flags=flags)
        total += result
        mod = f'{arg[2]:+}' if arg[2] != 0 else ''
        roll_str = f'({[f"{roll - arg[2]} {mod}".rstrip() for roll in rolls]})' if 'per-roll' in flags else f'({rolls})'
        result_list.append(f'{arg[0]}d{arg[1]}{mod}: {result} ' + roll_str)
    print(*result_list, sep='\n')
    print(f'total: {total}')
