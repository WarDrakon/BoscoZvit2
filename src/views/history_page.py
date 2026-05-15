import flet as ft

def history_view(page):
    history_items = page.session.store.get("game_log")

    if not history_items:
        history_items = ["Ваша історія поки що порожня..."]

    async def go_to_home(e):
        await page.push_route("/")

    async def go_to_game(e):
        await page.push_route("/game_page")

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    return ft.View(
        route="/history_page",
        controls=[
            ft.AppBar(
                title=ft.Text("Історія подій"),
                actions=[
                    ft.IconButton(icon=ft.Icons.HOME, on_click=go_to_home, tooltip="На головну"),
                    ft.IconButton(icon=ft.Icons.GAMEPAD, on_click=go_to_game, tooltip="До гри"),
                    ft.IconButton(icon=ft.Icons.TOGGLE_ON, on_click=toggle_theme, tooltip="Змінити тему"),
                    ft.IconButton(icon=ft.Icons.HISTORY, tooltip="Історія")
                ],
            ),
            ft.Divider(),
            ft.ListView(
                expand=True,
                spacing=10,
                padding=20,
                controls=[
                    ft.Container(
                        content=ft.Text(item, size=16),
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_GREY),
                        border_radius=10
                    ) for item in history_items
                ]
            )
        ],
    )
