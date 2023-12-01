# Generated by Django 4.2.7 on 2023-11-21 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='product/image')),
                ('stock', models.IntegerField()),
                ('is_available', models.BooleanField()),
                ('created_date', models.DateField(auto_now=True)),
                ('modefied_date', models.DateField(auto_now_add=True)),
                ('catogery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='category.category')),
            ],
        ),
    ]
