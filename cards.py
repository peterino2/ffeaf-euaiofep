
import textwrap

# this file just contains some helper functions
# to help write cards.

card_infos = []

class Deck:
    
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.wrapper = textwrap.TextWrapper(width=37)

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

    def add_card(self, card_name, text):
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
        card_infos.append(
            {
                "deck": self.deck_name,
                "name": card_name,
                "text": text_inner,
                "line_count": line_count,
            }
        )

ranger_deck = Deck('ranger')
tanky_deck = Deck('tanky')
support_deck = Deck('support')
speedy_deck = Deck('speedy')
misc_deck = Deck('misc')

ranger_deck.add_card(
    "Sharp Shot", 
    "Range 4: Deal 3 + 1d4 Damage.",
)

ranger_deck.add_card(
    "First Aid!", 
    "Range self: Heal for 3 + 1d3 health."
)

ranger_deck.add_card(
    "Binding Shot", 
    "Range 4: Deal 2 damage, the target is [slowed] for their next turn."
)

misc_deck.add_card(
    "Status: Slowed",
    "This target has reduced movement speed, all movement is moved by half."
)

ranger_deck.add_card(
    "Place Bomb trap", 
    "Range 1: Place a 2 + d4 damage [Bomb Trap] into an empty square."
)

misc_deck.add_card(
    "Contraption: Bomb Trap",
    "Detonates when an enemy steps onto this square or an adjacent square."
    "\n\nDeals 2 + d4 damage to all characters in range."
)

speedy_deck.add_card(
    "Aimed Strike",
    "Melee: Deal 3 + 1d6 damage"
)

speedy_deck.add_card(
    "Parting Strike",
    "Melee: Deal 1 + 1d3 damage, move 2"
)

speedy_deck.add_card(
    "Blur",
    "Grant self 1 + 1d2 [Blur]"
)

misc_deck.add_card(
    "Blurry",
    "Blocks damage, blur stacks and is persistent."
)

speedy_deck.add_card(
    "Shuriken",
    "Range 2: Deal 3 + 1d3 damage"
)
