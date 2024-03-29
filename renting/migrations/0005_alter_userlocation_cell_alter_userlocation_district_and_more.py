# Generated by Django 4.2 on 2023-04-19 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0004_alter_userlocation_cell_alter_userlocation_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='cell',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='renting.cell', verbose_name='Cell'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='renting.district', verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='renting.province', verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='renting.sector', verbose_name='Sector'),
        ),
    ]
