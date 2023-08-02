# Generated by Django 4.2.3 on 2023-08-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_product_date_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="note",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]