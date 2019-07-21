#!/usr/bin/python3.7

from roll import d
from random import randint
from functools import wraps


DC = 23
MOD = 15
LEVEL = 20
ABILITY = 7


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
    cantrip evocation
    Casting Time: 1 action
    Range: 120 feet
    Components: V S
    Duration: Instantaneous
    Classes: Sorcerer, Wizard

    You hurl a mote of fire at a creature or object within range. Make a ranged spell attack against the target.
    On a hit, the target takes 1d10 fire damage. A flammable object hit by this spell ignites if it isn’t being worn or carried.
    """
    print(f'to hit: {roll(1, 20, MOD)}, fire damage: {roll(mult, 10)}')


@cantrip
def shocking_grasp(mult):
    """
    cantrip evocation
    Casting Time: 1 action
    Range: Touch
    Components: V S
    Duration: Instantaneous
    Classes: Sorcerer, Wizard

    Lightning springs from your hand to deliver a shock to a creature you try to touch.
    Make a melee spell attack against the target. You have advantage on the attack roll if the target is wearing armor made of metal. 
    On a hit, the target takes 1d8 lightning damage, and it can’t take reactions until the start of its next turn.
    """
    print(f'to hit: {roll(1, 20, MOD)}, lightning damage: {roll(mult, 8)}, no reactions until it\'s next turn')


@cantrip
def shadow_missile(mult):
    """
    cantrip evocation
    Casting Time: 1 action
    Range: 120 feet
    Components: V S
    Duration: Instantaneous
    Classes: Wizard - Shadowmancer

    You create a shadowy dart of magical force. The dart hits a creature of your choice that you can see within range. 
    The dart deals 1d4 + 1 force damage to its target. The darts all strike simultaneously, and you can direct them to hit one creature or several.
    """
    print(f'Force damage: {roll(mult, 4, mult)}')


@cantrip
def mind_blast(mult):
    """
    cantrip enchantment
    Casting Time: 1 action
    Range: 120 feet
    Components: V S
    Duration: Instantaneous
    Classes: Wizard - Shadowmancer

    You blast a target\'s mind that you can see within range, attempting to shatter it\'s intellect.
    The target must make a Wisdom saving throw. On a failed save they take 1d10 psychic damage.
    The damage increases when you reach higher levels: 2d8 at 5th, 3d8 at 11th, 4d8 at 17th.
    """
    print(f'save: WIS, DC: {DC}, psychic damage: {roll(mult, 10)}')


@spell
def shield(upcast=None):
    """
    1st level abjuration
    Casting Time: 1 reaction, which you take when you are hit by an attack or targeted by the magic missile spell
    Range: Self
    Components: V S
    Duration: 1 round
    Classes: Sorcerer, Wizard

    An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC,
    including against the triggering attack, and you take no damage from magic missile.

    """
    print(f'you gain +5 AC until the start of your next turn, unaffected by magic missile')


@spell
def find_familiar(upcast=None):
    """
    1 conjuration
    Casting Time: 1 hour
    Range: 10 feet
    Components: V S M (10 gp worth of charcoal, incense, and herbs that must be consumed by fire in a brass brazier)
    Duration: Instantaneous
    Classes: Wizard

    You gain the service of a familiar, a spirit that takes an animal form you choose:
    bat, cat, crab, frog (toad), hawk, lizard, octopus, owl, poisonous snake, fish (quipper), rat, raven, sea horse, spider, or weasel.
    Appearing in an unoccupied space within range, the familiar has the statistics of the chosen form, though it is a celestial, fey, or fiend (your choice) instead of a beast
    Your familiar acts independently of you, but it always obeys your commands. In combat, it rolls its own initiative and acts on its own turn.
    A familiar can’t attack, but it can take other actions as normal.

    When the familiar drops to 0 hit points, it disappears, leaving behind no physical form. It reappears after you cast this spell again
    While your familiar is within 100 feet of you, you can communicate with it telepathically.
    Additionally, as an action, you can see through your familiar’s eyes and hear what it hears until the start of your next turn,
    gaining the benefits of any special senses that the familiar has. During this time, you are deaf and blind with regard to your own senses.

    As an action, you can temporarily dismiss your familiar. It disappears into a pocket dimension where it awaits your summons.
    Alternatively, you can dismiss it forever. As an action while it is temporarily dismissed, you can cause it to reappear in any unoccupied space within 30 feet of you
    You can’t have more than one familiar at a time. If you cast this spell while you already have a familiar, you instead cause it to adopt a new form.
    Choose one of the forms from the above list. Your familiar transforms into the chosen creature.

    Finally, when you cast a spell with a range of touch, your familiar can deliver the spell as if it had cast the spell.
    Your familiar must be within 100 feet of you, and it must use its reaction to deliver the spell when you cast it.
    If the spell requires an attack roll, you use your attack modifier for the roll.
    """
    print(find_familiar.__doc__)


@spell
def misty_step(upcast=None):
    """
    2nd level conjuration
    Casting Time: 1 bonus action
    Range: Self
    Components: V
    Duration: Instantaneous
    Classes: Sorcerer, Warlock, Wizard

    Briefly surrounded by silvery mist, you teleport up to 30 feet to an unoccupied space that you can see.
    """
    print('You teleport up to 30 feet to an unoccupied space that you can see.')


@spell
def shadow_image(upcast=None):
    """
    2nd level illusion
    Casting Time: 1 action
    Range: Self
    Components: V S
    Duration: 1 minute
    Classes: Wizard - Shadowmancer

    Three shadowy duplicates of yourself appear in your space. Until the spell ends, the duplicates move with you and mimic your actions,
    shifting position so it’s impossible to track which image is real. You can use your action to dismiss the shadowy duplicates.

    Each time a creature targets you with an attack during the spell’s duration, roll a d20 to determine whether the attack instead targets one of your duplicates.
    If you have three duplicates, you must roll a 6 or higher to change the attack’s target to a duplicate.
    With two duplicates, you must roll an 8 or higher. With one duplicate, you must roll an 11 or higher.

    A duplicate’s AC equals 15 + DEX + INT. If an attack hits a duplicate, the duplicate is destroyed.
    A duplicate can be destroyed only by an attack that hits it. It ignores all other damage and effects. The spell ends when all three duplicates are destroyed.

    A creature is unaffected by this spell if it can’t see, if it relies on senses other than sight, such as blindsight, or if it can perceive illusions as false, as with truesight.

    When you make a melee attack against an enemy, all active duplicates make an attack with your spell attack mod, dealing 1d8 + INT psychic damage.
    """
    print(f'to hit: {[roll(1, 20) + MOD for _ in range(3)]}, psychic damage: {[roll(1, 8) + ABILITY for _ in range(3)]}')


@spell
def haunt(upcast=None):
    """
    8th level illusion
    Casting Time: 1 action
    Range: 60 feet
    Components: V S
    Duration: 1 hour
    Classes: Carn DuVrangr

    A shadow image spawns by each creature in range, including allies and the caster, haunts have 1hp and cannot be targetted with mental abilities.
    if fewer than 5 creatures are within range, 5 duplicates are spawned, with the additional spawned adjacent to the caster.
    Casting this spell additional times does not despawn the haunts.

    These illusions use all the statistics of the caster at the time of the casting. This illusion is able to take actions and cast spells, though cannot regain spell slots.
    They act simultaneously after the caster in initiative order.

    You can swap places with any active illusion at will.
    """
    print(haunt.__doc__)


@spell
def fireball(upcast=None):
    """
    3rd level evocation
    Casting Time: 1 action
    Range: 150 feet
    Components: V S M (A tiny ball of bat guano and sulfur)
    Duration: Instantaneous
    Classes: Sorcerer, Wizard

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
    2nd level enchantment
    Casting Time: 1 action
    Range: 60 feet
    Components: V S M (A small, straight piece of iron)
    Duration: Up to 1 minute
    Classes: Bard, Cleric, Druid, Sorcerer, Warlock, Wizard

    Choose a humanoid that you can see within range. The target must succeed on a Wisdom saving throw or be paralyzed for the duration.
    At the end of each of its turns, the target can make another Wisdom saving throw. On a success, the spell ends on the target.
    At Higher Levels: When you cast this spell using a spell slot of 3rd level or higher, you can target on additional humanoid for each slot level above 2nd.
    The humanoids must be within 30 feet of each other when you target them.
    """
    print(f'save: WIS, DC: {DC}, paralyzed for up to one minute conc. can make another saving throw at the end of it\'s turns')

