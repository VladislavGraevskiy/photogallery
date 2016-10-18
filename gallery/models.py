from django.db import models
from loginer.models import User


class Picture(models.Model):
    class Meta():
        db_table = "picture"
    id = models.AutoField(primary_key=True)
    pictures = models.BinaryField(max_length=4621440)
    id_user = models.ForeignKey(User)
    date_of_add = models.DateTimeField(auto_now_add=True)
    name_of_picture = models.CharField(max_length=50)
    views = models.IntegerField(default=0)
    check = models.IntegerField(default=0)
    public = models.IntegerField(default=1)
    id_pictures = models.ForeignKey('self', null=True)
    picture_size = models.CharField(max_length=20,default='')

    def __str__(self):
        return self.name_of_picture


class Comment(models.Model):
    class Meta():
        db_table = "comments"

    id = models.AutoField(primary_key=True)
    comments = models.CharField(max_length=300)
    id_user = models.ForeignKey(User)
    id_picture = models.ForeignKey(Picture)
    date_of_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comments[:50]


class Likes(models.Model):
    class Meta():
        db_table = "likes"
    picture = models.ForeignKey(Picture,null=True)
    user = models.ForeignKey(User,null=True)




