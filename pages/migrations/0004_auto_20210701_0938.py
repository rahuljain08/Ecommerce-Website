# Generated by Django 3.1.4 on 2021-07-01 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20210701_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Processing', max_length=20),
        ),
    ]