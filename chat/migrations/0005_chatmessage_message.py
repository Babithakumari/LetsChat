# Generated by Django 3.2.7 on 2021-09-17 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_rename_chatmessages_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='message',
            field=models.TextField(default=''),
        ),
    ]