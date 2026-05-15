import flet as ft
from models.player import Player


def home_view(page: ft.Page, player: Player):
    if page.theme_mode is None:
        page.theme_mode = ft.ThemeMode.LIGHT

    async def go_to_game(e):
        page.session.store.set("game_log", player.history)
        await page.push_route("/game_page")

    async def go_to_history(e):
        await page.push_route("/history_page")

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

    info = ft.Container(
        content=ft.Column([
            ft.Text(
                "Програма для моделювання випадкових подій",
                size=25,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Натисніть кнопку нижче, щоб розпочати процес керування об'єктом.",
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=10),
            ft.Button("Розпочати симуляцію",
                on_click=go_to_game
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=50,
        alignment=ft.Alignment.CENTER,
        expand=True
    )

    return ft.View(
        route="/",
        controls=[
            ft.AppBar(
                title=ft.Text("Симуляція станом персонажа"),
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        tooltip="На головну"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.GAMEPAD,
                        on_click=go_to_game,
                        tooltip="Почати гру"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.TOGGLE_ON,
                        on_click=toggle_theme,
                        tooltip="Змінити тему"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.HISTORY,
                        on_click=go_to_history,
                        tooltip="Переглянути історію подій"
                    )
                ],
            ),
            info
        ],
        bottom_appbar=ft.BottomAppBar(
            bgcolor=ft.Colors.GREY,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(ft.Icons.HOME, icon_color="white"),
                    ft.IconButton(ft.Icons.GAMEPAD, icon_color="white", on_click=go_to_game),
                    ft.IconButton(ft.Icons.HISTORY, icon_color="white", on_click=go_to_history),
                ],
            ),
        ),
    )