
import flet as ft

# Constants
SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(ft.Container):
    """
    A slot is a container that can hold cards.
    """

    def __init__(self, top, left, border=None):
        super().__init__()
        self.pile = []
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.left = left
        self.top = top
        self.border = border
        self.border_radius = ft.border_radius.all(5)

    def add_card(self, card):
        pass
