
from typing import Any
from django.views import generic
from .mixins import AdminRoleMixin
from .models import Article
from .forms import ArticleCreationForm

class InformationPanel(generic.ListView, AdminRoleMixin):

    model = Article
    template_name = 'info_panel.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['article_creation_form'] = ArticleCreationForm()
        context['is_admin'] = self.get_admin_role(self.request)
        return context

