# Generated by Django 2.2.5 on 2019-09-24 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(blank=True, to='books.BookItem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(blank=True, to='books.OrderItem'),
        ),
    ]