
import flet as ft


class Menuder(ft.MenuBar):
    def __init__(self, controls=None):
        super().__init__(controls=controls)
        self.expand = True
        self.style = ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.RED_300,
            mouse_cursor={
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
            },
            padding=10,
        )
        self.controls = controls

    def _show(self, e):
        print(e.control.content.value)

    def a_submenu(self, text: str, icon: ft.Icon, controls=None):
        """
        Create submenus
        """
        return ft.SubmenuButton(
            content=ft.Text(text),
            on_open=self.handle_submenu_open,
            on_close=self.handle_submenu_close,
            on_hover=self.handle_submenu_hover,
            controls=controls,
        )

    def a_button(self, text: str, icon: ft.Icon, handle_on_click=lambda e: print("Button clicked")):
        """
        Create menu buttons
        """
        return ft.MenuItemButton(
            content=ft.Text(text),
            leading=ft.Icon(icon),
            close_on_click=False,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.colors.BLUE_300,
                    ft.ControlState.HOVERED: ft.colors.BLUE_400,
                },
                padding=10,
            ),
            on_click=handle_on_click,
        )

    def handle_submenu_open(self, e):
        pass

    def handle_submenu_close(self, e):
        pass

    def handle_submenu_hover(self, e):
        pass


class MyMenu(Menuder):
    def __init__(self, controls=None, game=None):
        super().__init__(controls=controls)
        self.game = game
        self.expand = True
        self.style = self.set_style()
        self.controls = [
            ft.Text("Solitaire", style=ft.TextStyle(color=ft.colors.WHITE)),
            self.a_submenu("New Game", ft.icons.GAMES, controls=[
                self.a_button("Klondike", ft.icons.STAR,
                              self.handle_new_klondike_game),
                self.a_button("Free Cell", ft.icons.BOOK_ONLINE,
                              self.handle_new_freecell_game),

            ]),
            self.a_button("Restart", ft.icons.REFRESH, self.handle_restart),
            self.a_button("Undo", ft.icons.UNDO, self._show),
            self.a_button("Pause", ft.icons.PAUSE, self._show),
            self.a_button("FastForward", ft.icons.FAST_FORWARD,
                          self.handle_ff),
            self.a_submenu("More", ft.icons.HELP, controls=[
                self.a_button("Help", ft.icons.HELP, self._show),
                self.a_button("About", ft.icons.INFO, self.handle_about),
                self.a_button("Settings", ft.icons.SETTINGS, self._show),
            ]),
        ]

    def set_style(self):
        return ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.RED_300,
            mouse_cursor={
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
            },
            padding=10,
        )

    def handle_new_klondike_game(self, e):
        self.handle_new_game(e, "Klondike")

    def handle_new_freecell_game(self, e):
        self.handle_new_game(e, "FreeCell")

    def handle_new_game(self, e, kind: str):
        """
        Use the solitaire object to start a new game.
        """
        print("New game to start")
        self.game.new_game(kind)

    def handle_restart(self, e):
        """
        Use the solitaire object to restart the game.
        """
        print("Game to restart")
        # TODO: implement restart solitaire
        print(self.game.solitaire.restart_solitaire())

    def handle_ff(self, e):
        """
        Use the solitaire object to fast forward the game.
        """
        print("Game to fast forward")
        print(self.game.solitaire.stock.pile)
        if len(self.game.solitaire.stock.pile) > 0:
            for card in self.game.solitaire.stock.pile:
                card.deal_to_waste()
        else:
            # re deal
            self.game.solitaire.restart_stock()

    def handle_about(self, e):
        """
        Use the solitaire object to show the about dialog.
        """
        print("Game to show about")
        print(self.game.solitaire.seed)
        print(self.game.solitaire)
