import random
import flet as ft
from solitaire import KlondikeSolitaire, FreeCellSolitaire
from solitaire.menu import MyMenu


class Game(ft.Page):
    """
    A class to replace the page with a solitaire game.
    The game can be Klondike or FreeCell.
    The app also has a menu and some other screens for help, settings, etc.
    """

    def __init__(self, page):
        super().__init__
        self.solitaire = ft.Stack()  # Solitaire for now.
        self.page = page
        self._width = page.width
        self._height = page.height

    def did_mount(self):
        """
        Add the game to the page.
        """
        self.new_game("Klondike")
        self.page.add(self.solitaire)

    def new_game(self, kind: str = "Klondike", seed: int = None):
        """
        Create a new solitaire game.
        Can be Klondike or FreeCell.
        """
        available_games = {
            "Klondike": KlondikeSolitaire,
            "FreeCell": FreeCellSolitaire,
        }
        width = self._width
        height = self._height

        # the seed is up to 32k in memory of the old solitaire game from MS.
        seed = seed if seed is not None else random.randint(0, 32000)

        # check the children in the game and remove the old solitaire
        if self.solitaire is not None:
            print("Ending existing game.")
            if hasattr(self.solitaire,"seed"):
                print(" Seed: ", self.solitaire.seed)
            else:
                print("No seed.")

            self.page.remove(self.solitaire)

        # add the new solitaire to the page
        self.solitaire = available_games[kind](
            width=width,
            height=height,
            seed=seed,
        )
        print("New game started. Seed: ", self.solitaire.seed)
        # El juego no se agrega a la pagina, sino al game.??
        # TODO: fix this.
        self.page.add(self.solitaire)

    def resize(self, width, height):
        self._width = width
        self._height = height
        self.page.overlay.append(ft.SnackBar(
            ft.Text(f'New page size => width: {
                    self._width}, height: {self._height}')
        ))
        self.page.overlay[0].open = True  # show the snackbar
        if self.solitaire:
            self.solitaire.resize(width, height)


def main(page: ft.Page):
    """
    Free Cell Solitaire from the flet solitaire tutorial.
    """

    def page_resize(e):
        game.resize(page.width, page.height)
        page.update()

    print(f"Window size: {page.width} x {page.height}")
    game = Game(page)
    # game.new_game("Klondike", seed=123)
    menubar = MyMenu(controls=None, game=game)

    page.on_resized = page_resize

    # page.add(game.solitaire)
    # el juego esta agregado en el menubar, no directamente en la pagina.
    # pero no lo pinta... no deberia pintarlo, es solo una ref no un control.

    page.add(ft.Row([menubar]))
    # game.new_game("Klondike") # TODO: ideally ,we should offer an empty game.
    page.add(game.solitaire)


ft.app(target=main, assets_dir="assets")
