from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from questions.widgets import SuggestWidget
from .models import Question, Comment, Answer


class QuestionInputForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'tag', 'message']
        widgets = {
            'tag': SuggestWidget(attrs={'data-url': reverse_lazy('questions:api_tags_get')}),
        }

    def clean_tag(self):
        tag = self.cleaned_data['tag']
        if len(tag) > 5:
            raise ValidationError("タグが五つ以上設定されています。")
        return tag

# 返信フォーム
class AnswerInputForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['message']


# コメントフォーム
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

