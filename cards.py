import textwrap
# this file just contains some helper functions
# to help write cards.
card_infos = []

class CardSet:
    
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.wrapper = textwrap.TextWrapper(width=37)
        self.card_infos = []

    def defix_links(self, text):
        new_text = ""
        state = 'normal'
        for c in text:

            if c == '[':
                state = 'link'

            if c == ']':
                state = 'normal'
            
            if state == 'normal':
                new_text += c
            
            if state == 'link':
                new_text += c if c != '_' else ' '

        return new_text

    def fix_links(self, text):
        new_text = ""
        state = 'normal'
        for c in text:

            if c == '[':
                state = 'link'

            if c == ']':
                state = 'normal'
            
            if state == 'normal':
                new_text += c
            
            if state == 'link':
                new_text += c if c != ' ' else '_'

        return new_text

    def add_card(self, card_name, text, tags, decks=None, flavour=None, costs=None):
        global card_infos
        splitlines = text.split('\n\n')
        line_count = 0
        segments = []
        for subline in splitlines:
            line_count += 1
            fixed_subline = self.fix_links(subline)
            textlist = self.wrapper.wrap(text=fixed_subline)
            line_count += len(textlist)
            textlist_join = '\n'.join(textlist)
            segment = self.defix_links(textlist_join)
            segments.append(segment)
        line_count -= 1

        text_inner = "\n \n".join(segments)
        card_info = {
                "decks": [self.deck_name],
                "name": card_name,
                "text": text_inner,
                "line_count": line_count,
                "tags": tags,
            }
        if costs is not None:
            card_info["costs"]={
                "ap": costs[0],
                "energy": costs[1],
            }
        if flavour is not None:
            card_info['flavour'] = flavour
        card_infos.append(card_info)
        self.card_infos.append(card_info)

default_cost = (2, 2)

def find_card(card_name):
    # first find exact match
    for card_info in card_infos:
        if card_name == card_info['name']:
            return card_info

    # then case insensitive
    for card_info in card_infos:
        if card_name.lower() == card_info['name'].lower():
            return card_info
    
    # then do contains
    for card_info in card_infos:
        if card_name.lower() in card_info['name'].lower():
            print(f"!!WARNING!! looking for {card_name}, fuzzy matched to {card_info['name']}")
            return card_info
    return None

ranger_set = CardSet('ranger')
tanky_set = CardSet('tanky')
support_set = CardSet('support')
speedy_set = CardSet('speedy')
misc_set = CardSet('misc')

ranger_set.add_card(
    "Bowshot", # Intrinsic
    "Range 4: Deal 3 Damage\n\n(Intrinsic)"
    ,costs=(2,0)
    ,tags=['attack.melee', 'backstab']
)

ranger_set.add_card(
    "Sharp Shot", 
    "Range 4: Deal 5 Damage.",
    flavour = '"Take aim and pull, let the shot come as a surprise."'
    ,costs=(2,2)
    ,tags=['attack','range', 'projectile']
)

ranger_set.add_card(
    "First Aid!", 
    "Heal for 4 health.",
    flavour="The first thing any ranger learns is how to take care of themself."
    ,costs=(3,2)
    ,tags=['heal', 'technique']
)

ranger_set.add_card(
    "Binding Shot", 
    "Range 4: Deal 2 damage, the target is [slowed] for their next turn.",
    flavour="Quite simple, you can fire arrows with ropes on them"
    ,costs=(2,2)
    ,tags=['attack','range', 'malignant', 'projectile']
)

misc_set.add_card(
    "Status: Slowed",
    "This target has reduced movement speed, all movement is cut in half.",
    flavour="Slow and steady might win the race but it rarely wins any fights."
    ,tags=['status', 'negative']
)

bomb_trap_dmg = '6'
ranger_set.add_card(
    "Place Bomb trap", 
    f"Range 1: Place a {bomb_trap_dmg} damage [Bomb Trap] into an empty square.",
    flavour="gunpowder, rope, a pin, and a splash of wild magic."
    ,costs=(1,2)
    ,tags=['technique', 'ranged', 'summon']
)

misc_set.add_card(
    "Contraption: Bomb Trap",
    "Detonates when an enemy steps onto this square or an adjacent square."
    f"\n\nDeals {bomb_trap_dmg} damage to all characters in range.\nAllies take half damage."
    ,flavour="A bit of a lost art, making bombs. I wonder why they outlawed it."
    ,tags=['minion', 'immobile']
)

crossbow_turret_damage = '3'
cbt_range = '3'
ranger_set.add_card(
    "Place Crossbow Turret", 
    f"Range 1: Place a {crossbow_turret_damage} damage [Crossbow Turret] into an empty square."
    ,costs=(2,3)
    ,tags=['technique', 'ranged', 'summon']
)

ranger_set.add_card(
    "Crossbow Turret Shot",
    f"Range {cbt_range}: deal {crossbow_turret_damage}"
    ,tags=['ranged', 'attack', 'projectile']
)
misc_set.add_card(
    "Contraption: Crossbow Turret",
    f"Once per turn this turret fires at an enemy within {cbt_range} range for {crossbow_turret_damage}."
    ,tags=['ranged_attacker', 'minion']
)

# ==================================

speedy_set.add_card(
    "Dash", # Intrinsic
    "Technique: Move 4\n\n(Intrinsic, Exhaust)"
    ,costs=(2,0)
    ,tags=['attack.melee', 'backstab']
)

speedy_set.add_card(
    "Aimed Strike",
    "Melee: Deal 4 damage, deal an extra 2 if attacking from "
    "the flank"
    ,flavour="Cut them from behind, it'll hurt more."
    ,costs=(2,2)
    ,tags=['attack', 'melee' , 'backstab']
)

speedy_set.add_card(
    "Parting Strike",
    "Melee: Deal 3 damage, Move 2"
    ,flavour="Strike! then vanish."
    ,costs=(2,2)
    ,tags=['attack', 'melee', 'movement']
)

speedy_set.add_card(
    "Blur",
    "Gain 2 [Blurry]",
    flavour="Whoosh!"
    ,costs=(0,2)
    ,tags=['technique', 'buff']
)

misc_set.add_card(
    "Blurry",
    "Blocks damage, blur stacks and is persistent.",
    flavour="Can't hit what you can't hit."
    ,tags=['status', 'positive', 'barrier']
)

speedy_set.add_card(
    "Shuriken",
    "Range 2: Deal 3 damage, deal an extra 2 if attacking "
    "from the flank",
    flavour="It's not always a throwing star. Sometimes it's sharp rocks, or a bucket."
    ,costs=(2,2)
    ,tags=['attack', 'range', 'backstab']
)

speedy_set.add_card(
    "Assassinate",
    "Melee: Destroy all block, then deal 10. I must be flanking the target."
    ,costs=(2,2)
    ,tags=['attack', 'melee', 'backstab']
)

speedy_set.add_card(
    "Shadow break",
    "Melee: deal 3 damage for each stack of [Blurry], lose all stacks of [Blurry]."
    ,costs=(2,2)
    ,tags=['attack', 'melee']
)

# ----------- tanky cards ------------

tanky_set.add_card(
    "Slash", # Intrinsic for tanky
    "Melee: Deal 3 damage to target\n\n(Intrinsic)"
    ,costs=(2,0)
    ,tags=['attack', 'melee']
)

tanky_set.add_card(
    "Heavy Strike",
    "Melee: Deal 6 damage, deal an extra 2 damage if they have block.",
    flavour="\"SMASH!\"- some green dude once."
    ,costs=(2,2)
    ,tags=['attack.melee']
)

tanky_set.add_card(
    "Sunder arms",
    "Melee: Deal 2 damage, target has card draw reduced by 1 for the next turn.",
    flavour="This technique was developed in order to win arm wrestling competitions."
    ,costs=(2,2)
    ,tags=['attack.melee', 'malignant']
)

tanky_set.add_card(
    "Shields Up!",
    "Technique: Gain 6 block",
    flavour="\"Bet you can't hurt me now bro!\" - local man, moments before disaster."
    ,costs=(1,2)
    ,tags=['attack.melee', 'malignant']
)

tanky_set.add_card(
    "Get behind me!",
    "Battlecry: All allies in my flank,\ntake half damage for 1 turn.",
    flavour="\"Aw geez, We better do what he says Rick.\""
    ,costs=(1,2)
    ,tags=['technique', 'battlecry', 'support', 'aoe', 'protect']
)

tanky_set.add_card(
    "Slayer's Soul",
    "Battlecry: Replace one of my Intrinsic cards with [Rip and tear] \n\n(Expend)",
    flavour="The only thing they fear is you."
    ,costs=(4,4)
    ,tags=['technique', 'battlecry']
)
tanky_set.add_card(
    "Rip and Tear",
    "Melee: Deal 4 damage twice."
    ,costs=(2, 1)
    ,tags=['melee', 'attack']
)

tanky_set.add_card(
    "Buff: Undeniable",
    "Automatically deal 3 damage to any enemy that moves in an adjacent square. Nearby enemies must spend an extra AP to start their normal movement."
    ,tags=['buff', 'attack', 'melee', 'stance']
)

tanky_set.add_card(
    "Buff: Unbreakable",
    "Reduce all incoming damage by 1."
    ,tags=['buff', 'attack', 'melee', 'stance']
)


tanky_set.add_card(
    "Champion's Stance",
    "Stance (Expend): Gain [Unbreakable] and [Undeniable].",
    flavour="This is the apex of what it means to become a warrior"
    ,costs=(4,4)
    ,tags=['stance', 'expend', 'buff']
)

misc_set.add_card(
    "Block",
    "Blocks damage, disappears at the end of the turn.",
    flavour="I want you to hit me as hard as you can."
    ,tags=['status', 'buff']
)

# ------------- Support cards --------------

support_set.add_card(
    "Invoke wisdom", # Intrinsic
    "Place one card from your hand to the top of your deck.\n\n (Intrinsic, Exhaust)" 
    ,costs=(2,2) 
    ,tags=['technique']
)

support_set.add_card(
    "Healing Touch", # Intrinsic
    "Range 1: Heal target for 4 hp.\n\n (Intrinsic, Exhaust)" 
    ,costs=(2,2) 
    ,tags=['touch', 'spell', 'heal']
)

support_set.add_card(
    "Energy Bolt",
    "Ranged 3: Deal 3 damage",
    flavour="Quick as lightning"
    ,costs=(0,2)
    ,tags=['spell', 'attack']
)

support_set.add_card(
    "Mending Bolt",
    "Ranged 3: Heal 4 to target",
    flavour="\"Na na na na Poly! na na na Sporin!\""
    ,costs=(2,2)
    ,tags=['spell', 'heal', 'beneficial']
)

support_set.add_card(
    "Motivate",
    "Ranged 2: Target's next activation will draw 2 extra cards.",
    flavour="You can do it!"
    ,costs=(3,3)
    ,tags=['spell', 'beneficial']
)

support_set.add_card(
    "Stamina Surge",
    "Range 3: Target starts their next turn with 8 AP.",
    flavour="\"Oh my god he just ran right in.\"- local man, moments before disaster."
    ,costs=(2,2)
    ,tags=['spell', 'beneficial']
)

support_set.add_card(
    "Hidden potential",
    "Range 3 (Expend): Target adds a new card that they're compatible with."
    ,costs=(6, 5)
    ,tags=['spell', 'beneficial']
)

support_set.add_card(
    "Circle of Healing",
    "Radius 3: Heal all allies in radius for 4"
    ,costs=(4,4)
    ,tags=['spell', 'beneficial', 'aoe', 'radius']
)

support_set.add_card(
    "Energy Aura",
    "Spell (Expend):While the caster is alive, all allies gain an additional energy point per turn."
    ,costs=(6,6)
    ,tags=['spell', 'beneficial', 'global', 'aura']
)

