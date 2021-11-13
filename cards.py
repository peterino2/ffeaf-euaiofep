
import textwrap

# this file just contains some helper functions
# to help write cards.

card_infos = []

class Deck:
    
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

    def add_card(self, card_name, text, decks=None, flavour=None):
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
            }
        if flavour is not None:
            card_info['flavour'] = flavour
        card_infos.append(card_info)
        self.card_infos.append(card_info)

ranger_deck = Deck('ranger')
tanky_deck = Deck('tanky')
support_deck = Deck('support')
speedy_deck = Deck('speedy')
misc_deck = Deck('misc')

ranger_deck.add_card(
    "Sharp Shot", 
    "Range 4: Deal 3 + 1d4 Damage.",
    flavour = '"Take aim and pull, let the shot come as a surprise."',
)

ranger_deck.add_card(
    "First Aid!", 
    "Range self: Heal for 3 + 1d3 health.",
    flavour="The first thing any ranger learns is how to take care of themself."
)

ranger_deck.add_card(
    "Binding Shot", 
    "Range 4: Deal 2 damage, the target is [slowed] for their next turn.",
    flavour="Quite simple, you can fire arrows with ropes on them"
)

misc_deck.add_card(
    "Status: Slowed",
    "This target has reduced movement speed, all movement is cut in half.",
    flavour="Slow and steady might win the race but it rarely wins any fights."
)

bomb_trap_dmg = '4 + d4'
ranger_deck.add_card(
    "Place Bomb trap", 
    f"Range 1: Place a {bomb_trap_dmg} damage [Bomb Trap] into an empty square.",
    flavour="gunpowder, rope, a pin, and a splash of wild magic."
)

misc_deck.add_card(
    "Contraption: Bomb Trap",
    "Detonates when an enemy steps onto this square or an adjacent square."
    f"\n\nDeals {bomb_trap_dmg} damage to all characters in range.\nAllies take half damage.",
    flavour="A bit of a lost art, making bombs. I wonder why they outlawed it."
)

speedy_deck.add_card(
    "Aimed Strike",
    "Melee: Deal 3 + 1d6 damage, deal an extra 1d4 if attacking from "
    "the flank",
    flavour="Cut them from behind, it'll hurt more.",
)

speedy_deck.add_card(
    "Parting Strike",
    "Melee: Deal 1 + 1d3 damage, Move 2",
    flavour="Strike! then vanish."
)

speedy_deck.add_card(
    "Blur",
    "Move 2, Gain 1 + 1d2 [Blur]",
    flavour="Whoosh!"
)

misc_deck.add_card(
    "Blurry",
    "Blocks damage, blur stacks and is persistent.",
    flavour="Can't hit what you can't hit."
)

speedy_deck.add_card(
    "Shuriken",
    "Range 2: Deal 3 + 1d3 damage, deal an extra 1d4 if attacking "
    "from the flank",
    flavour="It's not always a throwing star. Sometimes it's sharp rocks, or a bucket."
)

# ----------- tanky cards ------------

tanky_deck.add_card(
    "Heavy Strike",
    "Melee: Deal 3 + 1d6 damage, ends turn.",
    flavour="\"SMASH!\"- some green dude once."
)

tanky_deck.add_card(
    "Shields Up!",
    "Gain 4 + 1d4 block",
    flavour="\"Bet you can't hurt me now bro!\" - local man, moments before disaster."
)

tanky_deck.add_card(
    "Get behind me!",
    "All allies in my flank,\ntake half damage for 1 turn.",
    flavour="\"Aw geez, We better do what he says Rick.\""
)

tanky_deck.add_card(
    "Sunder arms",
    "Melee: Deal 2 damage, target has card draw reduced by 2 for the next turn.",
    flavour="This technique was developed in order to win arm wrestling competitions."
)

# ------------- Support cards --------------
support_deck.add_card(
    "Energy Bolt",
    "Ranged 2: Deal 2 + 1d4 damage",
    flavour="This won't hurt a bit... no seriously this really wont hurt."
)

support_deck.add_card(
    "Mending Bolt",
    "Ranged 2: Heal for 2 + 1d4",
    flavour="\"Na na na na Poly! na na na Sporin!\""
)

support_deck.add_card(
    "Motivate",
    "Ranged 2: target's next activation will draw 3 extra cards.",
    flavour="Oh damn someone cute's watching, don't mess up."
)

support_deck.add_card(
    "Stamina Surge",
    "Range 2: target's movement increases by 2 for 2 turns.",
    flavour="\"Oh my god he just ran right in.\"- local man, moments before disaster."
)
