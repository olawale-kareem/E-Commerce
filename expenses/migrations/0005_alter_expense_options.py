# Generated by Django 3.2.7 on 2021-10-22 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0004_alter_expense_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Income'},
        ),
    ]