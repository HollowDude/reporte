# Generated by Django 5.1.6 on 2025-04-03 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_alter_registro_receptor_alter_triciclo_autorizado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panels',
            name='aut',
            field=models.BooleanField(default=False, help_text='El kit se autorizara solo por el encargado de ello', verbose_name='Kit Autorizado'),
        ),
        migrations.AlterField(
            model_name='registro',
            name='cliente',
            field=models.ForeignKey(blank=True, help_text='Cliente a ser Reportado', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.cliente'),
        ),
        migrations.AlterField(
            model_name='registro',
            name='empresa',
            field=models.ForeignKey(blank=True, help_text='Empresa a ser Reportada', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.empresa'),
        ),
    ]
