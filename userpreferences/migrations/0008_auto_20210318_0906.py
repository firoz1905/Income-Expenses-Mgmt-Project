# Generated by Django 2.2 on 2021-03-18 09:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0007_auto_20210318_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='dob',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]