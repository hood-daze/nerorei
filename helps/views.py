from django.views.generic import TemplateView
from django.contrib.auth import get_user_model


class HelpView(TemplateView):
    template_name = 'helps/help.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx
