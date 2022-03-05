from asyncio import Task
from dataclasses import field, fields
from tkinter import FALSE
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView ,FormView
from django.urls import reverse_lazy
from home.models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView 

from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginView(LoginView):
    template_name = 'home/login.html'
    fields = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks') 


class registerPage(FormView):
    template_name = 'home/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') 

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)

        return super(registerPage,self).form_valid(form)

    def get(self, *args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(registerPage,self).get( *args, **kwargs)





class taskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''   
        if search_input :
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)  

        context['search_input'] = search_input

        return context


class taskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'home/task.html'

class taskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(taskCreate,self).form_valid(form)


class taskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields =  ['title','complete']
    success_url = reverse_lazy('tasks')

class taskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')





# Create your views here. 