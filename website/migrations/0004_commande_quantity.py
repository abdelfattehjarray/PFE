# Generated by Django 5.0.3 on 2024-04-27 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_remove_produit_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='quantity',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
