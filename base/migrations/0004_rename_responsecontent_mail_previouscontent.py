# Generated by Django 5.0.4 on 2024-04-28 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_mail_options_mail_responsecontent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='responseContent',
            new_name='previousContent',
        ),
    ]