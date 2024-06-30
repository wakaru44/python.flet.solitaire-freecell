
import flet as ft

# Constants
# It sholud be 63.5 x 88.9 according to <https://en.wikipedia.org/w/index.php?title=Standard_52-card_deck&section=4>
SLOT_WIDTH = 63.5
SLOT_HEIGHT = 88.9
BORDER_RADIUS = 6


class Slot(ft.Container):
    """
    A slot is a container that can hold cards.
    """

    def __init__(
            self,
            solitaire: ft.Stack,
            top: int,
            left: int,
            border: int,
            column_number: int,
            row: int = 1
    ):
        super().__init__()
        # Sizing and Positioning
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        assert left is not None, "left must be defined and greater than 0"
        self.left = left
        assert top is not None, "top must be defined and greater than 0"
        self.top = top
        # Row is defined on creation of the slot. should start at 0 for 'top row'.
        self.row = row
        self.border = border
        self.border_radius = ft.border_radius.all(BORDER_RADIUS)
        assert column_number >= 0, "column_number must be greater than or equal to 0"
        self.column_number = column_number

        # Game properties
        self.pile = []
        self.bgcolor = "DARK_GREEN"
        self.solitaire = solitaire

        # Actions
        self.on_click = self.click  # FUCK ME. this is because is a container.
        self.on_double_tap = self.click

    def resize(self, width: int, height: int, separator: float) -> None:
        self.width = width
        self.height = height
        self.top = self.row * (height + separator)
        self.left = self.column_number * (width + separator)
        card_offset = separator  # we use it for both till needed otherwise.
        for idx, card in enumerate(self.pile):
            card.resize(width, height, self.top, card_offset)
            card.left = self.left

    def get_top_card(self):
        """
        Get the top card from the pile.
        """
        if len(self.pile) > 0:
            return self.pile[-1]

    def click(self, e) -> None:
        if self == self.solitaire.stock:
            self.solitaire.restart_stock()
