# Generated by Django 4.1.7 on 2023-03-24 08:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_remove_company_status_company_vip_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
