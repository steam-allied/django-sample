# Generated by Django 4.0.2 on 2022-03-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votingapi', '0009_rename_menuid_menu_menutid'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='rate',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
