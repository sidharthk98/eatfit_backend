# Generated by Django 5.0 on 2024-12-12 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0002_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
