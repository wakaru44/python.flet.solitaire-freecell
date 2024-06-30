import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    # solitaire = Solitaire()
    # page.add(solitaire)
    """
    Free Cell Solitaire from the flet solitaire tutorial.
    """
    
    def page_resize(e):
        # solitaire.width = page.width
        # solitaire.height = page.height
        page.overlay.append( ft.SnackBar(
            ft.Text(f'New page size => width: {page.width}, height: {page.height}')
        ))
        page.overlay[0].open = True
        solitaire.resize(page.width, page.height)
        page.update()

    solitaire = Solitaire()

    page.on_resize = page_resize
    page.add(solitaire)


ft.app(target=main, assets_dir="assets")
