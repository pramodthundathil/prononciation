from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AudioPrononciation(models.Model):
    word = models.CharField(max_length=1000)
    audio = models.FileField(upload_to="Audios")
    date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="blogpost", blank=True)
    user = models.ForeignKey(User, related_name="blogsave", null=True,blank=True, on_delete=models.CASCADE)
    sentimental_score = models.FloatField(default=0)

    def total_likes(self):
        return self.likes.count()

class Comments(models.Model):
    Audio = models.ForeignKey(AudioPrononciation,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True)

