# Generated by Django 4.2.3 on 2023-07-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_remove_order_tags_product_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
