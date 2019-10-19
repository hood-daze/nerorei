from django.urls import path
from . import views
# 実験用
from django.views.generic import TemplateView

app_name = 'users'

urlpatterns = [
    path('setting/profile/', views.ProfileSetting.as_view(), name='profile_setting'),  # プロフィール設定
    path('setting/leave-confirm/', views.LeaveConfirm.as_view(), name='leave_confirm'),  # 退会確認

    path('profile/<int:user_pk>', views.ProfileDetail.as_view(), name='profile_detail'),  # プロフィール詳細
    path('profile/<int:user_pk>/<str:profile_nav>/', views.ProfileDetail.as_view(),
         name='profile_nav'),

    path('<int:user_pk>/connection/', views.Connection.as_view(), name='connection'),

    path('ranking/', views.RankingList.as_view(), name='ranking_list'),
]
