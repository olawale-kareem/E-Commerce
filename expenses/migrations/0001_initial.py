# Generated by Django 3.2.7 on 2021-10-12 02:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('ONLINE_SERVICES', 'ONLINE_SERVICES'), ('TRAVEL', 'TRAVEL'), ('FOOD', 'FOOD'), ('RENT', 'RENT'), ('OTHERS', 'OTHERS')], max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, max_length=255)),
                ('descripton', models.TextField()),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
