# Generated by Django 3.1.7 on 2021-02-23 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('len_parfume', '0003_auto_20210222_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ImageField(blank=True, null=True, upload_to='brands/photos/%Y/%m/%d/', verbose_name='Фото бренда если есть'),
        ),
    ]