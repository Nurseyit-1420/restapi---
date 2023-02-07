# Generated by Django 4.1.5 on 2023-02-05 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=1, max_digits=10)),
                ('products', models.ManyToManyField(to='product.product')),
            ],
        ),
    ]
