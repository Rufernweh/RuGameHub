# Generated by Django 4.1.7 on 2023-04-02 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='code',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='slug',
        ),
    ]