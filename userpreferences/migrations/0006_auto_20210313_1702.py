# Generated by Django 2.2 on 2021-03-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0005_auto_20210312_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='profile_pic',
            field=models.ImageField(blank=True, default='Profile_Pic_1.png', null=True, upload_to=''),
        ),
    ]
