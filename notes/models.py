from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator



# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.TextField(max_length=40)
    like = models.ManyToManyField(User, related_name='related_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        '画像ファイル',
        validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg','pdf',''])]
    )
    GRADE = (
        (1,'B2'),
        (2,'B3'),
        (3,'B4'),
    )
    SUB = (
        (1,'数学系'),
        (2,'物理系'),
        (3,'化学系'),
        (4,'地球惑星科学系'),
        (5,'機械系'),
        (6,'電気電子系'),
        (7,'情報通信系'),
        (8,'システム制御系'),
        (9,'経営工学系'),
        (10,'材料系'),
        (11,'応用化学系'),
        (12,'数理・計算科学系'),
        (13,'情報工学系'),
        (14,'生命理工学系'),
        (15,'建築系'),
        (16,'土木・環境工学系'),
        (17,'融合理工系'),
        (18,'英語科目'),
        (19,'第二外国語'),
    )

    grade = models.IntegerField('学年',choices=GRADE)
    sub = models.IntegerField('教科',choices=SUB)
    look = models.IntegerField(default=0)
 
    

    def __str__(self):
       return self.title



class Connection(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username     


class Connection1(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following1', blank=True)

    def __str__(self):
        return self.user.username   




class Post1(models.Model):
    title1  = models.TextField(max_length=100)
    content1 = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day1 = models.TextField(max_length=40)
    
    created_at1 = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        '画像ファイル',
        validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg','pdf',''])]
    )
    SUB1 = (
        (1,'文系教養科目'),
        (2,'英語科目'),
        (4,'日本・日本文化科目'),
        (5,'教職科目'),
        (6,'広域教養科目'),
        (7,'数学系'),
        (8,'物理学系'),
        (9,'生命系'),
        (10,'宇宙地球科学系'),
        (11,'初年次理学院'),
        (12,'初年次工学院'),
        (13,'初年次物質理工学院'),
        (14,'初年次環境社会理工学院'),
        (15,'初年次情報理工学院'),
        (16,'初年次生命理工学院'),
        (17,'その他の科目'),
    )


    sub1 = models.IntegerField('教科',choices=SUB1)
    look1 = models.IntegerField(default=0)
    like1 = models.ManyToManyField(User, related_name='related_post1', blank=True)
    def __str__(self):
       return self.title1