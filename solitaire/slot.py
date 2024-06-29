
import flet as ft

# Constants
SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(ft.Container):
    """
    A slot is a container that can hold cards.
    """

    def __init__(self, top, left):
        super().__init__()
        self.pile = []
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.left = left
        self.top = top
        self.border = ft.border.all(color=ft.colors.BLACK, width=1)

    def add_card(self, card):
        pass
