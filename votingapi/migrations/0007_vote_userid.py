# Generated by Django 4.0.2 on 2022-03-06 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votingapi', '0006_remove_menu_menuid_menu_restaurantid'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='userId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
