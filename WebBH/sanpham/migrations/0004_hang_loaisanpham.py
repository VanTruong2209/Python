# Generated by Django 4.0.4 on 2022-05-28 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanpham', '0003_hang_hinhanh_sanpham_ngaydat'),
    ]

    operations = [
        migrations.AddField(
            model_name='hang',
            name='loaisanpham',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sanpham.loaisanpham'),
        ),
    ]
