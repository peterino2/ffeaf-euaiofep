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
        for card_name, card_count in tuplist:
            card_info = cards.find_card(card_name)
            assert card_info is not None, f"unknown card {card_name}"
            deck_list.append((card_info, card_count))
        
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
        ("Sharp Shot", 5),
        ("First Aid", 2),
        ("Binding Shot", 4),
        ("Place Bomb", 4),
        ("Contraption: Bomb Trap", 1),
        ("Status: Slowed", 1),
])

main_deckset.make_deck(
    "standard_speedy",[ 
        ("aimed strike", 5),
        ("parting strike", 3),
        ("blur", 3),
        ("shuriken", 4),
        ("blurry", 1),
])

main_deckset.make_deck(
    "standard_support",[ 
        ("energy bolt", 4),
        ("mending bolt", 3),
        ("motivate", 3),
        ("stamina surge", 4),
        ("hidden potential", 2),
])

main_deckset.make_deck(
    "standard_tanky",[ 
        ("Heavy Strike", 5),
        ("shields up", 3),
        ("get behind me", 3),
        ("sunder arms", 4),
        ("block", 1),
])

main_deckset.join_decks("testing_deck", [
    "standard_ranger",
    "standard_speedy",
    "standard_support",
    "standard_tanky"
])
