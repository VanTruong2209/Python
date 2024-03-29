# Generated by Django 4.0.4 on 2022-06-08 16:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_image'),
        ('sanpham', '0006_remove_loaisanpham_hang_hang_loaisanpham'),
    ]

    operations = [
        migrations.CreateModel(
            name='DanhGia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noidung', models.CharField(max_length=2000, null=True)),
                ('ngaydat', models.DateField(default=datetime.datetime.now, null=True)),
                ('sanpham', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sanpham.sanpham')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
