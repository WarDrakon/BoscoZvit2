import flet as ft
from views.home_page import home_view
from views.game_page import game_view
from views.history_page import history_view
from models.player import Player

def main(page: ft.Page):
    if not page.session.store.get("player_obj"):
        page.session.store.set("player_obj", Player("Герой"))

    def route_change():
        page.views.clear()

        current_player = page.session.store.get("player_obj")

        if page.route == "/":
            page.views.append(home_view(page, current_player))

        elif page.route == "/game_page":
            page.views.append(game_view(page, current_player))

        elif page.route == "/history_page":
            page.views.append(history_view(page))

        page.update()

    page.on_route_change = route_change

    # page.on_view_pop = view_pop

    route_change()


if __name__ == '__main__':
    ft.run(main, view=ft.AppView.WEB_BROWSER)
