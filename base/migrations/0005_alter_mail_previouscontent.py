# Generated by Django 5.0.4 on 2024-04-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_responsecontent_mail_previouscontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='previousContent',
            field=models.TextField(blank=True, null=True),
        ),
    ]
