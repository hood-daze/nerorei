from django.db import models
# markdown用
from django.utils.safestring import mark_safe
from markdown import markdown

from tags.models import Tag
from django.contrib.auth import get_user_model


# questionのモデル
class Question(models.Model):
    subject = models.CharField(max_length=20)
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # タグを削除できないようにProtectと指定している。
    tag1 = models.ForeignKey(Tag, on_delete=models.PROTECT,
                             verbose_name='タグ1', related_name='question_tag1')
    tag2 = models.ForeignKey(Tag, on_delete=models.SET_NULL, verbose_name='タグ2', related_name='question_tag2',
                             null=True,
                             blank=True)
    tag = models.ManyToManyField(Tag, related_name='question_tag', verbose_name='タグ全て', )

    starter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    views = models.PositiveIntegerField(default=0)
    has_bestAnser = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    # 回答数を簡単に得る
    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()


class Answer(models.Model):
    message = models.TextField(verbose_name="回答", max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    is_bestAnswer = models.BooleanField(default=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    message = models.TextField(verbose_name="コメント",  max_length=2000)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
