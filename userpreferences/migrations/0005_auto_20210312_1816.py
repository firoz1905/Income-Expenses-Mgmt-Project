# Generated by Django 2.2 on 2021-03-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0004_userpreference_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
