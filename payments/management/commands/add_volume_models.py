from django.core.management.base import BaseCommand
from payments.models import Category, Subcategory, MenuItem, Variant


class Command(BaseCommand):
    help = "Import menu items from dictionary"

    def handle(self, *args, **kwargs):
        self.add_menu_items()

    def add_menu_items(self):
        menu_data = [
            {
                "category": "Food",
                "subcategories": [
                    {
                        "name": "Appetizers",
                        "items": [
                            {
                                "name": "Bread & Butter",
                                "name_pt": "Pão com manteiga",
                                "price": 4.0,
                            },
                            {
                                "name": "Sicilian olives",
                                "name_pt": "Azeitonas de Sicilia",
                                "price": 4.0,
                            },
                            {
                                "name": "Roast potato with truffle mayo",
                                "name_pt": "Batata assada com mayo de trufa",
                                "price": 5.0,
                            },
                        ],
                    },
                    {
                        "name": "Main",
                        "items": [
                            {
                                "name": "Salmon tataki with grapes and sesamy sauce",
                                "name_pt": "Tataki de salmão com uvas e molho de sésamo",
                                "price": 10.5,
                            },
                            {
                                "name": "Dorado crudo with mango and raspberries",
                                "name_pt": "Dorado crudo com mango e framboesas",
                                "price": 11.0,
                            },
                        ],
                    },
                    {
                        "name": "Warm",
                        "items": [
                            {
                                "name": "Mussels Portuguese style",
                                "name_pt": "Mexilhões à Bulhão Pato",
                                "description": "(white wine, parsley, garlic)",
                                "description_pt": "(vinho branco, salsa, alho)",
                                "price": 10.5,
                            },
                            {
                                "name": "Octopus with spinach, basil and roast potato",
                                "name_pt": "Polvo com espinafres, manjericão e batata assada",
                                "price": 20.5,
                            },
                            {
                                "name": "Dorado filet with truffled potato and asparagus",
                                "name_pt": "Filete de dorado com batata trufada e espargos",
                                "price": 19.5,
                            },
                        ],
                    },
                    {
                        "name": "Desserts",
                        "items": [
                            {
                                "name": "Ice cream vanilla",
                                "name_pt": "Gelado de baunilha",
                                "price": 5.0,
                            },
                            {
                                "name": "Glossy Pear",
                                "name_pt": "Pêra brilhante",
                                "price": 6.5,
                            },
                        ],
                    },
                    {
                        "name": "Caviar",
                        "items": [
                            {
                                "name": "Caviar Service",
                                "name_pt": "Caviar Service",
                                "description": "50gr, bread, butter, sour cream, scallions served with Champagne Billecart-Salmon 37,5cl or Vodka Beluga Noble 20.0cl",
                                "description_pt": "50gr, pão, manteiga, creme azedo, cebolinha, servido com Champagne Billecart-Salmon 37,5cl ou Vodka Beluga Noble 20.0cl",
                                "price": 125.0,
                            },
                            {
                                "name": '"Black pearl" Oyster',
                                "name_pt": '"Black pearl" Oyster',
                                "price": 5.0,
                            },
                            {
                                "name": 'Caviar „bumps"',
                                "name_pt": 'Caviar „bumps"',
                                "price": 5.0,
                            },
                            {
                                "name": "Sexy buterbrod with caviar",
                                "name_pt": "Sexy buterbrod com caviar",
                                "price": 30.0,
                            },
                            {
                                "name": "Seabass crudo with caviar and oranges",
                                "name_pt": "Seabass crudo com caviar e laranjas",
                                "price": 25.0,
                            },
                            {
                                "name": "Scallops with caviar and parmigiano sauce",
                                "name_pt": "Vieiras com caviar e molho de parmigiano",
                                "price": 35.0,
                            },
                            {
                                "name": "Vanilla ice cream with a spoon of caviar",
                                "name_pt": "Gelado de baunilha com uma colher de caviar",
                                "price": 12.0,
                            },
                            {
                                "name": "Pancakes with caviar e salmão*",
                                "name_pt": "Panquecas com caviar e salmão*",
                                "price": 20.0,
                            },
                        ],
                    },
                ],
            },
            {
                "category": "Oysters",
                "items": [
                    {
                        "name": "Oysters Gigas Especial No. 3",
                        "name_pt": "Ostras Gigas Especial No3",
                        "description": "cruas",
                        "description_pt": "cruas",
                        "variants": [
                            {"name": "3un", "name_pt": "3un", "price": 9.5},
                            {"name": "6un", "name_pt": "6un", "price": 17.5},
                            {"name": "12un", "name_pt": "12un", "price": 28.5},
                        ],
                    },
                    {
                        "name": 'Oysters "Margo"',
                        "name_pt": 'Ostras "Margo"',
                        "description": "(grapefruit, pomegranate, wasabi, papaya, kumquat, spicy tomato)",
                        "description_pt": "(toranja, romã, wasabi, papaia, kumquat, tomate picante)",
                        "price": 24.5,
                    },
                    {
                        "name": "Big Seafood Plate to share",
                        "name_pt": "Prato de Marisco para partilhar",
                        "description": "(6 oysters, 2 scallops, mussels, salmon, red caviar)",
                        "description_pt": "(6 ostras, 2 vieiras, mexilhões, salmão, caviar vermelho)",
                        "price": 55.0,
                    },
                ],
            },
        ]

        for category_data in menu_data:
            category_name = category_data["category"]
            category, _ = Category.objects.get_or_create(name=category_name)

            # Check if category has subcategories
            if "subcategories" in category_data:
                for subcategory_data in category_data["subcategories"]:
                    subcategory, _ = Subcategory.objects.get_or_create(
                        name=subcategory_data["name"], category=category
                    )

                    # Add items to subcategory
                    for item_data in subcategory_data["items"]:
                        menu_item = MenuItem.objects.create(
                            subcategory=subcategory,
                            name=item_data["name"],
                            name_pt=item_data["name_pt"],
                            description=item_data.get("description", ""),
                            description_pt=item_data.get("description_pt", ""),
                            price=item_data.get("price", 0.0),
                        )

                        # Add variants if available
                        if "variants" in item_data:
                            for variant_data in item_data["variants"]:
                                Variant.objects.create(
                                    menu_item=menu_item,
                                    name=variant_data["name"],
                                    name_pt=variant_data["name_pt"],
                                    price=variant_data["price"],
                                )

            # Add items directly to category if no subcategory
            if "items" in category_data:
                for item_data in category_data["items"]:
                    menu_item = MenuItem.objects.create(
                        category=category,
                        name=item_data["name"],
                        name_pt=item_data["name_pt"],
                        description=item_data.get("description", ""),
                        description_pt=item_data.get("description_pt", ""),
                        price=item_data.get("price", 0.0),
                    )

                    # Add variants if available
                    if "variants" in item_data:
                        for variant_data in item_data["variants"]:
                            Variant.objects.create(
                                menu_item=menu_item,
                                name=variant_data["name"],
                                name_pt=variant_data["name_pt"],
                                price=variant_data["price"],
                            )
