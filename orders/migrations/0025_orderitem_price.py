# Generated by Django 2.0.3 on 2020-05-31 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_auto_20200523_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=0.5),
        ),
    ]
