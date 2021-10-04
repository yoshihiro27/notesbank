# Generated by Django 3.2.5 on 2021-08-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_alter_post_sub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post1',
            name='sub1',
            field=models.IntegerField(choices=[(1, '文系教養科目'), (2, '英語科目'), (4, '日本・日本文化科目'), (5, '教職科目'), (6, '広域教養科目'), (7, '数学系'), (8, '物理学系'), (9, '生命系'), (10, '宇宙地球科学系'), (11, '初年次理学院'), (12, '初年次工学院'), (13, '初年次物質理工学院'), (14, '初年次環境社会理工学院'), (15, '初年次情報理工学院'), (16, '初年次生命理工学院')], verbose_name='教科'),
        ),
    ]
