from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from questions.forms import QuestionInputForm, CommentForm, AnswerInputForm
from tags.models import Tag
from .models import Question, Answer, Comment
from django.contrib.auth import get_user_model
from django.db.models import Count

from django.views import View
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.utils import timezone


# 特別にルートのアプリケーションのviewをquestionsに入れる。
class QuestionList(ListView):
    model = Question
    paginate_by = 10
    template_name = 'homes/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_nav'] = self.kwargs.get("home_nav")
        users = get_user_model().objects.all().order_by('-score')
        context['users'] = users
        context['user'] = self.request.user
        if not self.request.user.is_anonymous:
            i = 0
            for index, u in enumerate(users):
                if u == self.request.user:
                    i = index
                    break
            context['user_index'] = i + 1
        return context

    def get_queryset(self):
        queryset = None
        if self.kwargs.get("home_nav") != 'active':
            queryset = Question.objects.all().order_by('-created_at').annotate(replies=Count('answer'))
        else:
            queryset = Question.objects.all().order_by('-last_updated').annotate(replies=Count('answer'))
        return queryset


@method_decorator(login_required, name='dispatch')
class QuestionInput(FormView):
    template_name = 'questions/question_input.html'
    form_class = QuestionInputForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tags'] = Tag.objects.all()
        return ctx

    def form_valid(self, form):
        question_form = form.save(commit=False)
        question_form.starter = self.request.user
        question_form.save()
        question_form.tag.add(question_form.tag1)
        if question_form.tag2 is not None:
            question_form.tag.add(question_form.tag2)
        question_form.save()
        # 投稿したら1点入れる
        self.request.user.score += 1
        self.request.user.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class QuestionDetail(View):

    def get(self, request, *args, **kwargs):
        question_pk = self.kwargs.get("question_pk")
        question = Question.objects.get(pk=question_pk)
        session_key = 'viewed_topic_{}'.format(question_pk)
        if not request.session.get(session_key, False):
            question.views += 1  # 閲覧数
            question.save()
            request.session[session_key] = True

        return render(request, 'questions/question_detail.html', {
            'question': Question.objects.get(pk=self.kwargs.get("question_pk")),
            'comment_form': CommentForm(),
            'user': self.request.user
        })

    def post(self, request, *args, **kwargs):
        question_pk = self.kwargs.get("question_pk")
        question = Question.objects.get(pk=question_pk)

        # ベストアンサー関連のリクエスト
        if 'best' in request.POST:
            best_answer = Answer.objects.get(pk=request.POST["best"])
            best_answer.is_bestAnser = True
            question.has_bestAnser = True
            best_answer.save()
            question.save()
            user = best_answer.created_by
            user.score += 3
            user.save()
            return redirect('questions:question_detail', question_pk=question_pk)
        elif 'delbest' in request.POST:
            best_answer = Answer.objects.get(pk=request.POST["delbest"])
            best_answer.is_bestAnser = False
            question.has_bestAnser = False
            best_answer.save()
            question.save()
            return redirect('questions:question_detail', question_pk=question_pk)

        # 削除関連のリクエスト
        elif 'delete_question' in request.POST:
            del_question = Question.objects.get(pk=request.POST["delete_question"])
            del_question.delete()
            return redirect("home")
        elif 'delete_answer' in request.POST:
            del_answer = Answer.objects.get(pk=request.POST["delete_answer"])
            del_answer.delete()
            return redirect('questions:question_detail', question_pk=question_pk)
        elif 'delcomment' in request.POST:
            delcomment = Comment.objects.get(pk=request.POST["delcomment"])
            delcomment.delete()
            return redirect('questions:question_detail', question_pk=question_pk)

        # コメントのform
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                com_answer = Answer.objects.get(pk=request.POST["comment"])
                comment.answer = com_answer
                comment.created_by = request.user
                comment.save()
                com_answer.save()
            return redirect('questions:question_detail', question_pk=question_pk)


@method_decorator(login_required, name='dispatch')
class QuestionEdit(UpdateView):
    model = Question
    fields = ('subject', 'tag1', 'tag2', 'message',)
    template_name = 'questions/question_edit.html'
    pk_url_kwarg = 'question_pk'

    # 作った人のみアクセス可
    def get_object(self, *args, **kwargs):
        obj = super(QuestionEdit, self).get_object(*args, **kwargs)
        if not obj.starter == self.request.user:
            raise Http404
        return obj

    # 適切なpostだったらインスタンスを保存。
    def form_valid(self, form):
        question = form.save(commit=False)
        question.last_updated = timezone.now()
        question.tag.clear()
        question.tag.add(question.tag1)
        if question.tag2 is not None:
            question.tag.add(question.tag2)
        question.save()
        return redirect('questions:question_detail', question_pk=self.kwargs.get("question_pk"))


@method_decorator(login_required, name='dispatch')
class AnswerInput(FormView):
    template_name = 'questions/answer_input.html'
    form_class = AnswerInputForm

    def get_success_url(self):
        return reverse_lazy('questions:question_detail',
                            kwargs={'question_pk': self.kwargs.get("question_pk")})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['question'] = Question.objects.get(pk=self.kwargs.get("question_pk"))
        return ctx

    def form_valid(self, form):
        answer_form = form.save(commit=False)
        question = Question.objects.get(pk=self.kwargs.get("question_pk"))
        answer_form.question = question
        answer_form.created_by = self.request.user

        answer_form.save()
        question.save()

        self.request.user.score += 1
        self.request.user.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AnswerEdit(UpdateView):
    model = Answer
    fields = ('message',)
    template_name = 'questions/answer_edit.html'
    pk_url_kwarg = 'answer_pk'

    def get_object(self, *args, **kwargs):
        obj = super(AnswerEdit, self).get_object(*args, **kwargs)
        if not obj.created_by == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.updated_by = self.request.user
        answer.updated_at = timezone.now()
        answer.save()
        return redirect('questions:question_detail', question_pk=self.kwargs.get("question_pk"))


@method_decorator(login_required, name='dispatch')
class CommentEdit(UpdateView):
    model = Comment
    fields = ('message',)
    template_name = 'questions/comment_edit.html'
    pk_url_kwarg = 'comment_pk'

    def get_object(self, *args, **kwargs):
        obj = super(CommentEdit, self).get_object(*args, **kwargs)
        if not obj.created_by == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.updated_at = timezone.now()
        comment.save()
        return redirect('questions:question_detail', question_pk=self.kwargs.get("question_pk"))