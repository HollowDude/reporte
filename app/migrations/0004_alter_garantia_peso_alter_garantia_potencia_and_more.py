# Generated by Django 5.1.6 on 2025-03-07 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_reporte_email_garantia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garantia',
            name='peso',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='garantia',
            name='potencia',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='garantia',
            name='voltaje',
            field=models.IntegerField(),
        ),
    ]
