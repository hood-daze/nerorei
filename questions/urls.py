from django.urls import path

# 実験用
from django.views.generic import TemplateView
from . import views

app_name = 'questions'

urlpatterns = [
    path('input/', views.QuestionInput.as_view(), name='question_input'),  # 質問記入画面
    path('<int:question_pk>/', views.QuestionDetail.as_view(), name='question_detail'),  # 質問表示画面
    path('<int:question_pk>/edit/', views.QuestionEdit.as_view(), name='question_edit'),  # 質問編集画面

    path('<int:question_pk>/answer/input/', views.AnswerInput.as_view(), name='answer_input'),  # 答え表示
    path('<int:question_pk>/answer/<int:answer_pk>/edit/',
         views.AnswerEdit.as_view(), name='answer_edit'),  # 答え編集

    path('<int:question_pk>/answer/<int:answer_pk>/comment/<int:comment_pk>/edit/',
         views.CommentEdit.as_view(), name='comment_edit'),# コメント編集画面
]
