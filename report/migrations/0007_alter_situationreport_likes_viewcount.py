# Generated by Django 4.0.6 on 2022-07-31 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0006_remove_situationreport_dislikes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situationreport',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='blog_post', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=50)),
                ('session', models.CharField(max_length=50)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='View_count', to='report.situationreport')),
            ],
        ),
    ]