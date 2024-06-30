import flet as ft
from solitaire import KlondikeSolitaire
from solitaire.menu import MyMenu


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

    print(f"Window size: {page.width} x {page.height}")
    solitaire = KlondikeSolitaire()
    menubar = MyMenu(controls=None, solitaire=solitaire)

    page.on_resize = page_resize

    page.add(solitaire)
    page.add(ft.Row([menubar]))


ft.app(target=main, assets_dir="assets")
