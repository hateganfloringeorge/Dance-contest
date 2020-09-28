# Generated by Django 2.2.7 on 2019-11-18 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contestapp', '0002_remove_contest_numberofseries'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveIntegerField(default=0)),
                ('roundNumber', models.PositiveIntegerField(default=1)),
                ('bonus', models.PositiveIntegerField(default=0)),
                ('comment', models.CharField(default='', max_length=80)),
                ('categoryName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='contestapp.Category')),
                ('postedBy', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('teamName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='contestapp.Team')),
            ],
        ),
    ]
