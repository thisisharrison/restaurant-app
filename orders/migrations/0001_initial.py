# Generated by Django 2.0.3 on 2020-05-14 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subclass', models.CharField(choices=[('REG', 'regular'), ('SIL', 'sicilian')], default='REG', max_length=3)),
                ('flavour_option', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('SM', 'small'), ('LG', 'large')], default='SM', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topping', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='pizza',
            name='size_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_option', to='orders.Size'),
        ),
        migrations.AddField(
            model_name='pizza',
            name='toppings_option',
            field=models.ManyToManyField(blank=True, related_name='toppings_option', to='orders.Topping'),
        ),
    ]
