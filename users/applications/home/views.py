import datetime

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse


from django.views.generic import (
    TemplateView,
)


class DateMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super(DateMixin, self).get_context_data(**kwargs)
        context["date"] = datetime.datetime.now
        return context

class homepage(LoginRequiredMixin,TemplateView):
    template_name = "home/index.html"
    login_url = reverse_lazy('users_app:user-login')
    
class HomeDate(DateMixin,TemplateView):
    template_name = "home/mixin.html"
