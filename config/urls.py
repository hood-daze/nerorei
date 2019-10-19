
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from questions import views

#実験用
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.QuestionList.as_view(), name='home'), # ホーム画面
    path('<str:home_nav>', views.QuestionList.as_view(), name='home_nav'), # ホーム画面ナビゲーション

    path('questions/', include('questions.urls')),
    path('tags/', include('tags.urls')),
    path('helps/', include('helps.urls')),

    path('users/', include('users.urls')),


    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]

#　開発用
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)