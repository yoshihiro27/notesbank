# Generated by Django 3.2.5 on 2021-08-25 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_alter_post1_sub1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post1',
            old_name='title1',
            new_name='title',
        ),
    ]