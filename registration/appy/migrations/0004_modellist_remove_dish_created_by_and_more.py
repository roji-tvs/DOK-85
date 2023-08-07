# Generated by Django 4.2.3 on 2023-08-04 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appy', '0003_bookshop_flowershop_electronicsshop_dish'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelList',
            fields=[
                ('model_id', models.PositiveIntegerField(choices=[(1, 'Bookshop'), (2, 'Flowershop'), (3, 'Dish'), (4, 'Electronics')], primary_key=True, serialize=False)),
                ('model_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'model_list',
            },
        ),
        migrations.RemoveField(
            model_name='dish',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='electronicsshop',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='flowershop',
            name='created_by',
        ),
        migrations.CreateModel(
            name='UserModelPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appy.modellist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_model_permission',
                'unique_together': {('user', 'model_id')},
            },
        ),
    ]