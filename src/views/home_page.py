import flet as ft
from models.player import Player


def home_view(page: ft.Page, player: Player):
    def get_gradient_colors():
        if page.theme_mode == ft.ThemeMode.DARK:
            return ["#0f172a", "#1e1b4b"]
        else:
            return ["#e0f2fe", "#bae6fd"]

    async def go_to_game(e):
        page.session.store.set("game_log", player.history)
        await page.push_route("/game_page")

    async def go_to_history(e):
        await page.push_route("/history_page")

    async def toggle_theme(e):
        try:
            prefs = ft.SharedPreferences()
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                await prefs.set("theme", "dark")
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                await prefs.set("theme", "light")

            bg_container.gradient.colors = get_gradient_colors()
            page.update()
        except Exception as err:
            print(f"[Theme Toggle Error] {err}")

    difficulty_dropdown = ft.Dropdown(
        label="Складність симуляції",
        width=200,
        options=[
            ft.dropdown.Option("Легка"),
            ft.dropdown.Option("Нормальна"),
            ft.dropdown.Option("Хардкор"),
        ],
        value="Нормальна" if page.session.store.get("difficulty") is None else page.session.store.get("difficulty")
    )

    central_block = ft.Container(
        content=ft.Column([
            ft.Icon(
                ft.Icons.AUTO_STORIES_ROUNDED,
                size=36,
                color=ft.Colors.BLUE
            ),
            ft.Container(height=5),
            ft.Text(
                "Програма для моделювання випадкових подій",
                size=25,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.ON_SURFACE
            ),
            ft.Text(
                "Натисніть кнопку нижче, щоб розпочати процес керування об'єктом.",
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.ON_SURFACE_VARIANT
            ),
            ft.Container(height=10),
            difficulty_dropdown,
            ft.Container(height=10),
            ft.TextButton(
                content=ft.Text("Розпочати симуляцію", size=16, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD),
                on_click=go_to_game
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=40,
        border_radius=16,
        width=460,
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 8)
        )
    )

    bg_container = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=get_gradient_colors()
        ),
        expand=True,
    )

    full_screen_bg = ft.Stack(
        expand=True,
        controls=[
            bg_container,
            ft.Container(
                content=central_block,
                alignment=ft.Alignment.CENTER,
                expand=True,
                padding=ft.padding.symmetric(vertical=40, horizontal=20)
            )
        ]
    )

    return ft.View(
        route="/",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("Симуляція станом персонажа"),
                actions=[
                    ft.IconButton(icon=ft.Icons.HOME, tooltip="На головну"),
                    ft.IconButton(icon=ft.Icons.GAMEPAD, on_click=go_to_game, tooltip="Почати гру"),
                    ft.IconButton(icon=ft.Icons.TOGGLE_ON, on_click=toggle_theme, tooltip="Змінити тему"),
                    ft.IconButton(icon=ft.Icons.HISTORY, on_click=go_to_history, tooltip="Переглянути історію")
                ],
            ),
            full_screen_bg
        ],
        bottom_appbar=ft.BottomAppBar(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(ft.Icons.HOME,),
                    ft.IconButton(ft.Icons.GAMEPAD, on_click=go_to_game),
                    ft.IconButton(ft.Icons.HISTORY, on_click=go_to_history),
                ],
            ),
        ),
    )