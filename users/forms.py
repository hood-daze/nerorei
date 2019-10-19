from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


class ProfileSettingForm(UserChangeForm):
    password = None
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'placeholder': '自己紹介を300文字以内で入力してください。'}
        ),
        max_length=300,
        required=False
    )
    # アイコンボタンの文字変える。imgを出す。
    icon = forms.ImageField(label='アイコン', required=False,
                            widget=forms.FileInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'icon', 'description']
