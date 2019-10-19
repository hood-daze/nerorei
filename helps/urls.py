from django.urls import path

from helps.views import HelpView

app_name = 'helps'

urlpatterns = [
    path('', HelpView.as_view(), name='help'),
]
