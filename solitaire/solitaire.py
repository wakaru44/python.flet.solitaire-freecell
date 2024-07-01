
import random
from copy import deepcopy

import flet as ft
# from card import Card
# from slot import Slot
from .card import Card
from .slot import Slot

# Constants
SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500


class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value


class Solitaire(ft.Stack):
    def __init__(self, width=None, height=None, seed: int = 11982):
        super().__init__()
        self.controls = []
        self.slots = []
        self.border_style = ft.border.all(1, "outline")
        # self.seed = random.randint(1,32000) # win32 freecell seed range.
        # self.seed = 11982  # famous seed imposible to win in freecell win32
        # TODO: seed control
        self.seed = seed

        # Dimensions and sizing
        self.width = SOLITAIRE_WIDTH if width is None else width
        self.height = SOLITAIRE_HEIGHT if height is None else height
        self.max_card_width = 75  # initially only
        self.max_card_height = 100  # initially only
        self.separator = 25  # initially only
        self.first_row = 0  # this one actually stays
        self.second_row = 150  # initially only
        self.ratio = "16:9"
        # self.ratio = "4:3" # kinda weird with the menu in the bottom.

        # Event Handling
        self.on_tap = lambda e: print("Solitaire tapped")

    def set_ratio(self, ratio):
        """ Ratio is a string like "16:9" or "4:3" """
        self.ratio = ratio

    def _max_square(self, width, height):
        """
        find the biggest rectangle of a given ratio that fits in the screen.
        @param width: ancho de la pantalla
        @param height: alto de la pantalla
        @return: tupla con el ancho y alto del cuadrado maximo.
        """
        ratio_width, ratio_height = map(int, self.ratio.split(":"))
        if width / height > ratio_width / ratio_height:
            max_width = height * ratio_width // ratio_height
            max_height = height
        else:
            max_width = width
            max_height = width * ratio_height // ratio_width
        return (max_width, max_height)

    def _card_size(self, table_width, table_height):
        """
        Calcula el tamano de la carta en base al cuadrado maximo.
        @param width: ancho de la pantalla
        @param height: alto de la pantalla
        @return: tupla con el ancho y alto de la carta.
        """
        ratio = "384:576"
        rows = 8
        cols = 7
        margin = 25

        min_width = 1000
        min_height = 500

        # defensive programming
        if table_width < min_width or table_height < min_height:
            table_width = min_width
            table_height = min_height

        card_width = (table_width / rows) - (margin * 2)
        card_height = card_width * \
            int(ratio.split(":")[1]) / int(ratio.split(":")[0])
        return (card_width, card_height)

    def get_card_size(self):
        return (self.max_card_width, self.max_card_height)

    def resize(self, width, height):
        """
        Calculate the new size of the solitaire game.
        Update the size of the cards and the slots.
        """
        # calculate new sizes
        new_width, new_height = self._max_square(width, height)
        self.width = new_width
        self.height = new_height
        self.max_card_width, self.max_card_height = self._card_size(
            new_width, new_height)
        self.separator = self.max_card_width / 3
        # Todo choose the separator.
        self.second_row = self.max_card_height + self.separator * 2

        print("Updating slot size")
        for slot in self.slots:
            slot.resize(self.max_card_width,
                        self.max_card_height, self.separator)
        self.update()

    def create_card_deck(self):
        """
        Create a proper deck of cards.
        """
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]

        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                self.cards.append(
                    Card(
                        solitaire=self,
                        suite=suite,
                        rank=rank
                    )
                )

    def ms_random_generator(self, seed=1):
        """
        taken from 
        https://rosettacode.org/wiki/Deal_cards_for_FreeCell#Python
        """
        max_int32 = (1 << 31) - 1
        seed = seed & max_int32

        while True:
            seed = (seed * 214013 + 2531011) & max_int32
            yield seed >> 16
        
    def ms_shuffle(self, seed):
        nc = len(self.cards)
        cards = list(range(nc - 1, -1, -1))
        rnd = self.ms_random_generator(seed)
        for i, r in zip(range(nc), rnd):
            j = (nc - 1) - r % (nc - i)
            cards[i], cards[j] = cards[j], cards[i]
        self.cards = cards
        return cards

class KlondikeSolitaire(Solitaire):
    def __init__(self, width=None, height=None, seed: int = 11982):
        super().__init__(width, height, seed)
        self.controls = []
        self.slots = []

        # Event Handling
        self.on_tap = lambda e: print("Solitaire tapped")

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_slots(self):
        """
        Create a classick Klondike solitaire layout.
        <https://flet.dev/img/docs/solitaire-tutorial/solitaire-layout.svg>

        The positions of the slots are also numbered columns 0 to 6, 7 colunms.
        """

        self.stock = Slot(self, top=self.first_row, left=0,
                          border=ft.border.all(1), column_number=0, row=0)

        self.waste = Slot(self, top=self.first_row, left=100,
                          border=None, column_number=1, row=0)

        self.foundations = []
        x = (self.max_card_width + self.separator) * \
            3  # foundations starts in the 4th column
        for i in range(4):
            self.foundations.append(
                Slot(
                    self,
                    top=self.first_row,
                    left=x,
                    border=self.border_style,
                    column_number=i + 3,
                    row=0
                )
            )
            x += (self.max_card_width + self.separator)

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(
                Slot(
                    self,
                    top=self.second_row,
                    left=x,
                    border=self.border_style,
                    column_number=i,
                    row=1
                )
            )
            x += (self.max_card_width + self.separator)

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.slots = [self.stock, self.waste, *self.foundations, *self.tableau]

    def deal_cards(self):
        """
        Get a french deck of cards and deal them to the slots.
        """
        # Cards sholud be shuffled before dealing.
        self.controls.extend(self.cards)

        # deal to tableau
        first_slot = 0
        remaining_cards = self.cards

        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                top_card = remaining_cards[0]
                top_card.place(slot)
                remaining_cards.remove(top_card)
            first_slot += 1

        # place remaining cards to stock pile
        for card in remaining_cards:
            card.place(self.stock)

        self.update()

        for slot in self.tableau:
            slot.get_top_card().turn_face_up()

        self.update()
        print("Cards have been dealed.")
        # print(self.tableau)
        # recursively print the tableau slots and number of cards in each slot, with list comprehension
        print([len(slot.pile) for slot in self.tableau])

    def check_foundations_rules(self, card, slot):
        """
        Validate that the card can be placed in the top foundations slots.
        """
        top_card = slot.get_top_card()
        if top_card is not None:
            return (
                card.suite.name == top_card.suite.name
                and card.rank.value - top_card.rank.value == 1
            )
        else:
            return card.rank.name == "Ace"

    def check_tableau_rules(self, card, slot):
        """
        Validate that the card can be placed in the tableau slots.
        A card has to be of alternating color,
        decrease in rank by 1
        and be face up.
        """
        top_card = slot.get_top_card()
        if top_card is not None:
            return (
                card.suite.color != top_card.suite.color
                and top_card.rank.value - card.rank.value == 1
                and top_card.face_up
            )
        else:
            return card.rank.name == "King"

    def restart_stock(self):
        """
        Restarts the stock pile by moving all cards from the waste pile.
        """
        while len(self.waste.pile) > 0:
            card = self.waste.get_top_card()
            card.turn_face_down()
            card.move_on_top()
            card.place(self.stock)

    def check_win(self):
        """
        Check if the player has won the game.
        """
        cards_num = 0
        for slot in self.foundations:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False

    def fly_card(self, card):
        card.animate_position = 1000
        card.move_on_top()
        card.top = random.randint(0, SOLITAIRE_HEIGHT)
        card.left = random.randint(0, SOLITAIRE_WIDTH)
        self.update()

    def winning_sequence(self):
        """
        Display a winning message.
        """
        print("You won!")
        for slot in self.foundations:
            for card in slot.pile:
                self.fly_card(card)
        self.controls.append(
            ft.AlertDialog(
                title=ft.Text("Congratulations!"),
                open=True,
            )
        )


class FreeCellSolitaire(Solitaire):
    def __init__(self, width=None, height=None, seed: int = 11982):
        super().__init__(width, height, seed)
        self.controls = []

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_slots(self):
        """
        Create a FreeCell layout
        Freecell has 8 columns, 4 foundations, and 4 'free' cell slots.
        In between the the foundations and the free cells there is a gap,
        totalling 9 columns wide.
        Under the free cells there is the 8 tableau slots.
        """

        border_style = ft.border.all(1, "outline")

        self.foundations = []
        x = (self.max_card_width + self.separator) \
            * 4  # foundations starts in the 6th column
        for i in range(4):
            self.foundations.append(
                Slot(
                    self,
                    top=self.first_row,
                    left=x,
                    border=border_style,
                    column_number=i + 5,
                    row=0
                )
            )
            x += (self.max_card_width + self.separator/2)

        self.free_cells = []
        x = 0
        for i in range(4):
            self.free_cells.append(
                Slot(
                    self,
                    top=self.first_row,
                    left=x,
                    border=border_style,
                    column_number=i,
                    row=0
                )
            )
            x += (self.max_card_width + self.separator/2)

        self.tableau = []
        x = 0 + (self.separator)  # Slightly offset to the right

        for i in range(8):
            self.tableau.append(
                Slot(
                    self,
                    top=self.second_row,
                    left=x,
                    border=border_style,
                    column_number=i,
                    row=1
                )
            )
            x += (self.max_card_width + self.separator/2)

        self.controls.extend(self.foundations)
        self.controls.extend(self.free_cells)
        self.controls.extend(self.tableau)
        self.slots = [*self.foundations, *self.free_cells, *self.tableau]

    def deal_cards(self):
        """
        Get a french deck of cards and deal them
        face up, to the tableau slots, 6-7 cards each.

        It goes card by card, dealing one to each tableau slot.
        untill the 4 on the left have 7 cards and the 4 on the right have 6.

        """
        print("Dealing FreeCell cards... Seed: ", self.seed)
        random.shuffle(self.cards)
        self.controls.extend(self.cards)

        # deal to tableau
        current_slot = 0
        remaining_cards = self.cards

        while len(remaining_cards) > 0:
            for idx, slot in enumerate(self.tableau):
                try:
                    top_card = remaining_cards[0]
                except IndexError:
                    break
                top_card.turn_face_up()
                top_card.place(slot)
                remaining_cards.remove(top_card)

        # copy the slots as they are for backup and restore of the game.
        self.backup_slots = deepcodpy(self.slots)

    def check_foundations_rules(self, card, slot):
        """
        Validate that the card can be placed in the top foundations slots.
        """
        top_card = slot.get_top_card()
        if top_card is not None:
            is_same_suite = card.suite.name == top_card.suite.name
            is_one_rank_higher = card.rank.value - top_card.rank.value == 1
            return is_same_suite and is_one_rank_higher
        else:
            return card.rank.name == "Ace"

    def check_tableau_rules(self, card, slot):
        """
        Validate that the card can be placed in the tableau slots.
        A card has to be of alternating color,
        decrease in rank by 1
        and be face up.
        """
        top_card = slot.get_top_card()
        if top_card is not None:
            is_different_color = card.suite.color != top_card.suite.color
            is_one_rank_lower = top_card.rank.value - card.rank.value == 1
            return is_different_color and is_one_rank_lower and top_card.face_up
        else:
            return card.rank.name == "King"

    def check_win(self):
        """
        Check if the player has won the game.
        """
        cards_num = 0
        for slot in self.foundations:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        # Or fail
        return False

    def fly_card(self, card):
        pass

    def winning_sequence(self):
        pass

    def restart_solitaire(self):
        pass
