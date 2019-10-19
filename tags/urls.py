from django.urls import path
from . import views

# 実験用
from django.views.generic import TemplateView

app_name = 'tags'

urlpatterns = [
    path('', views.TagListView.as_view(), name='tag_list'),  # タグ一覧メニュー
    path('<int:tag_pk>/', views.TagDetailView.as_view(), name='tag_detail'),# タグ詳細
    path('<int:tag_pk>/<str:tag_nav>/', views.TagDetailView.as_view(), name='tag_nav'), # 詳細の中のナビゲーション部分
]
