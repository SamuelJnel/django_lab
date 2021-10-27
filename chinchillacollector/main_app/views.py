from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3
from .models import Chinchilla, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'kittycollector5'


class ChinchillaCreate(LoginRequiredMixin, CreateView):
    model = Chinchilla
    fields = ['name', 'color', 'description', 'age']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChinchillaUpdate(LoginRequiredMixin, UpdateView):
    model = Chinchilla
    fields = ['name', 'color', 'description', 'age']

class ChinchillaDelete(LoginRequiredMixin, DeleteView):
     model = Chinchilla
     success_url ='/chinchillas/'
    

def home(request):
    return render(request, 'about.html')

def about(request):
    return render(request, 'about.html')

@login_required
def chinchillas_index(request):
    chinchillas = Chinchilla.objects.filter(user=request.user)
    return render(request,'chinchillas/index.html', { 'chinchillas': chinchillas })

def chinchillas_details(request, chinchilla_id):
    chinchilla = Chinchilla.objects.get(id=chinchilla_id)
    toys_chinchilla_doesnt_have = Toy.objects.exclude(id__in = chinchilla.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request,'chinchillas/details.html', { 'chinchilla': chinchilla, 'feeding_form': feeding_form, 'toys': toys_chinchilla_doesnt_have })

def add_feeding(request, chinchilla_id):
    form = FeedingForm(request.POST)
 
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.chinchilla_id= chinchilla_id
        new_feeding.save()
    return redirect('details', chinchilla_id=chinchilla_id)


def add_photo(request, chinchilla_id):
   
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, chinchilla_id=chinchilla_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('details', chinchilla_id=chinchilla_id)

def assoc_toy(request, chinchilla_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Chinchilla.objects.get(id=chinchilla_id).toys.add(toy_id)
  return redirect('details', chinchilla_id=chinchilla_id)

def unassoc_toy(request, chinchilla_id, toy_id):
  Chinchilla.objects.get(id=chinchilla_id).toys.remove(toy_id)
  return redirect('details', chinchilla_id=chinchilla_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)

    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)




class ToyList(ListView):
  model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'