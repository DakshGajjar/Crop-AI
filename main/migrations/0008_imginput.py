# Generated by Django 3.2.5 on 2022-03-06 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0007_delete_imginput'),
    ]

    operations = [
        migrations.CreateModel(
            name='imginput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
