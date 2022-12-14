# Generated by Django 4.1.1 on 2022-10-11 09:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('order_date', models.DateField(default=datetime.datetime.today)),
                ('customer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='craft.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('img1', models.ImageField(blank=True, null=True, upload_to='')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='')),
                ('desc', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('manufacturer', models.EmailField(blank=True, max_length=254)),
                ('instock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='craft.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('address', models.CharField(blank=True, default='', max_length=100)),
                ('phone', models.CharField(blank=True, default='', max_length=15)),
                ('paymentMethod', models.CharField(blank=True, default='', max_length=15)),
                ('manufacturer', models.EmailField(blank=True, max_length=254)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='craft.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='craft.product')),
            ],
        ),
    ]
