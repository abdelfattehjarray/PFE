# Generated by Django 5.0.3 on 2024-04-27 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_commande_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='price_indiv',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='commande',
            name='price_total',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='commande',
            name='sum',
            field=models.CharField(max_length=50),
        ),
    ]