#!/usr/bin/python3.7

from roll import d
from random import randint
from functools import wraps


DC = 16
MOD = 8
LEVEL = 6
ABILITY = 5


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
def shadow_blade(upcast=None):
    """
    2nd level illusion
    Casting time: 1 Bonus Action
    Range: Self
    Components: V, S
    Duration: Concentration, up to 1 minute
    
    You weave together threads of shadow to create a sword of solidified gloom in your hand. This magic sword lasts until the spell ends.
    It counts as a simple melee weapon with which you are proficient. It deals 2d8 psychic damage on a hit and has the finesse, light, and thrown properties (range 20/60).
    In addition, when you use the sword to attack a target that is in dim light or darkness, you make the attack roll with advantage.
    If you drop the weapon or throw it, it dissipates at the end of the turn. Thereafter, while the spell persists, you can use a bonus action to cause the sword to reappear in your hand.

    At higher level
    3rd or 4th: 3d8
    5th or 6th: 4d8
    7th+: 5d8
    """
    print(shadow_blade.__doc__)

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


@spell
def sleep(upcast=None):
    """
    Sleep
    1st-level enchantment
    Casting Time: 1 action
    Range: 90 feet
    Components: V, S, M (a pinch of fine sand, rose petals, or a cricket)
    Duration: 1 minute
    
    This spell sends creatures into a magical slumber.
    Roll 5d8; the total is how many hit points of creatures this spell can affect.
    Creatures within 20 feet of a point you choose within range are affected in ascending order of their current hit points (ignoring unconscious creatures).

    Starting with the creature that has the lowest current hit points, each creature affected by this spell falls unconscious until the spell ends, 
    the sleeper takes damage, or someone uses an action to shake or slap the sleeper awake.
    Subtract each creature's hit points from the total before moving on to the creature with the next lowest hit points.
    A creature's hit points must be equal to or less than the remaining total for that creature to be affected.

    Undead and creatures immune to being charmed aren't affected by this spell.

    At Higher Levels.
    When you cast this spell using a spell slot of 2nd level or higher, roll an additional 2d8 for each slot level above 1st.
    """
    upcast_mod = upcast - 1 if upcast is not None and upcast > 1 else 0
    print(f'Total health: {roll(5 + 2*upcast_mod, 8)}')

@spell
def healing_spirit(upcast=None):
    """
    Healling Spirit
    2nd-level Conjuration
    Casting time: 1 Bonus Action
    Range: 60 feet
    Components: V, S
    Duration: Concentration, up to 1 minute

    You call forth a nature spirit to soothe the wounded. The intangible spirit appears in a space that is a 5-foot cube you can see within range. 
    The spirit looks like a transparent beast or fey (your choice). Until the spell ends, whenever you or a creature you can see moves into the spirits 
    space for the first time on a turn or starts its turn there, you can cause the spirit to restore ld6 hit points to that creature (no action required). 
    The spirit can’t heal constructs or undead. As a bonus action on your turn, you can move the Spirit up to 30 feet to a space you can see.

    At higher levels.
    When you cast this spell using a spell slot of 3rd level or higher, the healing increases 1d6 for each slot level above 2nd.
    """
    print(healing_spirit.__doc__)

@spell
def ice_knife(upcast=None):
    """
    1st-level Conjuration
    Casting time: 1 Action
    Range: 60 feet
    Components: S, M (a drop of water or piece of ice)
    Duration: Instantaneous

    You create a shard of ice and fling it at one creature within range. Make a ranged spell attack against the target. 
    On a hit, the target takes 1d10 piercing damage. Hit or miss, the shard then explodes. 
    The target and each creature within 5 feet of the point where the ice exploded must succeed on a Dexterity saving throw or take 2d6 cold damage.
    
    At Higher Levels. 
    When you cast this spell using a spell slot of 2nd level or higher, the cold damage increases by 1d6 for each slot level above 1st.

    """
    print(ice_knife.__doc__)

@spell
def illusory_dragon(upcast=None):
    """
    8th-level Illusion
    Casting time: 1 Action
    Range: 120 feet
    Components: S
    Duration: Concentration, up to 1 minute
    
    By gathering threads of shadow material from the Shadowfell, you create a Huge shadowy dragon in an unoccupied space that you can see within range. 
    The illusion lasts for the spell’s duration and occupies its space, as if it were a creature.
    
    When the illusion appears, any of your enemies that can see it must succeed on a Wisdom saving throw or become frightened of it for 1 minute. 
    If a frightened creature ends its turn in a location where it doesn’t have line of sight to the illusion, it can repeat the saving throw, ending the effect on itself on a success.
    As a bonus action on your turn, you can move the illusion up to 60 feet. 
    At any point during its movement, you can cause it to exhale a blast of energy in a 60-foot cone originating from its space. 
    
    When you create the dragon, choose a damage type: acid, cold, fire, lightning, necrotic, or poison.
    Each creature in the cone must make an Intelligence saving throw, taking 7d6 damage of the chosen damage type on a failed save, or half as much damage on a successful one.
    The illusion is tangible because of the shadow stuff used to create it, but attacks miss it automatically. 
    it succeeds on all saving throws, and it is immune to all damage and conditions. 
    A creature that uses an action to examine the dragon can determine that it is an illusion by succeeding on an Intelligence (Investigation) check against your spell save DC. 
    If a creature discerns the illusion for what it is, the creature can see through it and has advantage on saving throws against its breath.
    """
    print(illusory_dragon.__doc__)

@spell
def summon_shadow_spirit(upcast=None):
    """
    Summon Shadow Spirit
    3rd-level conjuration
    Casting Time: 1 action
    Range: 90 feet
    Components: V, S, M (tears inside a crystal vial worth at least 300 gp)
    Duration: Concentration, up to 1 hour

    You call forth a shadowy spirit from the Shadowfell. The spirit manifests physically in an unoccupied space that you can see within range. 
    This corporeal form uses the Shadow Spirit stat block below. When you cast the spell, choose an emotion: Fury, Despair, or Fear. 
    The creature physically resembles a misshapen humanoid marked by the chosen emotion, which also determines some of the traits in its stat block. 
    The creature disappears when it drops to 0 hit points or when the spell ends.

    The creature is friendly to you and your companions for the spell’s duration. 
    In combat, the creature shares your initiative count, but it takes its turn immediately after yours.
    It obeys verbal commands that you issue to it (no action required by you). If you don’t issue any, it defends itself but otherwise takes no action.

    At Higher Levels. When you cast this spell using a spell slot of 4th level or higher, the creature assumes the higher level for that casting wherever it uses the spell’s level in its stat block.

    Shadow Spirit
    Medium monstrosity, neutral evil
    Armor Class: 11 + the level of the spell (natural armor)
    Hit Points: equal the shadow’s Constitution modifier + your spellcasting ability modifier + ten times the spell’s level
    Speed: 40 ft.
    13 (+1) STR
    16 (+3) DEX
    15 (+2) CON
    4 (−4)  INT
    10 (+0) WIS
    16 (+3) CHA
    Damage Resistances: necrotic
    Condition Immunities: frightened
    Senses: darkvision 120 ft., passive Perception 10
    Languages: Common, understands the languages you speak
    
    Bloodthirsty Frenzy (Fury Only). The spirit has advantage on attack rolls against frightened creatures.
    Shadow Stealth (Fear Only). While in dim light or darkness, the spirit can take the Hide action as a bonus action.
    Weight of Ages (Despair Only). Any beast or humanoid, other than you, that starts its turn within 5 feet of the spirit has its speed reduced by 20 feet 
    until the start of that beast or humanoid’s next turn.
    
    Actions
    Multiattack. The spirit makes a number of attacks equal to half this spell’s level (rounded down).
    Chilling Rend. Melee Weapon Attack: +3 + the spell’s level to hit, reach 5 ft., one target. Hit: 2d8 + 3 + the spell’s level cold damage.
    Dreadful Scream (1/Day). The spirit screams. 
        Each creature within 30 feet of it must succeed on a Wisdom saving throw against your spell save DC or be frightened of the spirit for 1 minute. 
        The frightened creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success
    """
    print(summon_shadow_spirit.__doc__)

@spell
def minute_meteors(upcast=None):
    """
    3rd-level evocation
    Casting Time: 1 action
    Range: Self
    Components: V, S, M (niter, sulfur, and pine tar formed into a bead)
    Duration: Concentration, up to 10 minutes

    You create six tiny meteors in your space. They float in the air and orbit you for the spell’s duration. 
    When you cast the spell — and as a bonus action on each of your turns thereafter — you can expend one or two of the meteors, 
    sending them streaking toward a point or points you choose within 120 feet of you. Once a meteor reaches its destination or impacts against a solid surface, the meteor explodes. 
    Each creature within 5 feet of the point where the meteor explodes must make a Dexterity saving throw. 
    A creature takes 2d6 fire damage on a failed save, or half as much damage on a successful one.

    At Higher Levels. When you cast this spell using a spell slot of 4th level or higher, the number of meteors created increases by two for each slot level above 3rd.
    """
    print(minute_meteors.__doc__)

melfs_minute_meteors = minute_meteors
