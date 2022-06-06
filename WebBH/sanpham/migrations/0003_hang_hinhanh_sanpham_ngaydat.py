# Generated by Django 4.0.4 on 2022-05-26 15:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanpham', '0002_sanpham_tensanpham'),
    ]

    operations = [
        migrations.AddField(
            model_name='hang',
            name='hinhanh',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='sanpham',
            name='ngaydat',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
    ]