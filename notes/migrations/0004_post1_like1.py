# Generated by Django 3.2.5 on 2021-08-02 13:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0003_alter_post1_title1'),
    ]

    operations = [
        migrations.AddField(
            model_name='post1',
            name='like1',
            field=models.ManyToManyField(blank=True, related_name='related_post1', to=settings.AUTH_USER_MODEL),
        ),
    ]
