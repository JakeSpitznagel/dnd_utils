#!/usr/bin/python3.7

from roll import d
from random import randint
from sys import argv
from functools import wraps
from argparse import ArgumentParser


DC = 23
MOD = 15
LEVEL = 20


def roll(num, die, mod=0):
    return d(num, die, mod)[0]


def spell(func):
    func.is_spell = True
    return func


def cantrip(func):
    @wraps(func)
    @spell
    def f(upcast):
        if LEVEL >= 17:
            mult = 4
        elif LEVEL >= 11:
            mult = 3
        elif LEVEL >= 5:
            mult = 2
        else:
            mult = 1
        func(mult)
    return f


@cantrip
def firebolt(mult):
    """
    You hurl a mote of fire at a creature or object within range. Make a ranged spell attack against the target.
    On a hit, the target takes 1d10 fire damage. A flammable object hit by this spell ignites if it isn’t being worn or carried.
    """
    print(f'to hit: {roll(1, 20, MOD)}, fire damage: {roll(mult, 10)}')


@cantrip
def shocking_grasp(mult):
    """
    Lightning springs from your hand to deliver a shock to a creature you try to touch.
    Make a melee spell attack against the target. You have advantage on the attack roll if the target is wearing armor made of metal. 
    On a hit, the target takes 1d8 lightning damage, and it can’t take reactions until the start of its next turn.
    """
    print(f'to hit: {roll(1, 20, MOD)}, lightning damage: {roll(mult, 8)}, no reactions until it\'s next turn')


@cantrip
def shadow_missile(mult):
    """
    You create a shadowy dart of magical force. The dart hits a creature of your choice that you can see within range. 
    The dart deals 1d4 + 1 force damage to its target. The darts all strike simultaneously, and you can direct them to hit one creature or several.
    """
    print(f'Force damage: {roll(mult, 4, mult)}')


@cantrip
def mind_blast(mult):
    """
    You blast a target\'s mind that you can see within range, attempting to shatter it\'s intellect.
    The target must make a Wisdom saving throw. On a failed save they take 1d10 psychic damage.
    The damage increases when you reach higher levels: 2d8 at 5th, 3d8 at 11th, 4d8 at 17th.
    """
    print(f'save: WIS, DC: {DC}, psychic damage: {roll(mult, 10)}')


@spell
def fireball(upcast=None):
    """
    A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame.
    Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw.
    A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one.
    The fire spreads around corners. It ignites flammable objects in the area that aren’t being worn or carried.
    At Higher Levels: When you cast this spell using a spell slot of 4th level or higher, the damage increases by 1d6 for each slot level above 3rd.
    """
    upcast_mod = upcast - 3 if upcast is not None and upcast > 3 else 0
    print(f'save: DEX, DC: {DC}, fire damage: {roll(8 + upcast_mod, 6)}, AOE: 20ft radius')


@spell
def hold_person(upcast=None):
    """
    Choose a humanoid that you can see within range. The target must succeed on a Wisdom saving throw or be paralyzed for the duration.
    At the end of each of its turns, the target can make another Wisdom saving throw. On a success, the spell ends on the target.
    At Higher Levels: When you cast this spell using a spell slot of 3rd level or higher, you can target on additional humanoid for each slot level above 2nd.
    The humanoids must be within 30 feet of each other when you target them.
    """
    print(f'save: WIS, DC: {DC}, paralyzed for up to one minute conc. can make another saving throw at the end of it\'s turns')


if __name__ == '__main__':
    try:
        argv[1] = argv[1].replace(' ', '_')  # allow for quotes with spaces or underscores eg. 'hold person' or hold_person
    except IndexError:
        pass
    spell_list = [i.__name__ for i in list(locals().values()) if(hasattr(i, 'is_spell'))]

    parser = ArgumentParser()
    parser.add_argument('spell_name', choices=spell_list)
    parser.add_argument('--upcast', choices=[i for i in range(2, 10)], type=int)
    parser.add_argument('--desc', action='store_true')
    args = parser.parse_args()

    _spell = locals()[args.spell_name]
    if args.desc:
        print(_spell.__doc__)
    else:
        try:
            _spell(args.upcast)
        except TypeError:
            print('Cantrips cannot be upcast')

