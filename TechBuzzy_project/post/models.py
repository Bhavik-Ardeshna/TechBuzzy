from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from groups.models import Groups


User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts",on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    message = models.TextField()
    group = models.ForeignKey(Groups,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering = ['-created_on']
        unique_together = ['user','message']