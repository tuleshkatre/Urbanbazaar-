# Generated by Django 5.1.4 on 2025-01-16 07:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urbanbazaarapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_quantity', models.PositiveIntegerField()),
                ('category', models.CharField(choices=[('ELECTRONICS', 'Electronics'), ('CLOTHING', 'Clothing'), ('FURNITURE', 'Furniture'), ('ACCESSORIES', 'Accessories'), ('MOBILE', 'Mobile'), ('LAPTOP', 'Laptop')], default='ELECTRONICS', max_length=100)),
                ('image', models.ImageField(default='dd.png', upload_to='')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
