# Generated by Django 3.2.5 on 2022-03-06 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_imginput_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imginput',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
