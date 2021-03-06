# Generated by Django 2.2.12 on 2022-05-14 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220506_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('role', models.CharField(choices=[('member', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Админ')], default='member', max_length=10)),
                ('age', models.IntegerField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Location')),
            ],
        ),
    ]
