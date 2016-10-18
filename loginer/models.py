from django.db import models

# Create your models here.


class User(models.Model):
    class Meta():
        db_table = "users"

    id_users = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    data_of_reg = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=50)
    nikname = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nikname

