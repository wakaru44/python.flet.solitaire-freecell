
import flet as ft

# Constants
SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(ft.Container):
    """
    A slot is a container that can hold cards.
    """

    def __init__(self, top, left, border):
        super().__init__()
        self.pile = []
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.left = left
        self.top = top
        self.border = border
        self.border_radius = ft.border_radius.all(6)

    def get_top_card(self):
        """
        Get the top card from the pile.
        """
        if len(self.pile) > 0:
            return self.pile[-1]

    def click(self, e):
        if self == self.solitaire.stock:
            self.solitaire.restart_stock()
