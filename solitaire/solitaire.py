
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
        self.slots = []
        self.cards = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT
        print("yes")

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
        """
        Create a proper deck of cards.
        """
        suites = [
            Suite("hearts", "red"),
            Suite("diamonds", "red"),
            Suite("clubs", "black"),
            Suite("spades", "black")
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
            Rank("King", 13)
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
        self.stock = Slot(top=0, left=0, border=ft.border.all(color=ft.colors.BLACK, width=1))
        self.waste = Slot(top=0, left=100, border=None)

        self.foundations = []
        x = 300
        for i in range(4):
            self.foundations.append(Slot(top=0, left=x, border=ft.border.all(color=ft.colors.BLACK, width=1))
            )
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(Slot(top=200, left=x, border=ft.border.all(color=ft.colors.BLACK, width=1))
            )
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.update()

        


        ## old
        self.slots.append(Slot(top=0, left=0))
        self.slots.append(Slot(top=0, left=200))
        self.slots.append(Slot(top=0, left=300))
        self.controls.extend(self.slots)
        self.update()

    def deal_cards(self):
        self.controls.extend(self.cards)
        for card in self.cards:
            card.place(self.slots[0])
        self.update()

