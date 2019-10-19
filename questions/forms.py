from django import forms
from .models import Question, Comment, Answer


class QuestionInputForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'tag1', 'tag2', 'message']


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
