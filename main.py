from PIL import Image, ImageFont, ImageDraw
import os
import cards

card_back = "cardback.png"

blanks = {
    "ranger": "ranger_blank.png",
    "speedy": "speedy_blank.png",
    "support": "support_blank.png",
    "tanky": "tanky_blank.png",
    "misc": "info_blank.png",
}

class CardMaker:
    def __init__(self):
        self.title_height = 48
        self.text_height = 36
        self.title_font = ImageFont.truetype('Charter Regular.ttf', size=self.title_height)
        self.text_font = ImageFont.truetype('Charter Regular.ttf', size=self.text_height)

    def make_card_texture(self, card_info, out_dir=None):
        if not out_dir:
            out_dir = './'

        src_image = Image.open(blanks[card_info['deck']])
        width, height = src_image.size

        out_image = ImageDraw.Draw(src_image)
        out_image.text((width/2, self.title_height*1.5), card_info["name"], font=self.title_font, anchor='ms')

        desc_box_startx = 43
        desc_box_endx = 694
        desc_box_width = desc_box_endx - desc_box_startx

        desc_box_starty = 635
        desc_box_endy = 945
        desc_box_height = desc_box_endy - desc_box_starty

        desc_box_lmargin = 12

        card_text_height = card_info['line_count'] * self.text_height
        assert card_text_height < desc_box_height, "Damn dude your description is really long"
            
        card_text_top_margin = (desc_box_height - card_text_height)/2

        out_image.multiline_text((desc_box_lmargin + desc_box_startx, card_text_top_margin+desc_box_starty), card_info["text"], font=self.text_font, align='center', spacing=12)

        os.makedirs(out_dir, exist_ok=True)

        filename = card_info['name']
        filename = filename.replace(' ', '_')
        filename = filename.replace(':', '_')
        filename = filename.replace('!', '_')

        src_image.save(out_dir + f"{filename}.png")

    def make_all_cards(self, cards, out_dir):
        """makes all cards for the list of cards it is assumed that all the cards have unique names

        """
        for card_info in cards:
            self.make_card_texture(card_info, out_dir)

def test_make_aimed_shot():
    card_info = {
        "deck": "ranger",
        "name": "Arrow Shot",
        "text": "Ranged 4: deal 3 + 1d4 Damage\n",
        "line_count": 1,
    };
    maker = CardMaker();
    maker.make_card_texture(card_info, 'tests/');

def test_make_all_cards():

    for card in cards.card_infos:
        print(card)
    
    maker = CardMaker();
    maker.make_all_cards(cards.card_infos, 'playtest_cards/')

if __name__ == "__main__":
    test_make_aimed_shot()
    test_make_all_cards()
