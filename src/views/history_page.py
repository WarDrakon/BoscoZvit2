import flet as ft


def history_view(page: ft.Page, player):
    def get_gradient_colors():
        if page.theme_mode == ft.ThemeMode.DARK:
            return ["#0f172a", "#1e1b4b"]
        else:
            return ["#e0f2fe", "#bae6fd"]

    async def go_home(e):
        await page.push_route("/")

    async def go_to_game(e):
        await page.push_route("/game_page")

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

    history_logs = page.session.store.get("game_log") or []

    if not history_logs:
        card_content = ft.Column([
            ft.Icon(ft.Icons.HISTORY_TOGGLE_OFF_ROUNDED, size=48, color=ft.Colors.BLUE_GREY_400),
            ft.Container(height=10),
            ft.Text(
                "Ваша історія поки що порожня...",
                size=18,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.ON_SURFACE,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Запустіть симуляцію та пройдіть кілька кроків, щоб тут з'явилися записи подій.",
                color=ft.Colors.ON_SURFACE_VARIANT,
                text_align=ft.TextAlign.CENTER,
                size=14
            ),
            ft.Container(height=15),
            ft.TextButton(
                content=ft.Text("Зіграти першу гру", size=15, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD),
                on_click=go_to_game
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    else:
        log_controls = []
        for log in history_logs:
            log_controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LABEL_IMPORTANT_ROUNDED, color=ft.Colors.BLUE),
                    title=ft.Text(str(log), weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE),
                )
            )

        card_content = ft.Column([
            ft.Text(
                "Історія подій забігу",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_SURFACE
            ),
            ft.Divider(),
            ft.ListView(
                controls=log_controls,
                expand=True,
                spacing=10,
                height=350,
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    central_card = ft.Container(
        content=card_content,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        padding=30,
        border_radius=16,
        width=480,
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
                content=central_card,
                alignment=ft.Alignment.CENTER,
                expand=True,
                padding=ft.padding.symmetric(vertical=40, horizontal=20)
            )
        ]
    )

    return ft.View(
        route="/history_page",
        padding=0,
        spacing=0,
        controls=[
            ft.AppBar(
                title=ft.Text("Історія подій"),
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_home),
                actions=[
                    ft.IconButton(icon=ft.Icons.HOME, on_click=go_home, tooltip="На головну"),
                    ft.IconButton(icon=ft.Icons.GAMEPAD, on_click=go_to_game, tooltip="Почати гру"),
                    ft.IconButton(icon=ft.Icons.TOGGLE_ON, on_click=toggle_theme, tooltip="Змінити тему"),
                    ft.IconButton(icon=ft.Icons.HISTORY, tooltip="Переглянути історію")
                ],
            ),
            full_screen_bg
        ],
    )