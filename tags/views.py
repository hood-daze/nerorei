from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from questions.models import Question
from tags.models import Tag


class TagListView(ListView):
    model = Tag
    template_name = 'tags/tag_list.html'


@method_decorator(login_required, name='dispatch')
class TagDetailView(ListView):
    model = Question
    paginate_by = 4
    template_name = 'tags/tag_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['tag'] = get_object_or_404(Tag, pk=self.kwargs.get('tag_pk'))
        context['tag_nav'] = self.kwargs.get("tag_nav")
        return context

    def get_queryset(self):
        queryset = None
        tag = get_object_or_404(Tag, pk=self.kwargs.get('tag_pk'))
        if self.kwargs.get("tag_nav") != 'active':
            queryset = Question.objects.filter(tag=tag).order_by('-created_at').annotate(replies=Count('answer'))
        else:
            queryset = Question.objects.filter(tag=tag).order_by('-last_updated').annotate(replies=Count('answer'))
        return queryset

    def post(self, request, *args, **kwargs):
        add = self.request.POST.get('addtag')
        delete = self.request.POST.get('deltag')
        request_user = self.request.user
        tag = get_object_or_404(Tag, pk=self.kwargs.get('tag_pk'))
        if add is not None:
            request_user.register_tag.add(tag)
            request_user.save()
            return self.get(request, *args, **kwargs)
        elif delete is not None:
            request_user.register_tag.remove(tag)
            request_user.save()
            return self.get(request, *args, **kwargs)