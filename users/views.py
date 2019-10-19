from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, TemplateView, ListView

from questions.models import Question
from users.forms import ProfileSettingForm


@method_decorator(login_required, name='dispatch')
class ProfileSetting(UpdateView):
    model = get_user_model()
    form_class = ProfileSettingForm
    template_name = 'users/profile_setting.html'
    success_url = reverse_lazy('home')

    # 作った人のみアクセス化
    def get_object(self, *args, **kwargs):
        return get_user_model().objects.get(pk=self.request.user.pk)


@method_decorator(login_required, name='dispatch')
class LeaveConfirm(TemplateView):
    template_name = 'users/leave_confirm.html'

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        user.delete()
        return redirect("home")


@method_decorator(login_required, name='dispatch')
class ProfileDetail(ListView):
    model = Question
    paginate_by = 3
    template_name = 'users/profile_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_nav'] = self.kwargs.get("profile_nav")
        target_user = get_user_model().objects.get(pk=self.kwargs.get('user_pk'))
        if target_user in self.request.user.follow.all():
            is_follow = True
        else:
            is_follow = False
        context['target_user'] = target_user
        context['is_follow'] = is_follow
        return context

    def get_queryset(self):
        profile_nav = self.kwargs.get("profile_nav")
        queryset = None
        user = get_user_model().objects.get(pk=self.kwargs.get('user_pk'))
        if (profile_nav == 'question') or (profile_nav is None):
            queryset = Question.objects.filter(starter=user).order_by('-created_at').annotate(
                replies=Count('answer'))
        elif profile_nav == 'answer':
            queryset = Question.objects.filter(answer__created_by=user).order_by('-created_at').annotate(
                replies=Count('answer'))

        return queryset

    def post(self, request, *args, **kwargs):
        target_user = get_user_model().objects.get(pk=self.kwargs.get('user_pk'))
        if 'do_follow' in request.POST:
            request.user.follow.add(target_user)
            request.user.save()
            return self.get(request, *args, **kwargs)

        elif 'now_follow' in request.POST:
            request.user.follow.remove(target_user)
            request.user.save()
            return self.get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class Connection(TemplateView):
    template_name = 'users/connection.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = get_user_model().objects.get(pk=self.kwargs.get('user_pk'))
        context['target_user'] = target_user
        return context


class RankingList(ListView):
    model = get_user_model()
    paginate_by = 50
    template_name = 'users/ranking.html'

    def get_queryset(self):
        queryset = get_user_model().objects.all().order_by('-score')
        return queryset
