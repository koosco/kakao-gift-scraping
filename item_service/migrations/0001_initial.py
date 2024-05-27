# Generated by Django 5.0.6 on 2024-05-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('item_price', models.IntegerField()),
                ('item_image_url', models.CharField(max_length=255)),
                ('brand_name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('option_name', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'item',
            },
        ),
    ]