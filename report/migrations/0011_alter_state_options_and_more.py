# Generated by Django 4.0.6 on 2022-08-03 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0010_state_alter_situationreport_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='state',
            options={'ordering': ['created_on']},
        ),
        migrations.RenameField(
            model_name='situationreport',
            old_name='likes',
            new_name='dislike',
        ),
        migrations.AlterField(
            model_name='situationreport',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_state', to='report.state'),
        ),
        migrations.AlterField(
            model_name='situationreport',
            name='title',
            field=models.CharField(max_length=75),
        ),
    ]
