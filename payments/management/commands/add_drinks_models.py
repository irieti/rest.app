from django.core.management.base import BaseCommand
from payments.models import Category, Subcategory, MenuItem, Variant


class Command(BaseCommand):
    help = "Import menu items from dictionary"

    def handle(self, *args, **kwargs):
        self.add_menu_items()

    def add_menu_items(self):
        # Здесь добавьте ваш список данных
        self.menu_data = [
            {
                "category": "Cocktails",
                "items": [
                    {
                        "name": "Margarita",
                        "description": "tequila, agave, lime 150ml",
                        "variants": [
                            {"name": "Classic", "price": 9.0},
                            {"name": "Fruity - tangerine & banana", "price": 10.0},
                            {"name": "Mezcal - smoky", "price": 11.5},
                            {"name": "Spicy - chili & cucumber", "price": 9.5},
                            {
                                "name": "Spicy & Fruity - chili & passion fruit",
                                "price": 10.5,
                            },
                            {"name": "Spicy Mezcal - chili & smoky", "price": 12.0},
                        ],
                    },
                    {
                        "name": "Woland",
                        "description": "cranberry, gin, cointreau sweet & slightly bitter, 125ml",
                        "price": 8.5,
                    },
                    {
                        "name": "Azazello",
                        "description": "rhubarb, pisco, amaro montenegro, dry vermouth strong & herbal, 125ml",
                        "price": 10.0,
                    },
                    {
                        "name": "Behemoth",
                        "description": "lychee, vodka, pamplemousse tropical & velvety, 125ml",
                        "price": 9.5,
                    },
                    {
                        "name": "Natasha",
                        "description": "pear, rum, st germain fruity & creamy, 125ml",
                        "price": 9.0,
                    },
                    {
                        "name": "Hella",
                        "description": "ginger, turmeric, limoncello, sparkling light & spicy, 185ml",
                        "price": 9.0,
                    },
                    {
                        "name": "Frida",
                        "description": "lillet, white vermouth, suze dry & herbal, 125ml",
                        "price": 9.5,
                    },
                    {
                        "name": "Queen Margo at the Ball",
                        "description": "spicy tomato juice, vodka (with tequila +1.0 eur) bloody mary, 150ml",
                        "price": 9.5,
                    },
                ],
            },
            {
                "category": "Wine",
                "subcategories": [
                    {
                        "name": "Champagne",
                        "items": [
                            {
                                "name": "Champagne Henri Giraud, Espirit Nature, Brut, France",
                                "description": "pinot noir, chardonnay/ natural / mineral & slightly bitter/ 12.0%",
                                "price": 17.5,
                            },
                            {
                                "name": "Champagne Ullens Brut, France",
                                "description": "pinot noir, chardonnay/ natural / mineral & slightly bitter/ 12.0%",
                                "price": 18.5,
                            },
                            {
                                "name": "Champagne Ruinart, Brut, France",
                                "description": "pinot noir, meunier, chardonnay / fruity & nutty/ 12.5%",
                                "price": 20.0,
                            },
                        ],
                    },
                    {
                        "name": "Sparkling",
                        "items": [
                            {
                                "name": "Sparkling Rama e Selas, Brut, Portugal",
                                "description": "chardonnay, bical, arinto, baga / salty & slightly bitter/ 12.5%",
                                "price": 5.5,
                            },
                        ],
                    },
                    {
                        "name": "PetNat",
                        "items": [
                            {
                                "name": "PetNat Ghazii Rosato, Silvio Messana, Italy",
                                "description": "sangiovese / peach & lime/ 13.0%",
                                "price": 6.0,
                            },
                        ],
                    },
                    {
                        "name": "Orange",
                        "items": [
                            {
                                "name": "Orange Ciclo, Portugal",
                                "description": "moscatel galego/ citrus & flowers/ 13%",
                                "price": 6.0,
                            },
                            {
                                "name": "Orange Funky, Boutique Winery, Portugal",
                                "description": "rabigato, viosinho, síria/ mineral & peach/ 12%",
                                "price": 7.0,
                            },
                        ],
                    },
                    {
                        "name": "White",
                        "items": [
                            {
                                "name": "White Domaine de l'Écu Muscadet Classic, France",
                                "description": "muscadet 100%/ green apple & pear / 11%",
                                "price": 6.0,
                            },
                        ],
                    },
                    {
                        "name": "Verde",
                        "items": [
                            {
                                "name": "Verde Dona Paterna, Portugal",
                                "description": "alvarinho, trajadura/ elegant & mineral/ 13.0%",
                                "price": 5.5,
                            },
                        ],
                    },
                    {
                        "name": "Red",
                        "items": [
                            {
                                "name": "Red Ciclo, Portugal",
                                "description": "syrah/ tannins & red fruit/ 12,5%",
                                "price": 6.0,
                            },
                        ],
                    },
                ],
            },
            {
                "category": "Soft Drinks",
                "items": [
                    {
                        "name": "Lemonade, natural, sparkling, 330 ml",
                        "description": "Passion fruit, Lime",
                        "price": 4.5,
                    },
                    {
                        "name": "Cold tea ChariTea, natural, sparkling, 330 ml",
                        "description": "Mate, Rooibos",
                        "price": 4.5,
                    },
                    {
                        "name": "Selzer, natural, 330 ml",
                        "description": "Yuzu, Cucumber",
                        "price": 4.5,
                    },
                    {
                        "name": "Kombucha, natural, 330 ml",
                        "description": "Hibiscus, Lemondrop",
                        "price": 4.5,
                    },
                ],
            },
            {
                "category": "No Alcohol",
                "items": [
                    {
                        "name": "Sparkling Wine",
                        "description": "White, Rosé, 0,0%",
                        "price": 5.0,
                    },
                    {
                        "name": "Arensbak - Sparking White Wine Alternative",
                        "description": "Flavor profile: peach, gooseberry, lemongrass",
                        "price": 6.0,
                    },
                ],
            },
        ]

        for category_data in self.menu_data:
            # Получите или создайте категорию
            category, _ = Category.objects.get_or_create(name=category_data["category"])

            # Проверяем наличие подкатегорий
            if "subcategories" in category_data:
                for subcategory_data in category_data["subcategories"]:
                    subcategory, _ = Subcategory.objects.get_or_create(
                        name=subcategory_data["name"], category=category
                    )

                    # Добавляем элементы в подкатегорию
                    for item_data in subcategory_data["items"]:
                        menu_item = MenuItem.objects.create(
                            subcategory=subcategory,
                            name=item_data["name"],
                            description=item_data.get("description", ""),
                            price=item_data.get("price", 0.0),
                        )

                        # Добавляем варианты, если они доступны
                        if "variants" in item_data:
                            for variant_data in item_data["variants"]:
                                Variant.objects.create(
                                    menu_item=menu_item,
                                    name=variant_data["name"],
                                    price=variant_data["price"],
                                )

            # Добавляем элементы напрямую в категорию, если подкатегорий нет
            if "items" in category_data:
                for item_data in category_data["items"]:
                    menu_item = MenuItem.objects.create(
                        category=category,
                        name=item_data["name"],
                        description=item_data.get("description", ""),
                        price=item_data.get("price", 0.0),
                    )

                    # Добавляем варианты, если они доступны
                    if "variants" in item_data:
                        for variant_data in item_data["variants"]:
                            Variant.objects.create(
                                menu_item=menu_item,
                                name=variant_data["name"],
                                price=variant_data["price"],
                            )
