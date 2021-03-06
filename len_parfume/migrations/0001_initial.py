# Generated by Django 3.1.7 on 2021-02-22 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Общая сумма')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymoys_user', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('size', models.CharField(blank=True, max_length=150, null=True, verbose_name='Размер')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая сумма')),
            ],
            options={
                'verbose_name': 'Продукт для корзины',
                'verbose_name_plural': 'Продукты для корзины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Имя категории')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('phone', models.CharField(help_text='+38-050-111-11-11', max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=60, null=True, verbose_name='Емайл')),
                ('adress', models.CharField(blank=True, max_length=60, null=True, verbose_name='Город')),
                ('otdel', models.CharField(blank=True, max_length=20, null=True, verbose_name='Отделение')),
                ('status', models.CharField(choices=[('new', 'Новый заказ'), ('in_progress', 'Заказ в обработке'), ('is_ready', 'Заказ готов'), ('completed', 'Заказ выполнен'), ('deactive', 'Заказ Отменен')], default='new', max_length=100, verbose_name='Статус заказа')),
                ('buying_type', models.CharField(choices=[('self', 'Отделение'), ('delivery', 'Курьер')], default='self', max_length=100, verbose_name='Доставка')),
                ('status_pay', models.CharField(choices=[('pay', 'Оплачен'), ('not_pay', 'Отклонен'), ('miss', 'Ошибка при оплате'), ('nal', 'Наложенный платеж'), ('wait', 'Ожидание платежа'), ('reversed', 'Платеж возвращен')], default='nal', max_length=100, verbose_name='Оплата')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')),
                ('pay', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cпособ оплаты')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Наименоватние продукта')),
                ('image1', models.ImageField(upload_to='images/photos/%Y/%m/%d/', verbose_name='Главное изображение')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='images/products/%Y/%m/%d/', verbose_name='Изображение 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='images/products/%Y/%m/%d/', verbose_name='Изображение 3')),
                ('available', models.BooleanField(default=True, verbose_name='Наличие')),
                ('description', models.TextField(null=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Старая Цена')),
                ('views', models.IntegerField(default=0, verbose_name='Кол-во просмотров')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='len_parfume.category', verbose_name='Категория продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Обьем',
                'verbose_name_plural': 'Обьемы',
            },
        ),
        migrations.CreateModel(
            name='Whishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('products', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Продукты', to='len_parfume.product')),
            ],
            options={
                'verbose_name': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Rewiews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('text', models.TextField(max_length=500, verbose_name='Сообщение')),
                ('data', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Добавлено')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='len_parfume.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
