# Generated by Django 2.0.3 on 2020-05-18 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20200517_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topping',
            old_name='topping',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='order',
            name='item_order',
            field=models.ManyToManyField(related_name='ordereditems', to='orders.OrderItem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.MenuItem'),
        ),
    ]
