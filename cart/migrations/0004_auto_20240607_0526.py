# Generated by Django 3.1 on 2024-06-07 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20240606_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_items',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.cart'),
        ),
    ]
