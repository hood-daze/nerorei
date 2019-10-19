from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings.base import AUTH_USER_MODEL
from tags.models import Tag

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    description = models.CharField(verbose_name='自己紹介', max_length=300, blank=True, null=True)

    origin = models.ImageField(verbose_name='アイコン', upload_to='icon/', default='sugar.png')

    icon = ImageSpecField(source="origin",
                          processors=[ResizeToFill(250, 250)],
                          format='PNG'
                          )

    follow = models.ManyToManyField(AUTH_USER_MODEL, related_name='custom_user_follow')
    register_tag = models.ManyToManyField(Tag, related_name='custom_user_register_tag')
    score = models.IntegerField(verbose_name='スコア', default=0)
