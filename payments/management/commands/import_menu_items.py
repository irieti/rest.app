from django.core.management.base import BaseCommand
from payments.models import Category, MenuItem, Variant
from decimal import Decimal


class Command(BaseCommand):
    help = "Import menu items from dictionary"

    def handle(self, *args, **options):
        menu_items = {
            "Oysters": [
                {
                    "name": "Oysters Gigas Especial No.3",
                    "price": {"3 un": 9.5, "6 un": 17.5, "12 un": 28.5},
                },
                {
                    "name": "Oysters 'Margo'",
                    "price": 24.5,
                    "description": "(grapefruit, pomegranate, wasabi, papaya, kumquat, spicy tomato)",
                },
                {
                    "name": "Big Seafood Plate to share",
                    "price": 55.0,
                    "description": "(6 oysters, 2 scallops, mussels, salmon, red caviar)",
                },
            ],
            "Bites": [
                {"name": "Bread & Butter", "price": 4.0},
                {"name": "Sicilian olives", "price": 4.0},
                {"name": "Roast potato with truffle mayo", "price": 5.0},
                {"name": "Salmon tataki with grapes and sesamy sauce", "price": 10.5},
                {"name": "Dorado crudo with mango and raspberries", "price": 11.0},
                {
                    "name": "Sashimi trio (tuna, seabass, salmon) with capers and olive oil",
                    "price": 13.0,
                },
                {
                    "name": "Bruschetta with anchovies, stracciatella and green oil",
                    "price": 8.0,
                },
                {
                    "name": "Scallops roasted with Comté cheese",
                    "price": 13.5,
                    "description": "(per 3 un.)",
                },
                {"name": "Burrata wtih figs and caramelised nuts", "price": 9.5},
                {
                    "name": "Tomato carpaccio with salmon, cottage goat cheese and capers",
                    "price": 9.5,
                },
                {
                    "name": "Tuna tataki a-la Niçoise",
                    "price": 13.5,
                    "description": "(asparagus, egg, dijon mustard, roast potato)",
                },
                {
                    "name": "Mussels Portuguese style",
                    "price": 10.5,
                    "description": "(white wine, parsley, garlic)",
                },
                {"name": "Octopus with spinach, basil and roast potato", "price": 20.5},
                {
                    "name": "Dorado filet with truffled potato and asparagus",
                    "price": 19.5,
                },
                {
                    "name": "Cheese board",
                    "price": 14.5,
                    "description": "(Comté, Gouda with truffle, Parmigiano, Wensleydale with cranberries)",
                },
                {"name": "Ice cream vanilla", "price": 5.0},
                {"name": "Glossy Pear", "price": 6.5},
            ],
            "Cocktails": [
                {
                    "name": "Margarita",
                    "base": "tequila, agave, lime",
                    "volume": "150ml",
                    "variants": [
                        {"name": "Classic", "price": 9.0, "description": "tommy's"},
                        {
                            "name": "Fruity",
                            "price": 10.0,
                            "description": "tangerine & banana",
                        },
                        {"name": "Mezcal", "price": 11.5, "description": "smoky"},
                        {
                            "name": "Spicy",
                            "price": 9.5,
                            "description": "chili & cucumber",
                        },
                        {
                            "name": "Spicy & Fruity",
                            "price": 10.5,
                            "description": "chili & passion fruit",
                        },
                        {
                            "name": "Spicy Mezcal",
                            "price": 12.0,
                            "description": "chili & smoky",
                        },
                    ],
                },
                {
                    "name": "Woland",
                    "price": 8.5,
                    "ingredients": "cranberry, gin, cointreau",
                    "description": "sweet & slightly bitter",
                    "volume": "125ml",
                },
                {
                    "name": "Azazello",
                    "price": 10.0,
                    "ingredients": "rhubarb, pisco, amaro montenegro, dry vermouth",
                    "description": "strong & herbal",
                    "volume": "125ml",
                },
                {
                    "name": "Behemoth",
                    "price": 9.5,
                    "ingredients": "lychee, vodka, pamplemousse",
                    "description": "tropical & velvety",
                    "volume": "125ml",
                },
                {
                    "name": "Natasha",
                    "price": 9.0,
                    "ingredients": "pear, rum, st germain",
                    "description": "fruity & creamy",
                    "volume": "125ml",
                },
                {
                    "name": "Hella",
                    "price": 9.0,
                    "ingredients": "ginger, turmeric, limoncello, sparkling",
                    "description": "light & spicy",
                    "volume": "185ml",
                },
                {
                    "name": "Frida",
                    "price": 9.5,
                    "ingredients": "lillet, white vermouth, suze",
                    "description": "dry & herbal",
                    "volume": "125ml",
                },
                {
                    "name": "Queen Margo at the Ball",
                    "price": 9.5,
                    "ingredients": "spicy tomato juice, vodka (with tequila +1.0 eur)",
                    "description": "bloody mary",
                    "volume": "150ml",
                },
            ],
            "Wine": [
                {
                    "name": "Champagne Henri Giraud, Espirit Nature, Brut, France",
                    "price": {"glass": 17.5, "bottle": 80.0},
                    "grapes": "pinot noir, chardonnay",
                    "description": "natural / mineral & slightly bitter",
                    "alcohol": "12.0%",
                },
                {
                    "name": "Champagne Ullens Brut, France",
                    "price": {"glass": 18.5, "bottle": 85.0},
                    "grapes": "pinot noir, chardonnay",
                    "description": "natural / mineral & slightly bitter",
                    "alcohol": "12.0%",
                },
                {
                    "name": "Champagne Ruinart, Brut, France",
                    "price": {"glass": 20.0, "bottle": 90.0},
                    "grapes": "pinot noir, meunier, chardonnay",
                    "description": "fruity & nutty",
                    "alcohol": "12.5%",
                },
                {
                    "name": "Sparkling Rama e Selas, Brut, Portugal",
                    "price": {"glass": 5.5, "bottle": 24.5},
                    "grapes": "chardonnay, bical, arinto, baga",
                    "description": "salty & slightly bitter",
                    "alcohol": "12.5%",
                },
                {
                    "name": "PetNat Ghazii Rosato, Silvio Messana, Italy",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "grapes": "sangiovese",
                    "description": "peach & lime",
                    "alcohol": "13.0%",
                },
                {
                    "name": "Orange Ciclo, Portugal",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "grapes": "moscatel galego",
                    "description": "citrus & flowers",
                    "alcohol": "13%",
                },
                {
                    "name": "Orange Funky, Portugal Boutique Winery, Portugal",
                    "price": {"glass": 7.0, "bottle": 29.5},
                    "grapes": "rabigato, viosinho, siria",
                    "description": "mineral & peach",
                    "alcohol": "12%",
                },
                {
                    "name": "White Domaine de l'Écu Muscadet Classic, France",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "grapes": "muscadet 100%",
                    "description": "green apple & pear",
                    "alcohol": "11%",
                },
                {
                    "name": "White Sauvignon Blanc, Vicentino, Portugal",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "grapes": "sauvignon blanc 100%",
                    "description": "flowers & pepper",
                    "alcohol": "12.5%",
                },
                {
                    "name": "White Oxalá, Portugal",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "grapes": "viognier 100%",
                    "description": "full bodied & buttery",
                    "alcohol": "13,0%",
                },
                {
                    "name": "Verde Dona Paterna, Portugal",
                    "price": {"glass": 5.5, "bottle": 24.5},
                    "grapes": "alvarinho, trajadura",
                    "description": "elegant & mineral",
                    "alcohol": "13,0%",
                },
                {
                    "name": "Red Ciclo, Portugal",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "grapes": "syrah",
                    "description": "tannins & red fruit",
                    "alcohol": "12,5%",
                },
                {
                    "name": "Red Natural Pacto Palhete, Carvalho Martins",
                    "price": {"glass": 5.5, "bottle": 24.5},
                    "grapes": "touriga franca, touriga nacional, tinta roriz",
                    "description": "crisp & fresh",
                    "alcohol": "12.5%",
                },
                {
                    "name": "Red Natural Primata, Niepoort, Portugal",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "grapes": "tinta qmarela, touriga franca, tinta roriz",
                    "description": "cherry & tanines",
                    "alcohol": "11.2%",
                },
            ],
            "Soft Drinks": [
                {
                    "name": "Lemonade, natural, sparkling",
                    "volume": "330 ml",
                    "brand": "ABC",
                    "price": 4.5,
                    "flavors": ["Passion fruit", "Lime"],
                },
                {
                    "name": "Cold tea ChariTea, natural, sparkling",
                    "volume": "330 ml",
                    "brand": "ABC",
                    "price": 4.5,
                    "flavors": ["Mate", "Rooibos"],
                },
                {
                    "name": "Selzer, natural",
                    "volume": "330 ml",
                    "brand": "Something & Nothing",
                    "price": 4.5,
                    "flavors": ["Yuzu", "Cucumber"],
                },
                {
                    "name": "Kombucha, natural",
                    "volume": "330 ml",
                    "brand": "Bouche",
                    "price": 4.5,
                    "flavors": ["Hibiscus", "Lemondrop"],
                },
            ],
            "No Alcohol": [
                {
                    "name": "Sparkling Wine",
                    "price": {"glass": 5.0, "bottle": 22.5},
                    "types": ["White", "Rosé"],
                    "alcohol": "0,0%",
                },
                {
                    "name": "Arensbak - Sparking White Wine Alternative",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "description": "Flavor profile: peach, gooseberry, lemongrass",
                    "pairing": "Ideal to pair with oysters",
                    "alcohol": "0,0%",
                },
                {
                    "name": "Cider Ambijus clearly confused Norway",
                    "price": {"glass": 6.0, "bottle": 26.5},
                    "description": "Flavor profile: apple cider, spruce needles, roasted oakwood, angelica root, elderflower and juniper",
                    "alcohol": "0,0%",
                },
                {
                    "name": "BRLO Beer, Naked",
                    "volume": "0,33ml",
                    "price": 5.0,
                    "alcohol": "0,0%",
                },
            ],
        }

        for category_name, items in menu_items.items():
            category, _ = Category.objects.get_or_create(name=category_name)

            for item in items:
                name = item["name"]
                description = item.get("description", "")

                if "price" in item:
                    if isinstance(item["price"], dict):
                        # Handle items with multiple price options
                        base_price = min(item["price"].values())
                        menu_item = MenuItem.objects.create(
                            category=category,
                            name=name,
                            description=description,
                            price=base_price,
                        )
                        for variant_name, variant_price in item["price"].items():
                            Variant.objects.create(
                                menu_item=menu_item,
                                name=variant_name,
                                price=variant_price,
                            )
                    elif isinstance(item["price"], (int, float, Decimal)):
                        # Handle items with a single price
                        MenuItem.objects.create(
                            category=category,
                            name=name,
                            description=description,
                            price=item["price"],
                        )
                elif "variants" in item:
                    # Handle items with variants (like cocktails)
                    base_price = min(variant["price"] for variant in item["variants"])
                    menu_item = MenuItem.objects.create(
                        category=category,
                        name=name,
                        description=description,
                        price=base_price,
                    )
                    for variant in item["variants"]:
                        Variant.objects.create(
                            menu_item=menu_item,
                            name=variant["name"],
                            price=variant["price"],
                            description=variant.get("description", ""),
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping item {name} due to missing price information"
                        )
                    )
                    continue

                # Handle additional information
                if "ingredients" in item:
                    menu_item = MenuItem.objects.get(name=name, category=category)
                    menu_item.description += f"\nIngredients: {item['ingredients']}"
                    menu_item.save()

                if "volume" in item:
                    menu_item = MenuItem.objects.get(name=name, category=category)
                    menu_item.description += f"\nVolume: {item['volume']}"
                    menu_item.save()

        self.stdout.write(self.style.SUCCESS("Successfully imported menu items"))
