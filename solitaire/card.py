
import flet as ft

# Constants
CARD_WIDTH = 70
CARD_HEIGTH = 100
DROP_PROXIMITY = 20


class Card(ft.GestureDetector):
    def __init__(self, solitaire, color_name):
        super().__init__()
        self.slot = None
        self.solitaire = solitaire
        #
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop

        self.left = None
        self.top = None
        self.color = color_name
        self.content = ft.Container(
            bgcolor=self.color,
            width=CARD_WIDTH,
            height=CARD_HEIGTH,
        )

    def move_on_top(self):
        """Push card to the top of the pile while dragging."""
        self.solitaire.controls.remove(self)
        self.solitaire.controls.append(self)
        self.solitaire.update()

    def bounce_back(self):
        """Return a card to its original position."""
        self.top = self.slot.top
        self.left = self.slot.left
        self.update()

    def place(self, slot):
        """Snap a card into a slot."""
        self.top = slot.top
        self.left = slot.left
        self.slot = slot

    def start_drag(self, e: ft.DragStartEvent):
        """Start dragging a card to keep track of prev. positions."""
        self.move_on_top()
        self.update()

    def drag(self, e: ft.DragUpdateEvent):
        """Allow the card to be dragged around the screen."""
        self.top = max(0, self.top + e.delta_y)
        self.left = max(0, self.left + e.delta_x)
        self.update()

    def drop(self, e: ft.DragEndEvent):
        """If a card is close enough to a slot, snap it into place."""
        for slot in self.solitaire.slots:
            if (
                abs(self.top - slot.top) < DROP_PROXIMITY
                and abs(self.left - slot.left) < DROP_PROXIMITY
            ):
                self.place(slot)
                self.update()
                return

        # or bounce back
        self.bounce_back()
        self.update()
