# Generated by Django 4.0.4 on 2022-06-17 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profiles/user-default.png', null=True, upload_to='profiles/'),
        ),
    ]
