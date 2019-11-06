from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings.base import AUTH_USER_MODEL
from tags.models import Tag
import os
from django.conf import settings

class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    description = models.CharField(verbose_name='自己紹介', max_length=300, blank=True, null=True)

    icon = models.ImageField(verbose_name='アイコン', upload_to='icon/', default='momiji.png')


    follow = models.ManyToManyField(AUTH_USER_MODEL, related_name='custom_user_follow', blank=True)
    register_tag = models.ManyToManyField(Tag, related_name='custom_user_register_tag', blank=True)
    score = models.IntegerField(verbose_name='スコア', default=0)
