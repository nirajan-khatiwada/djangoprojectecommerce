# Generated by Django 4.2.7 on 2023-11-29 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_cartitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='is_active',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]
