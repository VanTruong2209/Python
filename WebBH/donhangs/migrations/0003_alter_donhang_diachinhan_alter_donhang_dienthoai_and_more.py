# Generated by Django 4.0.4 on 2022-05-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donhangs', '0002_alter_chitietdonhang_id_alter_donhang_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donhang',
            name='diachinhan',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='donhang',
            name='dienthoai',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='donhang',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='donhang',
            name='ghichu',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='donhang',
            name='hoten',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
