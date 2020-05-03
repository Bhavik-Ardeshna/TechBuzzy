from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

from django import template
register = template.Library()


User = get_user_model()

class Groups(models.Model):
    name = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    members = models.ManyToManyField(User,related_name='mem',through='GroupMember')

    def __str__(self):
        return self.name

    # Here override save in midel.Model
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Metal:
        ordering = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Groups,related_name='membership',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')