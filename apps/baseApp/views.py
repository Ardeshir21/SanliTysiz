from django.shortcuts import render
from django.views import generic


# Index View
class IndexView(generic.TemplateView):
    template_name = 'baseApp/index.html'
