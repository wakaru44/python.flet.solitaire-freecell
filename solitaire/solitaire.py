
import random

import flet as ft
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
    def __init__(self):
        super().__init__()
        self.controls = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT
        # self.seed = random.randint(1,32000) # win32 freecell seed range.
        # TODO: put the proper seed stuff here.
        self.seed = 11982  # famous seed imposible to win in freecell win32
        print("Seed:", self.seed)
        self.max_card_width = 75  # initially only
        self.max_card_height = 100  # initially only
        self.separator = 25  # initially only

        self.on_tap = lambda e: print("Solitaire tapped")

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def _max_square(self, width, height):
        """
        find the biggest rectangle of a given ratio that fits in the screen.
        @param width: ancho de la pantalla
        @param height: alto de la pantalla
        @return: tupla con el ancho y alto del cuadrado maximo.
        """
        ratio = "2:1"
        ratio_width, ratio_height = map(int, ratio.split(":"))
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

        print("Updating solt size")
        for slot in [self.stock, self.waste, *self.foundations, *self.tableau]:
            slot.resize(self.max_card_width, self.max_card_height)
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

    def create_slots(self):
        """
        Create a classick Klondike solitaire layout.
        <https://flet.dev/img/docs/solitaire-tutorial/solitaire-layout.svg>

        The positions of the slots are also numbered columns 0 to 6, 7 colunms.
        """

        self.stock = Slot(top=0, left=0,
                          border=ft.border.all(1), column_number=0)

        self.waste = Slot(top=0, left=100, border=None, column_number=1)

        self.foundations = []
        x = (self.max_card_width + self.separator) * \
            3  # foundations starts in the 4th column
        for i in range(4):
            self.foundations.append(
                Slot(top=0, left=x, border=ft.border.all(1, "outline"), column_number=i + 3))
            x += (self.max_card_width + self.separator)

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(Slot(top=150, left=x,
                                     border=ft.border.all(1, "outline"), column_number=i))
            x += (self.max_card_width + self.separator)

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.update()

    def deal_cards(self):
        """
        Get a french deck of cards and deal them to the slots.
        """
        random.shuffle(self.cards)
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
        print(self.tableau)

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
            print("And another round")

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
