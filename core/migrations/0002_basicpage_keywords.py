# Generated by Django 3.2.2 on 2021-10-02 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicpage',
            name='keywords',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='keywords'),
        ),
    ]