# Generated by Django 4.1.2 on 2023-03-01 10:14

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_licznik_receptur'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='receptura',
            managers=[
                ('receptury', django.db.models.manager.Manager()),
            ],
        ),
    ]
