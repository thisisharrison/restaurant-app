# Generated by Django 2.0.3 on 2020-05-22 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_auto_20200521_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Size'),
        ),
    ]
