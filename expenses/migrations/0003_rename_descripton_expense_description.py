# Generated by Django 3.2.7 on 2021-10-22 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_expense_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='descripton',
            new_name='description',
        ),
    ]
