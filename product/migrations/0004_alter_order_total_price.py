# Generated by Django 4.1.5 on 2023-02-05 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
