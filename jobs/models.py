from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_position = models.CharField(max_length=30)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.job_position


class post(models.Model):
    job_position = models.CharField(max_length=30)
    experience_required = models.CharField(max_length=15, default='')
    date_posted = models.DateField()
    job_description = models.TextField()

    def __str__(self):
        return self.job_position

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_id = models.CharField(max_length=20, primary_key=True)
    company = models.CharField(max_length=30)
    posts = models.ManyToManyField(post)

    def __str__(self):
        return self.referral_id

class apply(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    job_referral = models.CharField(max_length=20)
    applied_company = models.CharField(max_length=30)
    applied_position = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=20, default='')
    desc = models.CharField(max_length=5000, default='')

    def __str__(self):
        return self.name