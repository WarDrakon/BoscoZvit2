import flet as ft
from models.player import Player


def shop_view(page: ft.Page, player: Player):
    SHOP_ITEMS = [
        {"id": "potion_hp", "name": "Мале зілля лікування", "desc": "Відновлює 25 HP. Корисно перед боєм.", "cost": 10,
         "hp": 25, "max_hp": 0, "atk": 0, "def": 0, "limit": 5},
        {"id": "elixir_max_hp", "name": "Еліксир довголіття", "desc": "Збільшує максимальне HP (+20).", "cost": 30,
         "hp": 20, "max_hp": 20, "atk": 0, "def": 0, "limit": 2},
        {"id": "sword", "name": "Сталевий меч", "desc": "Гострий клинок кузні. Збільшує атаку на 4.", "cost": 15,
         "hp": 0, "max_hp": 0, "atk": 4, "def": 0, "limit": 3},
        {"id": "armor", "name": "Важкі обладунки", "desc": "Чудовий захист від пасток та гоблінів. Захист +3.",
         "cost": 20, "hp": 0, "max_hp": 0, "atk": 0, "def": 3, "limit": 2},
        {"id": "amulet", "name": "Амулет Удачі", "desc": "Дарує комплексне посилення статів (+2 ATK, +2 DEF).",
         "cost": 40, "hp": 0, "max_hp": 0, "atk": 2, "def": 2, "limit": 1},
    ]

    CLASSES_FOR_SALE = [
        {"name": "Воїн", "cost": 100, "req_lvl": 2, "color": ft.Colors.AMBER_400, "icon": ft.Icons.SHIELD_MOON_ROUNDED},
        {"name": "Маг", "cost": 150, "req_lvl": 3, "color": ft.Colors.BLUE_400, "icon": ft.Icons.AUTO_AWESOME},
        {"name": "Злодій", "cost": 200, "req_lvl": 4, "color": ft.Colors.RED_400,
         "icon": ft.Icons.NO_ENCRYPTION_ROUNDED},
        {"name": "Ельф", "cost": 250, "req_lvl": 5, "color": ft.Colors.GREEN_400, "icon": ft.Icons.PARK},
    ]

    async def back_to_game(e):
        await page.push_route("/game_page")

    gold_balance = ft.Text(f"Твоє золото: {player.gold} 💰", size=22, weight=ft.FontWeight.BOLD,
                           color=ft.Colors.YELLOW_400)
    level_display = ft.Text(f"Ваш рівень: {player.level} 🎖", size=16, color=ft.Colors.CYAN_200,
                            weight=ft.FontWeight.BOLD)

    def update_shop_ui():
        gold_balance.value = f"Твоє золото: {player.gold} 💰"
        level_display.value = f"Ваш рівень: {player.level} 🎖"
        buy_lvl_btn.content.value = f"Купити рівень ({player.get_level_up_cost()} 💰)"
        update_classes_list()
        page.update()

    def try_buy_level(e):
        success, msg = player.buy_level()
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN if success else ft.Colors.RED)
        page.snack_bar.open = True
        update_shop_ui()

    def try_buy_class(c_item):
        success, msg = player.buy_class(c_item["name"], c_item["cost"], c_item["req_lvl"])
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN if success else ft.Colors.RED)
        page.snack_bar.open = True
        update_shop_ui()

    def try_buy(item, count_text, buy_btn):
        item_id = item["id"]
        current_bought = player.shop_limits.get(item_id, 0)
        max_limit = item["limit"]

        if current_bought >= max_limit:
            page.snack_bar = ft.SnackBar(ft.Text("Цей товар закінчився на складі!"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        if player.gold < item["cost"]:
            page.snack_bar = ft.SnackBar(ft.Text("Тобі не вистачає золота!"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        player.gold -= item["cost"]
        player.shop_limits[item_id] += 1

        player.max_hp += item["max_hp"]
        player.hp = min(player.max_hp, player.hp + item["hp"])
        player.attack += item["atk"]
        player.defense += item["def"]
        player.inventory.append(item["name"])
        player.history.append(f"Куплено в магазині: {item['name']}. Залишок золота: {player.gold}")

        gold_balance.value = f"Твоє золото: {player.gold} 💰"
        new_bought = player.shop_limits[item_id]
        count_text.value = f"Куплено: {new_bought}/{max_limit}"

        if new_bought >= max_limit:
            buy_btn.disabled = True
            buy_btn.content = ft.Text("Розпродано", color=ft.Colors.GREY)

        page.snack_bar = ft.SnackBar(ft.Text(f"Успішно куплено: {item['name']}!"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.update()

    buy_lvl_btn = ft.TextButton(
        content=ft.Text(f"Купити рівень ({player.get_level_up_cost()} 💰)", color=ft.Colors.CYAN_200,
                        weight=ft.FontWeight.BOLD),
        on_click=try_buy_level
    )

    items_list = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

    for item in SHOP_ITEMS:
        item_id = item["id"]
        bought = player.shop_limits.get(item_id, 0)
        max_lim = item["limit"]

        count_text = ft.Text(f"Куплено: {bought}/{max_lim}", size=14, color=ft.Colors.WHITE70)

        buy_btn = ft.TextButton(
            content=ft.Text(f"Купити за {item['cost']}💰", color=ft.Colors.GREEN_400)
        )
        buy_btn.on_click = lambda e, i=item, ct=count_text, btn=buy_btn: try_buy(i, ct, btn)

        if bought >= max_lim:
            buy_btn.disabled = True
            buy_btn.content = ft.Text("Розпродано", color=ft.Colors.GREY)

        card = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(item["name"], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
                    ft.Text(item["desc"], size=14, color=ft.Colors.WHITE60, max_lines=2, width=320),
                ], expand=True, alignment=ft.MainAxisAlignment.CENTER),
                ft.Column([
                    count_text,
                    buy_btn
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
            padding=15, border_radius=12, border=ft.border.all(1, ft.Colors.WHITE10)
        )
        items_list.controls.append(card)

    classes_container = ft.Column(spacing=10)

    def update_classes_list():
        classes_container.controls.clear()
        for c in CLASSES_FOR_SALE:
            is_unlocked = c["name"] in player.unlocked_classes
            is_level_ok = player.level >= c["req_lvl"]
            icon_color = c["color"] if is_unlocked else ft.Colors.GREY_600

            if is_unlocked:
                status_text = "Розблоковано"
                status_color = ft.Colors.GREEN_400
                btn_action = ft.TextButton(content=ft.Text("Куплено", color=ft.Colors.WHITE30), disabled=True)
            elif not is_level_ok:
                status_text = f"Потрібен рівень {c['req_lvl']}"
                status_color = ft.Colors.RED_300
                btn_action = ft.TextButton(content=ft.Text("Рівень занизький", color=ft.Colors.WHITE30), disabled=True)
            else:
                status_text = f"Ціна: {c['cost']} 💰"
                status_color = ft.Colors.WHITE70
                btn_action = ft.TextButton(
                    content=ft.Text("Купити клас", color=ft.Colors.GREEN_ACCENT, weight=ft.FontWeight.BOLD),
                    on_click=lambda e, item=c: try_buy_class(item)
                )

            classes_container.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Icon(c["icon"], color=icon_color, size=30),
                            ft.Column([
                                ft.Text(c["name"], size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                ft.Text(status_text, size=12, color=status_color),
                            ], spacing=2)
                        ]),
                        btn_action
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    padding=10, border_radius=8
                )
            )

    update_classes_list()

    return ft.View(
        route="/shop_page", padding=20, bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Row([
                ft.Text("Лавка Мандрівного Торговця", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                gold_balance
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=ft.Colors.WHITE24),

            ft.Container(
                content=ft.Row([
                    level_display,
                    ft.Container(content=buy_lvl_btn, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN),
                                 border_radius=8, padding=5)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE), padding=12, border_radius=10
            ),
            ft.Container(height=10),

            ft.Text("Гільдія Класів", size=20, color=ft.Colors.CYAN_300, weight=ft.FontWeight.BOLD),
            classes_container,
            ft.Divider(color=ft.Colors.WHITE24),

            ft.Text("Товари", size=20, color=ft.Colors.BLUE_200, weight=ft.FontWeight.BOLD),
            ft.Container(content=items_list, expand=True),
            ft.Divider(color=ft.Colors.WHITE24),
            ft.Row([
                ft.TextButton(content=ft.Text("Назад до пригод", color=ft.Colors.WHITE), on_click=back_to_game,
                              width=200)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]
    )