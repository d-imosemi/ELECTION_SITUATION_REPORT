# Generated by Django 4.0.6 on 2022-07-31 01:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0005_alter_situationreport_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situationreport',
            name='dislikes',
        ),
        migrations.AlterField(
            model_name='situationreport',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='blog_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
