import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    # solitaire = Solitaire()
    # page.add(solitaire)
    """
    Free Cell Solitaire from the flet solitaire tutorial.
    """

    def place(card, slot):
        """Snap a card into a slot."""
        card.top = slot.top
        card.left = slot.left

    # Cosas de solitario
    def bounce_back(game, card):
        """Return a card to its original position."""
        card.top = game.start_top
        card.left = game.start_left

    def move_on_top(card, controls):
        """Push card to the top of the pile while dragging."""
        controls.remove(card)
        controls.append(card)
        page.update()

    def start_drag(e: ft.DragStartEvent):
        """Start dragging a card to keep track of prev. positions."""
        move_on_top(e.control, controls)
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left

    # Cosas de cartas
    def drag(e: ft.DragUpdateEvent):
        """Allow the card to be dragged around the screen."""
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(e: ft.DragEndEvent):
        """If a card is close enough to a slot, snap it into place."""
        snap_distance = 50  # pixels

        for slot in slots:
            if (
                abs(e.control.top - slot.top) < snap_distance
                and abs(e.control.left - slot.left) < snap_distance
            ):
                place(e.control, slot)
                e.control.update()
                return

        # or bounce back
        bounce_back(solitaire, e.control)
        e.control.update()

    # Games starts here
    slot1 = ft.Container(
        bgcolor=ft.colors.GREEN,
        width=70,
        height=100,
        left=0,
        top=0,
        border=ft.border.all(color=ft.colors.BLACK, width=1),
    )

    slot2 = ft.Container(
        bgcolor=ft.colors.GREEN,
        width=70,
        height=100,
        left=100,
        top=0,
        border=ft.border.all(color=ft.colors.BLACK, width=1),
    )

    slot3 = ft.Container(
        bgcolor=ft.colors.GREEN,
        width=70,
        height=100,
        left=200,
        top=0,
        border=ft.border.all(color=ft.colors.BLACK, width=1),
    )

    slots = [slot1, slot2, slot3]

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.colors.YELLOW, width=70, height=100),
    )

    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=100,
        top=0,
        content=ft.Container(bgcolor=ft.colors.BLUE, width=70, height=100),
    )

    solitaire = Solitaire()

    controls = slots + [card1, card2]

    # deal cards
    place(card1, slot1)
    place(card2, slot2)
    page.add(ft.Stack(controls=controls, width=1000, height=500))


ft.app(target=main)
