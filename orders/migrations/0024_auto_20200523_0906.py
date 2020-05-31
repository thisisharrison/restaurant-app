# Generated by Django 2.0.3 on 2020-05-23 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_auto_20200523_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PEND', 'pending'), ('CONF', 'confirmed'), ('PREP', 'preparing'), ('READ', 'ready'), ('SHIP', 'shipped')], default='PEND', max_length=4),
        ),
    ]