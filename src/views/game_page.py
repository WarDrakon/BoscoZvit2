import flet as ft
import random
import asyncio
from models.player import Player
from models.event_list import events
from models.battle import Battle

LOCATIONS = [
    (0, "https://images.unsplash.com/photo-1441974231531-c6227db76b6e"),
    (10, "https://images.unsplash.com/photo-1448375240586-882707db888b"),
    (20, "https://images.unsplash.com/photo-1425913397330-cf8af2ff40a1"),
    (30, "https://images.unsplash.com/photo-1506744038136-46273834b3fb"),
    (40, "https://images.unsplash.com/photo-1454496522488-7a8e488e8606"),
    (50, "https://images.unsplash.com/photo-1509023464722-18d996393ca8"),
    (60, "https://images.unsplash.com/photo-1519681393784-d120267933ba"),
]

def get_background_for_steps(steps):
    current_img = LOCATIONS[0][1]
    for step_threshold, img_url in LOCATIONS:
        if steps >= step_threshold:
            current_img = img_url
    return current_img

def game_view(page: ft.Page, player: Player):
    async def go_to_home(e):
        player.reset()
        await page.push_route("/")

    async def go_to_history(e):
        page.session.store.set("game_log", player.history)
        await page.push_route("/history_page")

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    def edit_name(e):
        name_display.visible = False
        edit_button.visible = False
        name_input.visible = True
        save_button.visible = True
        page.update()

    async def save_name(e):
        if name_input.value.strip():
            player.name = name_input.value
            name_display.value = player.name
        name_display.visible = True
        edit_button.visible = True
        name_input.visible = False
        save_button.visible = False
        page.update()

    name_display = ft.Text(player.name, size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    name_input = ft.TextField(
        value=player.name,
        height=40,
        width=100,
        visible=False,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        text_size=14,
        content_padding=5
    )
    edit_button = ft.IconButton(ft.Icons.EDIT, icon_size=16, icon_color=ft.Colors.WHITE70, on_click=edit_name)
    save_button = ft.IconButton(ft.Icons.CHECK, icon_size=16, icon_color=ft.Colors.GREEN, visible=False,
                                on_click=save_name)

    hp_display = ft.Text(f"{player.hp}/{player.max_hp}", size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    hp_bar = ft.ProgressBar(
        value=player.hp / player.max_hp,
        width=180,
        color=ft.Colors.RED,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.RED),
        height=10,
        border_radius=5,
    )

    atk_text = ft.Text(f"ATK: {player.attack}", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    def_text = ft.Text(f"DEF: {player.defense}", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)

    atk_row = ft.Row([ft.Icon(ft.Icons.BOLT, color=ft.Colors.ORANGE, size=20), atk_text],
                     alignment=ft.MainAxisAlignment.CENTER)
    def_row = ft.Row([ft.Icon(ft.Icons.SHIELD, color=ft.Colors.BLUE, size=20), def_text],
                     alignment=ft.MainAxisAlignment.CENTER)

    steps_display = ft.Text(f"Кроків: {player.steps}", size=16, color=ft.Colors.WHITE70)

    event_title = ft.Text("Оберіть шлях", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400,
                          text_align=ft.TextAlign.CENTER)
    event_description = ft.Text("Ви стоїте на роздоріжжі посеред лісу...", size=16, color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.CENTER)
    event_impact = ft.Text("", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    death_message = ft.Text(size=20, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
    death_reason = ft.Text(size=16, color=ft.Colors.WHITE70, italic=True, text_align=ft.TextAlign.CENTER)

    current_bg_image = ft.DecorationImage(src=get_background_for_steps(player.steps), fit=ft.BoxFit.COVER)
    main_container_ref = ft.Container(expand=True, animate_opacity=400)

    btn_straight = ft.TextButton("Прямо", width=200)
    btn_left = ft.TextButton("Наліво", width=150)
    btn_right = ft.TextButton("Направо", width=150)

    state = {"last_event_title": None}

    async def handle_step(e):
        if not player.is_alive(): return

        btn_straight.disabled = True
        btn_left.disabled = True
        btn_right.disabled = True
        main_container_ref.opacity = 0.4
        event_card.opacity = 0
        buttons_container.opacity = 0
        page.update()

        await asyncio.sleep(0.4)

        available_events = events
        event = random.choice(available_events)
        while event.get("title") == state["last_event_title"]:
            event = random.choice(available_events)
        state["last_event_title"] = event.get("title")

        if event.get("type") == "ambush":
            difficulty = player.steps // 10
            e_hp = random.randint(20, 40) + (difficulty * 5)
            e_atk = random.randint(10, 15) + (difficulty * 2)
            e_def = random.randint(2, 5) + difficulty
            player.add_step()
            hp_lost = Battle.calculate_fight(player, e_hp, e_atk, e_def)
            hp_change, atk_change, def_change = -hp_lost, 0, 0
            player.history.append(f"Крок {player.steps}: Бій з ворогом. Втрачено {hp_lost} HP.")
            event_description.value = f"{event.get('text')}\nВорог: HP:{e_hp}, ATK:{e_atk}, DEF:{e_def}"
        else:
            hp_change = event.get("hp", 0)
            atk_change = event.get("attack", 0)
            def_change = event.get("defense", 0)
            player.apply_event(event)
            res = []
            if hp_change != 0: res.append(f"{hp_change} HP")
            if atk_change != 0: res.append(f"{atk_change} ATK")
            res_text = ", ".join(res) if res else "Без втрат"
            player.history.append(f"Крок {player.steps}: {event.get('title')} ({res_text})")
            event_description.value = event.get("text", "...")

        impacts = []
        if hp_change != 0: impacts.append(f"{'+' if hp_change > 0 else ''}{hp_change} HP")
        if atk_change != 0: impacts.append(f"{'+' if atk_change > 0 else ''}{atk_change} ATK")
        if def_change != 0: impacts.append(f"{'+' if def_change > 0 else ''}{def_change} DEF")

        event_title.value = event.get("title", "Подія")
        event_impact.value = " | ".join(impacts)
        event_impact.color = ft.Colors.RED_ACCENT if (
                hp_change < 0 or atk_change < 0 or def_change < 0) else ft.Colors.GREEN_ACCENT

        hp_display.value = f"{player.hp}/{player.max_hp}"
        hp_bar.value = player.hp / player.max_hp
        steps_display.value = f"Кроків: {player.steps}"
        atk_text.value = f"ATK: {player.attack}"
        def_text.value = f"DEF: {player.defense}"
        current_bg_image.src = get_background_for_steps(player.steps)

        if not player.is_alive():
            player.history.append(f"--- ГЕРОЙ ЗАГИНУВ НА КРОЦІ {player.steps} ---")
            death_message.value = f"Герой загинув після {player.steps} кроків"
            death_reason.value = f"Остання подія: {event.get('title')}\n({event_impact.value})"
            event_card.opacity = 1
            page.update()
            await asyncio.sleep(1.2)
            death_overlay.visible = True
            main_container_ref.opacity = 1
        else:
            main_container_ref.opacity = 1
            event_card.opacity = 1
            buttons_container.opacity = 1
            btn_straight.disabled = False
            btn_left.disabled = False
            btn_right.disabled = False
        page.update()

    btn_straight.on_click = btn_left.on_click = btn_right.on_click = handle_step

    buttons_container = ft.Column([
        ft.Container(content=btn_straight, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK), border_radius=12),
        ft.Row([
            ft.Container(content=btn_left, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK), border_radius=12),
            ft.Container(content=btn_right, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK), border_radius=12),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, animate_opacity=300)

    death_overlay = ft.Container(
        expand=True, visible=False, bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.BLACK),
        content=ft.Column([
            ft.Icon(ft.Icons.DANGEROUS, color=ft.Colors.RED, size=100),
            ft.Text("ГРА ЗАКІНЧЕНА", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
            death_message,
            death_reason,
            ft.Container(height=20),
            ft.TextButton("Повернутися в меню", on_click=go_to_home, style=ft.ButtonStyle(color=ft.Colors.WHITE)),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    return ft.View(
        padding=0, spacing=0, bgcolor=ft.Colors.BLACK, route="/game_page",
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    main_container_ref := ft.Container(
                        expand=True,
                        image=current_bg_image,
                        content=ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Симуляція гри", size=20, weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE),
                                    ft.Row([
                                        ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.WHITE,
                                                      on_click=go_to_home),
                                        ft.IconButton(ft.Icons.GAMEPAD, icon_color=ft.Colors.WHITE),
                                        ft.IconButton(ft.Icons.TOGGLE_ON, icon_color=ft.Colors.WHITE,
                                                      on_click=toggle_theme),
                                        ft.IconButton(ft.Icons.HISTORY, icon_color=ft.Colors.WHITE,
                                                      on_click=go_to_history),
                                    ])
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                padding=ft.padding.only(20, 10, 20, 10),
                                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                            ),
                            ft.Container(
                                expand=True, padding=30,
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=50),
                                            ft.Row([name_display, name_input, edit_button, save_button],
                                                   alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                                            ft.Divider(color=ft.Colors.WHITE24),
                                            ft.Text("ЗДОРОВ'Я", size=12, weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.RED),
                                            hp_bar,
                                            hp_display,
                                            ft.Container(height=5),
                                            atk_row,
                                            def_row,
                                            ft.Divider(color=ft.Colors.WHITE24),
                                            steps_display,
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                                        bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK), padding=15,
                                        border_radius=20, width=220,
                                    ),
                                    ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                                    ft.Column([
                                        event_card := ft.Container(
                                            content=ft.Column([
                                                event_title, ft.Divider(height=1, color=ft.Colors.WHITE24),
                                                event_description, event_impact
                                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                                            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK), padding=30,
                                            border_radius=25, width=500,
                                            animate_opacity=300, scale=ft.Scale(1)
                                        ),
                                        buttons_container
                                    ], alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            ),
                        ], spacing=0),
                    ),
                    death_overlay
                ]
            )
        ]
    )