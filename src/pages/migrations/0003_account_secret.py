# Generated by Django 3.2.7 on 2021-11-21 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_account_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='secret',
            field=models.TextField(null=True),
        ),
    ]
