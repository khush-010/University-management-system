from django.db import models

# Create your models here.
class Users(models.Model):
    CHOICES = [
        ('S', 'Student'),
        ('F', 'Faculty'),
    ]
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=70)
    password=models.CharField(max_length=256)
    role=models.CharField(max_length=10,choices=CHOICES)
    is_active=models.BooleanField(default=True)
    otp=models.IntegerField(blank=True, null=True)

    


class Application(models.Model):
    CHOICES = [
        ('Online', 'Online'),
        ('On Campus', 'On-Campus'),
    ]
    STATUS = [
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
        ('Pending','Pending'),
    ]
    uni_name=models.CharField(max_length=70)
    prog_name=models.CharField(max_length=70)
    study_mode=models.CharField(max_length=10,choices=CHOICES)
    status=models.CharField(max_length=10,choices=STATUS,default='Pending')
    user_name=models.ForeignKey(Users, on_delete=models.CASCADE)