from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,DeleteView,UpdateView
from .models import PnModel
from django.urls import reverse_lazy

# Create your views here.
class PnList(ListView):
    template_name = 'list.html'
    model = PnModel #表示したいモデルをmodels.pyから選択して、モデル名を入力

class PnDetail(DetailView):
    template_name = 'detail.html'
    model = PnModel 

class PnCreate(CreateView):
    template_name = 'create.html'
    model = PnModel
    fields = ('title','cat')
    success_url = reverse_lazy('list')

class PnDelete(DeleteView):
    template_name = 'delete.html'
    model = PnModel
    success_url = reverse_lazy('list')

class PnTest(ListView):
    template_name = 'test.html'
    model = PnModel