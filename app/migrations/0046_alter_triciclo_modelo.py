# Generated by Django 5.1.6 on 2025-05-04 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_remove_triciclo_nume_remove_triciclo_vinch_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triciclo',
            name='modelo',
            field=models.CharField(choices=[('triciclo con extensor de rango', 'TRICICLO CON EXTENSOR DE RANGO'), ('triciclo eléctrico de carga', 'TRICICLO ELÉCTRICO DE CARGA'), ('triciclo eléctrico con panel solar', 'TRICICLO ELÉCTRICO CON PANEL SOLAR'), ('moto ry', 'MOTO RY'), ('cuatriciclo t90', 'CUATRICICLO T90')], help_text='Modelo del Triciclo', max_length=255, verbose_name='Modelo'),
        ),
    ]
