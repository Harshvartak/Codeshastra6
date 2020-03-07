from django.db import models
from account.models import Therapist
from account.models import *
from django.conf import settings

class Diary(models.Model):
    title=models.CharField(max_length=40)
    Addition=models.TextField()
    pub_date= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def summary(self):
        return self.Addition[:100]

    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Comment(models.Model):
    post = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    psychiatrist=models.ForeignKey(Therapist,on_delete=models.CASCADE,related_name='psych')

    def __str__(self):
        return str(self.author)+str(self.post)
