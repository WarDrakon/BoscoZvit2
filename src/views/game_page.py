import flet as ft
import random
import asyncio
import re
from models.player import Player
from models.event_list import events
from models.battle import Battle

LOCATIONS = [
    (0, "https://images.unsplash.com/photo-1441974231531-c6227db76b6e"),
    (15, "https://images.unsplash.com/photo-1448375240586-882707db888b"),
    (30, "https://images.unsplash.com/photo-1425913397330-cf8af2ff40a1"),
    (45, "https://images.unsplash.com/photo-1506744038136-46273834b3fb"),
    (60, "https://images.unsplash.com/photo-1454496522488-7a8e488e8606"),
    (75, "https://images.unsplash.com/photo-1509023464722-18d996393ca8"),
    (90, "https://images.unsplash.com/photo-1519681393784-d120267933ba"),
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

    async def go_to_shop(e):
        await page.push_route("/shop_page")

    async def toggle_theme(e):
        try:
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
        except Exception as err:
            print(f"[Theme Toggle Error] {err}")

    def edit_name(e):
        name_display.visible = False
        edit_button.visible = False
        edit_box.visible = True
        page.update()

    async def save_name(e):
        input_value = name_input.value.strip()

        if not re.match(r"^[a-zA-Zа-яА-ЯіІїЇєЄ0-9\s]{2,15}$", input_value):
            name_error_label.value = "Ім'я повинне бути від 2 до 15 літер! і без символів"
            name_error_label.visible = True
            page.update()
            return

        name_error_label.visible = False
        player.name = input_value
        name_display.value = player.name


        name_display.visible = True
        edit_button.visible = True
        edit_box.visible = False
        page.update()



    avatar_container = ft.Container(
        content=ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.WHITE70),
        margin=ft.margin.only(bottom=5, top=5)
    )

    name_display = ft.Text(player.name, size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    name_error_label = ft.Text("", size=12, color=ft.Colors.RED_ACCENT, weight=ft.FontWeight.BOLD, visible=False)

    edit_button = ft.IconButton(ft.Icons.EDIT, icon_size=16, icon_color=ft.Colors.WHITE70, on_click=edit_name)
    save_button = ft.IconButton(ft.Icons.CHECK_CIRCLE, icon_size=28, icon_color=ft.Colors.GREEN_ACCENT,
                                on_click=save_name)

    name_input = ft.TextField(
        value=player.name,
        height=45,
        width=180,
        hint_text="Ім'я героя",
        hint_style=ft.TextStyle(color=ft.Colors.WHITE38),
        bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE24,
        text_size=14,
        content_padding=10,
        text_align=ft.TextAlign.CENTER
    )




    edit_box = ft.Column([
        name_input,
        save_button
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5, visible=False)

    BAR_MAX_WIDTH = 180

    def calculate_hp_padding(current_hp, max_hp):
        percentage = max(0, min(1, current_hp / max_hp))
        return ft.padding.only(right=BAR_MAX_WIDTH * (1 - percentage))

    hp_bar_container = ft.Container(
        width=BAR_MAX_WIDTH, height=12,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.RED),
        border_radius=6,
        padding=calculate_hp_padding(player.hp, player.max_hp),
        content=ft.Container(bgcolor=ft.Colors.RED, border_radius=6)
    )

    hp_display = ft.Text(f"{player.hp}/{player.max_hp}", size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    atk_text = ft.Text(f"ATK: {player.attack}", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    def_text = ft.Text(f"DEF: {player.defense}", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    gold_text = ft.Text(f"Золото: {player.gold}", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)

    atk_row = ft.Row([ft.Icon(ft.Icons.BOLT, color=ft.Colors.ORANGE, size=20), atk_text],
                     alignment=ft.MainAxisAlignment.CENTER)
    def_row = ft.Row([ft.Icon(ft.Icons.SHIELD, color=ft.Colors.BLUE, size=20), def_text],
                     alignment=ft.MainAxisAlignment.CENTER)
    gold_row = ft.Row([ft.Icon(ft.Icons.PAID, color=ft.Colors.YELLOW, size=20), gold_text],
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

    btn_straight = ft.TextButton(content=ft.Text("Прямо", color=ft.Colors.WHITE), width=200)
    btn_left = ft.TextButton(content=ft.Text("Наліво", color=ft.Colors.WHITE), width=150)
    btn_right = ft.TextButton(content=ft.Text("Направо", color=ft.Colors.WHITE), width=150)

    state = {"last_event_title": None}

    async def handle_step(e):
        if not player.is_alive(): return

        btn_straight.disabled = btn_left.disabled = btn_right.disabled = True
        main_container_ref.opacity = 0.4
        event_card.opacity = 0
        buttons_container.opacity = 0
        page.update()

        await asyncio.sleep(0.4)

        event = random.choice(events)
        while event.get("title") == state["last_event_title"]:
            event = random.choice(events)
        state["last_event_title"] = event.get("title")

        gold_change = event.get("gold", 0)

        if event.get("type") == "ambush":
            difficulty = player.steps // 10
            e_hp = random.randint(20, 40) + (difficulty * 5)
            e_atk = random.randint(10, 15) + (difficulty * 2)
            e_def = random.randint(2, 5) + difficulty
            player.add_step()

            hp_lost, loot_gold = Battle.calculate_fight(player, e_hp, e_atk, e_def)
            hp_change, atk_change, def_change = -hp_lost, 0, 0
            gold_change = loot_gold

            loot_text = f" Отримано трофеї: +{loot_gold} 💰." if loot_gold > 0 else ""
            player.history.append(f"Крок {player.steps}: Бій з ворогом. Втрачено {hp_lost} HP.{loot_text}")

            event_description.value = f"{event.get('text')}\nВорог: HP:{e_hp}, ATK:{e_atk}, DEF:{e_def}"
        else:
            hp_change = event.get("hp", 0)
            atk_change = event.get("attack", 0)
            def_change = event.get("defense", 0)
            player.apply_event(event)
            res = []
            if hp_change != 0: res.append(f"{hp_change} HP")
            if atk_change != 0: res.append(f"{atk_change} ATK")
            if def_change != 0: res.append(f"{def_change} DEF")
            if gold_change != 0: res.append(f"{gold_change} Золота")
            res_text = ", ".join(res) if res else "Без втрат"
            player.history.append(f"Крок {player.steps}: {event.get('title')} ({res_text})")
            event_description.value = event.get("text", "...")

        impacts = []
        if hp_change != 0: impacts.append(f"{'+' if hp_change > 0 else ''}{hp_change} HP")
        if atk_change != 0: impacts.append(f"{'+' if atk_change > 0 else ''}{atk_change} ATK")
        if def_change != 0: impacts.append(f"{'+' if def_change > 0 else ''}{def_change} DEF")
        if gold_change != 0: impacts.append(f"{'+' if gold_change > 0 else ''}{gold_change} Золота")

        event_title.value = event.get("title", "Подія")
        event_impact.value = " | ".join(impacts) if impacts else ""
        event_impact.color = ft.Colors.RED_ACCENT if (
                hp_change < 0 or atk_change < 0 or def_change < 0 or gold_change < 0) else ft.Colors.GREEN_ACCENT

        hp_display.value = f"{player.hp}/{player.max_hp}"
        hp_bar_container.padding = calculate_hp_padding(player.hp, player.max_hp)
        steps_display.value = f"Кроків: {player.steps}"
        atk_text.value = f"ATK: {player.attack}"
        def_text.value = f"DEF: {player.defense}"
        gold_text.value = f"Золото: {player.gold}"
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
            btn_straight.disabled = btn_left.disabled = btn_right.disabled = False
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
            ft.TextButton(content=ft.Text("Повернутися в меню", color=ft.Colors.WHITE), on_click=go_to_home),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    return ft.View(
        padding=0, spacing=0, bgcolor=ft.Colors.BLACK, route="/game_page",
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    main_container_ref := ft.Container(
                        expand=True, image=current_bg_image,
                        content=ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Симуляція гри", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    ft.Row([
                                        ft.IconButton(ft.Icons.STORE, icon_color=ft.Colors.YELLOW, on_click=go_to_shop,
                                                      tooltip="Магазин"),
                                        ft.IconButton(ft.Icons.HOME, icon_color=ft.Colors.WHITE, on_click=go_to_home,
                                                      tooltip="Головна"),
                                        ft.IconButton(ft.Icons.TOGGLE_ON, icon_color=ft.Colors.WHITE,
                                                      on_click=toggle_theme, tooltip="Змінити тему"),
                                        ft.IconButton(ft.Icons.HISTORY, icon_color=ft.Colors.WHITE,
                                                      on_click=go_to_history, tooltip="Історія подій"),
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
                                            avatar_container,

                                            ft.Row([name_display, edit_button], alignment=ft.MainAxisAlignment.CENTER,
                                                   spacing=5),

                                            edit_box,

                                            name_error_label,
                                            ft.Divider(color=ft.Colors.WHITE24),
                                            ft.Text("ЗДОРОВ'Я", size=12, weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.RED),
                                            hp_bar_container,
                                            hp_display,
                                            ft.Container(height=5),
                                            atk_row, def_row, gold_row,
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
                                            border_radius=25, width=500, animate_opacity=300
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