
import flet as ft

# Constants
SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(ft.Container):
    """
    A slot is a container that can hold cards.
    """

    def __init__(self, top, left, border, column_number):
        super().__init__()
        self.pile = []
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        assert left is not None, "left must be defined and greater than 0"
        self.left = left
        assert top is not None, "top must be defined and greater than 0"
        self.top = top
        self.border = border
        self.border_radius = ft.border_radius.all(6)
        assert column_number >= 0, "column_number must be greater than or equal to 0"
        self.column_number = column_number

        # Actions
        self.on_tap = self.click
        self.on_tap = lambda e: print("Solitaire tapped")
        self.on_double_tap = self.click

    def resize(self, width : int, height :int ) -> None:
        self.width = width
        self.height = height
        separator = width / 3
        self.left = self.column_number * (width + separator)
        for card in self.pile:
            card.resize(width, height)
            card.left = self.left

    def get_top_card(self):
        """
        Get the top card from the pile.
        """
        if len(self.pile) > 0:
            return self.pile[-1]

    def click(self, e ) -> None:
        if self == self.solitaire.stock:
            self.solitaire.restart_stock()
        else:
            print("Slot clicked")