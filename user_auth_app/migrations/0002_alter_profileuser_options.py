# Generated by Django 5.1.7 on 2025-04-05 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profileuser',
            options={'ordering': ['user__username'], 'verbose_name': 'Profile User', 'verbose_name_plural': 'Profile Users'},
        ),
    ]
