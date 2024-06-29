import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    # solitaire = Solitaire()
    # page.add(solitaire)
    """
    Free Cell Solitaire from the flet solitaire tutorial.
    """

    solitaire = Solitaire()

    page.add(solitaire)


ft.app(target=main, assets_dir="assets")
