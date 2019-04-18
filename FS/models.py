from django.db import models
from django.contrib.auth.models import User
#old_accuracy , feat_num , new_accuracy, new_features , new_ds
# Create your models here.
class FS(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE , blank = True)
    name = models.CharField(max_length=50)
    old_features = models.IntegerField()
    new_features = models.IntegerField()	
    old_accuracy = models.FloatField()
    new_accurcay = models.FloatField()
    csv = models.TextField()
    def __str__(self):
        return self.name


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User)

    email = models.EmailField(max_length=70)
    name = models.CharField(max_length = 50)
    surname = models.CharField(max_length = 50)

    def __str__(self):
        return self.user.username