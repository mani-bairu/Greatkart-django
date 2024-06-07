# Generated by Django 3.1 on 2024-06-06 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0002_auto_20240603_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_items',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cart_items',
            name='variation',
            field=models.ManyToManyField(blank=True, null=True, to='store.variations'),
        ),
    ]
