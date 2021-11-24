from PIL import Image, ImageFont, ImageDraw
import os
import cards
import decks

card_back = "cardback.png"

blanks = {
    "ranger": "ranger_blank.png",
    "speedy": "speedy_blank.png",
    "support": "support_blank.png",
    "tanky": "tanky_blank.png",
    "misc": "info_blank.png",
}

cardbase = "cardblanks/CardBlank.png"
cardbase_nocost = "cardblanks/CardBlank_nocost.png"

icons = {
    "ranger": "ranger_icon.png",
    "speedy": "rogue_icon.png",
    "support": "support_icon.png",
    "tanky": "tanky_icon.png",
    "magus": "magus_icon.png",
    "misc": "info_icon.png",
}


class CardMaker:
    def __init__(self):
        self.title_height = 48
        self.text_height = 36
        self.text_height_smaller = 32
        self.text_height_flavor = 20
        self.title_font = ImageFont.truetype('Charter Regular.ttf', size=self.title_height)
        self.text_font = ImageFont.truetype('Charter Regular.ttf', size=self.text_height)
        self.text_font_smaller = ImageFont.truetype('Charter Regular.ttf', size=self.text_height_smaller)
        
        self.text_fonts = {
            "normal": (36, ImageFont.truetype('Charter Regular.ttf', size=36)),
            "small": (30, ImageFont.truetype('Charter Regular.ttf', size=30)),
            "flavour": (self.text_height_flavor, ImageFont.truetype('Charter Italic.ttf', size=self.text_height_flavor)),
        }

    def get_text_dimensions(self, text_string, font):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)

    def make_card_texture(self, card_info):

        text_height, text_font = self.text_fonts['normal']

        if(card_info['line_count'] > 4):
            text_height, text_font = self.text_fonts['small']

        src_image = Image.open(cardbase) if 'costs' in card_info else Image.open(cardbase_nocost)
        width, height = src_image.size

        out_image = ImageDraw.Draw(src_image)

        # draw the name
        out_image.text((width/2, self.title_height*1.5), card_info["name"], font=self.title_font, anchor='ms')

        # draw the costs.
        if 'costs' in card_info:
            energy = card_info["costs"]["energy"]
            ap = card_info["costs"]["ap"]
            fill_energy = "#aaffff" if energy > 0 else "#fff"
            fill_ap = "#ffdd88" if ap > 0 else "#fff"

            fill_energy = "#fff"
            fill_ap = "#fff"

            if ap <= 0: ap = '-'
            if energy <= 0: energy = '-'
            out_image.text((64, self.title_height*1.7), str(energy), font=self.title_font, anchor='ms', fill=fill_energy)
            out_image.text((64, self.title_height*4.1), str(ap), font=self.title_font, anchor='ms', fill=fill_ap)

        # draw class icons
        icon_name = card_info['decks'][0]
        icon_image = Image.open("cardblanks/" + icons[icon_name])
        icon_image = icon_image.convert("RGBA")
        icon_image_data = icon_image.getdata()
        icon_image_new_data = []

        for pix in icon_image_data:
            icon_image_new_data.append((pix[0], pix[1], pix[2], int(pix[3] * 0.40)))

        icon_image.putdata(icon_image_new_data)
        icon_width, icon_height = icon_image.size

        # start drawing the text height
        desc_box_startx = 43
        desc_box_endx = 694
        desc_box_width = desc_box_endx - desc_box_startx

        desc_box_starty = 635
        desc_box_endy = 945
        desc_box_height = desc_box_endy - desc_box_starty

        desc_box_lmargin = 12
        card_text_height = card_info['line_count'] * (text_height + 16)
        assert card_text_height < desc_box_height, "Damn dude your description is really long"
            
        card_text_top_margin = (desc_box_height - card_text_height)/2

        # finish drawing the image
        icon_offset = (
            int((desc_box_width - icon_width)/2 + desc_box_startx), #x
            int((desc_box_height - icon_height)/2 + desc_box_starty), #y
        )
        src_image.paste(icon_image, icon_offset, icon_image)

        # draw the text
        out_image.multiline_text(
            (desc_box_lmargin + desc_box_startx, card_text_top_margin + desc_box_starty),
            card_info["text"], font=text_font, align='center', spacing=12
        )

        # draw the flavor text
        if "flavour" in card_info:
            flavour_font_height, flavour_font = self.text_fonts['flavour']
            flavour_width, flavour_height = self.get_text_dimensions(card_info['flavour'], flavour_font)
            flavour_offset = desc_box_endx - 12 - flavour_width, desc_box_endy - flavour_height * 2 - 12
            out_image.multiline_text(flavour_offset, card_info['flavour'], font=flavour_font)



        return src_image

    def make_and_save_card(self, card_info, out_dir=None):
        if not out_dir:
            out_dir = './'
        image = self.make_card_texture(card_info)

        # write out the card

        os.makedirs(out_dir, exist_ok=True)

        filename = card_info['name']
        filename = filename.replace(' ', '_')
        filename = filename.replace(':', '_')
        filename = filename.replace('!', '_')
        image.save(out_dir + f"{card_info['decks'][0]}_{filename}.png")

    def make_all_cards(self, cards, out_dir):
        """makes all cards for the list of cards it is assumed that all the cards have unique names

        """
        for card_info in cards:
            self.make_and_save_card(card_info, out_dir)

    def make_deck(self, deck_list, deck_name, out_dir='test/', dimensions=(10, 7)):
        # A decklist is a list of (card_info, count) tuples

        card_count = 0
        for card, count in deck_list:
            card_count += count

        if card_count > 69:
            print(f"There are too many cards in this deck {deck_list}")
            return

        out_file = os.path.join(out_dir, deck_name + ".png")
        os.makedirs(out_dir, exist_ok=True)
        out_image = self.make_deck_texture(deck_list, deck_name, dimensions)
        out_image.save(out_file)

    def make_deck_texture(self, deck_list, deck_name, dimensions):

        if (len(deck_list) > 69):
            print("!!! Uh oh this deck has too many cards")
            return 

        base_image = Image.open(cardbase)

        card_width, card_height = base_image.size
        root_width, root_height = (dimensions[0] * card_width, dimensions[1] * card_height)

        assert (7380, 6909) == (root_width, root_height), "what? did the card dimensions change?"

        root_image = Image.new('RGBA', (root_width, root_height), (0, 0, 0, 255))

        card_index = 0
        for card, count in deck_list:
            card_tex = self.make_card_texture(card)
            for i in range(count):
                offset = (int((card_index % 10)*card_width), int((card_index/10))*card_height)
                root_image.paste(card_tex, offset)
                card_index += 1

        card_index = 69
        offset = (int((card_index % 10)*card_width), int((card_index/10))*card_height)
        backimage = Image.open(card_back)
        root_image.paste(backimage, offset)
        return root_image

_aimed_shot_test_card = {
    "decks": ["ranger"],
    "name": "Arrow Shot",
    "text": "Ranged 4: deal 3 + 1d4 Damage\n",
    "line_count": 1,
    "costs":{
        "energy": 2,
        "ap": 2
    },
    "tags": ['ranged', 'attack']
}

def test_make_single_deck():
    decklist = [(_aimed_shot_test_card, 69)] 
    maker = CardMaker()
    maker.make_deck(decklist, 'test_decklist', 'tests/')

def test_make_aimed_shot():
    card_info = _aimed_shot_test_card
    maker = CardMaker()
    maker.make_card_texture(card_info);

def test_make_all_cards():
    maker = CardMaker()
    maker.make_all_cards(cards.card_infos, 'playtest_cards/')

def test_make_decks():
    maker = CardMaker()
    count = 0
    for deck_name, deck in decks.main_deckset.decks.items():
        count += 1
        print(f"Assembling deck.. [{count} of {len(decks.main_deckset.decks)}]\r", end='')
        maker.make_deck(deck, deck_name, 'playtest_decks')

def test_make_playtest_deck():
    maker = CardMaker()
    maker.make_deck(decks.main_deckset.decks['testing_deck'], 'testing_deck', 'playtest_decks')

if __name__ == "__main__":
    test_make_all_cards()
    test_make_decks()
