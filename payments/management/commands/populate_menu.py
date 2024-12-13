from django.core.management.base import BaseCommand
from payments.models import Category, Subcategory, MenuItem, Variant


class Command(BaseCommand):
    help = "Import menu items from dictionary"

    def handle(self, *args, **kwargs):
        self.populate_menu()

    def populate_menu(self):
        menu_data = {
            "Caviar": [
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
                    "name": "Pancakes with caviar with salmon",
                    "name_pt": "Panquecas com caviar e salmão*",
                    "price": 20.0,
                },
            ],
        }

        # Iterate through each category
        for category_name, subcategories in menu_data.items():
            # Create or get the category
            category, _ = Category.objects.get_or_create(name=category_name)

            # Check if category has subcategories or is flat
            if isinstance(subcategories, dict):
                # Iterate through subcategories
                for subcategory_name, items in subcategories.items():
                    # Create subcategory
                    subcategory, _ = Subcategory.objects.get_or_create(
                        name=subcategory_name, category=category
                    )

                    # Add items for each subcategory
                    for item_data in items:
                        self.create_menu_item(category, subcategory, item_data)
            else:
                # No subcategories, direct list of items
                for item_data in subcategories:
                    self.create_menu_item(category, None, item_data)

    def create_menu_item(self, category, subcategory, item_data):
        # Create menu item
        menu_item = MenuItem.objects.create(
            category=category,
            subcategory=subcategory,
            name=item_data["name"],
            description=item_data.get("description", ""),
            ingredients=item_data.get("ingredients", ""),
            volume=item_data.get("volume", ""),
            price=item_data.get(
                "price", item_data.get("variants", [{}])[0].get("price", 0)
            ),
        )

        # Create variants (if applicable)
        variants = item_data.get("variants", [])
        for variant_data in variants:
            Variant.objects.create(
                menu_item=menu_item,
                name=variant_data["name"],
                price=variant_data["price"],
            )
