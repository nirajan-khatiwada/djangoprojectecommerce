# Generated by Django 4.2.7 on 2023-11-29 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_address_line_2_remove_order_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
    ]
