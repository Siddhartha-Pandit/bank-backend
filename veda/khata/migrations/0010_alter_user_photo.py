# Generated by Django 4.1.5 on 2024-01-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khata', '0009_alter_user_aadharimg_alter_user_panimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(null=True, upload_to='user_photos/'),
        ),
    ]
