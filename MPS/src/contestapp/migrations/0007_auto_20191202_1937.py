# Generated by Django 2.2.7 on 2019-12-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contestapp', '0006_auto_20191201_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='currentRound',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contest',
            name='currentSeries',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
