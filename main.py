import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    # solitaire = Solitaire()
    # page.add(solitaire)
    """
    Free Cell Solitaire from the flet solitaire tutorial.
    """
    # Cosas de solitario
    def place(card: ft.GestureDetector, slot: ft.Container):
        """Place a card into a slot."""
        card.top = slot.top
        card.left = slot.left

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
        if (
            abs(e.control.top - slot.top) < snap_distance
            and abs(e.control.left - slot.left) < snap_distance
        ):
            place(e.control, slot)
        else:
            bounce_back(solitaire, e.control)
        e.control.update()

    # Games starts here
    slot = ft.Container(
        bgcolor=ft.colors.GREEN,
        width=70,
        height=100,
        left=200,
        top=0,
        border=ft.border.all(color=ft.colors.BLACK, width=1),
    )

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
        left=75,
        top=0,
        content=ft.Container(bgcolor=ft.colors.BLUE, width=70, height=100),
    )

    card3 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=75,
        top=0,
        content=ft.Container(bgcolor=ft.colors.RED, width=70, height=100),
    )

    solitaire = Solitaire()

    controls = [card3, card2, card1, slot]
    page.add(ft.Stack(controls=controls, width=1000, height=500))


ft.app(target=main)
