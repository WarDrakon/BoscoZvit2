import flet as ft
from views.home_page import home_view
from views.game_page import game_view
from views.history_page import history_view
from views.shop_page import shop_view
from models.player import Player

async def main(page: ft.Page):
    try:
        prefs = ft.SharedPreferences()
        saved_theme = await prefs.get("theme")
        if saved_theme:
            page.theme_mode = ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
    except Exception as err:
        print(f"[Storage Error] {err}")
        page.theme_mode = ft.ThemeMode.DARK

    if not page.session.store.get("player_obj"):
        page.session.store.set("player_obj", Player("Герой"))

    async def route_change(e=None):
        page.views.clear()
        current_player = page.session.store.get("player_obj")

        if page.route == "/":
            page.views.append(home_view(page, current_player))
        elif page.route == "/game_page":
            page.views.append(game_view(page, current_player))
        elif page.route == "/history_page":
            page.views.append(history_view(page, current_player))
        elif page.route == "/shop_page":
            page.views.append(shop_view(page, current_player))

        page.update()

    page.on_route_change = route_change
    await route_change()

if __name__ == '__main__':
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)