# Generated by Django 2.2 on 2021-03-12 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0002_auto_20210312_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='profile_pic',
            field=models.ImageField(blank=True, default='Profile_pic.png', null=True, upload_to=''),
        ),
    ]
