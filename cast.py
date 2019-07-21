#!/usr/bin/python3.7
import gen_spells
import man_spells

from roll import d
from random import randint
from sys import argv
from functools import wraps
from argparse import ArgumentParser
from pprint import pprint


def get_spell_list():
    man_list = [i for i in man_spells.__dir__() if hasattr(getattr(man_spells, i), 'is_spell')]
    gen_list = [i for i in gen_spells.__dir__() if hasattr(getattr(gen_spells, i), 'is_spell')]
    
    man_list.extend(gen_list)
    spell_list = set(man_list)

    return list(spell_list)


if __name__ == '__main__':
    try:
        argv[1] = argv[1].replace(' ', '_')  # allow for quotes with spaces or underscores eg. 'hold person' or hold_person
    except IndexError:
        pass

    spell_list = get_spell_list()

    parser = ArgumentParser()
    parser.add_argument('spell_name')  # , choices=spell_list)
    parser.add_argument('--upcast', choices=[i for i in range(2, 10)], type=int)
    parser.add_argument('--desc', '-d', action='store_true')
    args = parser.parse_args()

    _spell = None
    if hasattr(man_spells, args.spell_name):
        _spell = getattr(man_spells, args.spell_name)
    elif hasattr(gen_spells, args.spell_name):
        _spell = getattr(gen_spells, args.spell_name)

    if _spell:
        if args.desc:
            print(_spell.__doc__)
        else:
            try:
                _spell(args.upcast)
            except TypeError:
                print('Cantrips cannot be upcast')
    else:
        print(f'Spell {args.spell_name} not found')
