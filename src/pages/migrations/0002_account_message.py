# Generated by Django 3.2.7 on 2021-11-21 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
