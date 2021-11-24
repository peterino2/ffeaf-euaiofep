import cards


class DeckSet:

    def __init__(self):
        self.decks = {}

        all_list = []

        for card_info in cards.card_infos:
            all_list.append((card_info, 1))

        self.decks['all'] = all_list

    def make_deck(self, deck_name, tuplist):
        deck_list = []
        non_misc_count = 0
        for card_name, card_count in tuplist:
            card_info = cards.find_card(card_name)
            print(card_info['decks'])
            if card_info['decks'][0] != 'misc':
                non_misc_count  += card_count
            assert card_info is not None, f"unknown card {card_name}"
            deck_list.append((card_info, card_count))

        if 'standard' in deck_name:
            assert non_misc_count == 16, f'standard deck {deck_name} does not have 16 cards (has {non_misc_count})'
        
        self.decks[deck_name] = deck_list

    def join_decks(self, new_name, deck_names):

        new_list = []
        assert new_name not in self.decks, f"Attempting to join to a deck with the same name {new_name}"
        for name in deck_names:
            assert name in self.decks, f"Joining failed, name not found {name}"
            for tup in self.decks[name]:
                new_list.append(tup)

        self.decks[new_name] = new_list

main_deckset = DeckSet()

main_deckset.make_deck(
    "standard_ranger",[ 
        ("Sharp Shot", 6),
        ("First Aid", 2),
        ("Binding Shot", 4),
        ("Place Bomb", 4),
        ("Contraption: Bomb Trap", 1),
])

main_deckset.make_deck(
    "standard_speedy", [ 
        ("aimed strike", 5),
        ("Flash of steel", 4),
        ("blur", 3),
        ("shuriken", 4),
])

main_deckset.make_deck(
    "standard_support",[ 
        ("energy bolt", 4),
        ("mending bolt", 5),
        ("motivate", 3),
        ("stamina surge", 2),
        ("hidden potential", 2),
])

main_deckset.make_deck(
    "standard_tanky",[ 
        ("Heavy Strike", 5),
        ("shields up", 5),
        ("get behind me", 3),
        ("sunder arms", 3),
])

main_deckset.make_deck(
"intrinsics", [
    ('invoke wisdom', 1),
    ('healing touch', 1),
    ('bowshot', 1),
    ('dash', 1),
    ('slash', 1),
])

main_deckset.make_deck(
    "biter_medium", [
        ('claw', 4),
        ('bite', 2),
        ('pounce',  2)
    ]
)

main_deckset.make_deck(
    "goblin_slinger", [
        ('slingshot', 6),
        ('dirty fighting',  2)
    ]
)

main_deckset.make_deck(
    "goblin", [
        ('goblin sword', 6),
        ('dirty fighting',  2)
    ]
)

main_deckset.make_deck(
    "biter_small", [
        ('small bite', 6),
        ('small leap',  2)
    ]
)

main_deckset.join_decks("testing_deck", [
    "standard_ranger",
    "standard_speedy",
    "standard_support",
    "standard_tanky"
])
