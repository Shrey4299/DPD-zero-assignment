# Generated by Django 4.2.3 on 2023-09-09 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_registeruser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
