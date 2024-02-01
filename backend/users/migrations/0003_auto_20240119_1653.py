# Generated by Django 3.2.3 on 2024-01-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_foodgramuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodgramuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='Username'),
        ),
    ]
