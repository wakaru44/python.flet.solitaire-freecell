
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

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

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
        """
        self.stock = Slot(top=0, left=0,
                          border=ft.border.all(1))

        self.waste = Slot(top=0, left=100, border=None)

        self.foundations = []
        x = 300
        for i in range(4):
            self.foundations.append(
                Slot(top=0, left=x, border=ft.border.all(1, "outline")))
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(Slot(top=150, left=x,
                                     border=ft.border.all(1, "outline")))
            x += 100

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
