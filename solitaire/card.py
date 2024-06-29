
import flet as ft

# Constants
CARD_WIDTH = 70
CARD_HEIGTH = 100
DROP_PROXIMITY = 20
CARD_OFFSET = 20


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()
        #
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop

        self.left = None
        self.top = None
        self.solitaire = solitaire
        self.slot = None
        self.card_offset = CARD_OFFSET

        self.suite = suite
        self.rank = rank
        self.face_up = False
        self.content = ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGTH,
            border_radius = ft.border_radius.all(5),
            content = ft.Image(
                src = "card_back.png"
            )
        )
        self.draggable_pile = [self]

    def move_on_top(self):
        """Brings draggable card pile to the top of the stack while dragging."""
        for card in self.draggable_pile:
            self.solitaire.controls.remove(card)
            self.solitaire.controls.append(card)
        self.solitaire.update()

    def bounce_back(self):
        """Return a card to its original position."""
        for card in self.draggable_pile:
            card.top = card.slot.top + card.slot.pile.index(card) * CARD_OFFSET
            card.left = card.slot.left
        self.solitaire.update()

    def place(self, slot):
        """Snap a pile of cards into a slot."""
        for card in self.draggable_pile:
            card.top = slot.top + len(slot.pile) * CARD_OFFSET
            card.left = slot.left

            # Remove the card from the previous slot
            if card.slot:
                card.slot.pile.remove(card)

            # Change to new slot
            card.slot = slot

            # Add the card to the new slot's pile
            slot.pile.append(card)

        self.solitaire.update()

    def get_draggable_pile(self):
        """
        Returns list of cards that will be dragged together starting with
        the current card.
        """
        if self.slot is not None:
            self.draggable_pile = self.slot.pile[self.slot.pile.index(self) :]
        else:  # slot is None when the cards are dealt and need to be placed first time.
            self.draggable_pile = [self]

    def start_drag(self, e: ft.DragStartEvent):
        """Start dragging a card to keep track of prev. positions."""
        self.get_draggable_pile()
        self.move_on_top()
        self.solitaire.update()

    def drag(self, e: ft.DragUpdateEvent):
        """Allow the pile of cards to be dragged around the screen."""
        for card in self.draggable_pile:
            card.top = (
                max(0, self.top + e.delta_y)
                + self.draggable_pile.index(card) * CARD_OFFSET
            )
            card.left = max(0, self.left + e.delta_x)
            self.solitaire.update()

    def drop(self, e: ft.DragEndEvent):
        """If a card is close enough to a slot, snap it into place."""
        for slot in self.solitaire.slots:
            if (
                abs(self.top - (slot.top + len(slot.pile) * CARD_OFFSET))
                < DROP_PROXIMITY
                and abs(self.left - slot.left) < DROP_PROXIMITY
            ):
                self.place(slot)
                self.solitaire.update()
                return

        # or bounce back
        self.bounce_back()
