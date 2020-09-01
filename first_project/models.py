from django.db import models

# Create your models here.
class Users(models.Model):
    useremail = models.EmailField(max_length=30, primary_key=True, verbose_name="이메일(아이디)")
    username = models.CharField(max_length=12,verbose_name="사용자 이름")
    password = models.CharField(max_length=12, verbose_name="비밀 번호")
    registered_dttm = models.DateField(auto_now_add=True, verbose_name="가입 시간")

    def __str__(self):
        return self.username

class Upload(models.Model):
    # type_choices = {('a','말티즈'), ('b','푸들'),('c','시츄')}
    # , choices = type_choices, null = True
    type = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    datetime = models.DateTimeField(null=True)
    gender = models.TextField()
    feature = models.TextField()
    phone = models.IntegerField()
    place = models.TextField()
    photo = models.FileField(blank=True)  #, upload_to="photo_%Y_%m_%d")