# Generated by Django 4.2.3 on 2023-09-09 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_registeruser_premium_remove_registeruser_spam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeruser',
            name='phone_number',
        ),
    ]