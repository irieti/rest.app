# Generated by Django 5.1.2 on 2024-10-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_subcategory_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="media/"),
        ),
    ]
