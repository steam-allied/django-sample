# Generated by Django 4.0.2 on 2022-03-06 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votingapi', '0007_vote_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='menutId',
            new_name='menuId',
        ),
    ]
