from re import template
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from .models import Artikel,Kategori
from .forms import ArtikelForms
# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        #request.session['is_operator'] = True
        return True
    else:
        return False

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Operator').exists():
        request.session['is_operator'] = 'operator'
    template_name = "back/dashboard.html"
    context = {
        'title':'dashboard'
    }
    return render(request, template_name, context)

@login_required
def artikel(request):
    template_name = "back/tabel_artikel.html"
    artikel = Artikel.objects.filter(nama = request.user)
    context = {
        'title':'tabel artikel',
        'artikel':artikel,
    }
    return render(request, template_name, context)

@login_required
def tambah_artikel(request):
    template_name = "back/tambah_artikel.html"
    kategory = Kategori.objects.all()

    if request.method == "POST":
        forms_artikel = ArtikelForms(request.POST)
        if forms_artikel.is_valid():
            print('valid')
            art = forms_artikel.save(commit=False)
            art.nama = request.user
            art.save()
        return redirect(artikel)
    else:
        forms_artikel = ArtikelForms()
    context = {
        'title': 'tambah_artikel',
        'kategory':kategory,
        'forms_artikel' : forms_artikel,
    }
    return render(request, template_name, context)

@login_required
def lihat_artikel(request, id):
    template_name = "back/lihat_artikel.html"
    artikel = Artikel.objects.get(id=id)
    print(artikel)
    context = {
        'title' : 'lihat artikel',
        'artikel' : artikel,
    }
    return render(request, template_name, context)

@login_required
def edit_artikel(request, id):
    template_name = "back/tambah_artikel.html"
    a = Artikel.objects.get(id=id)
    if request.method == "POST":
        forms_artikel = ArtikelForms(request.POST, instance=a)
        if forms_artikel.is_valid():
            print('valid')
            art = forms_artikel.save(commit=False)
            art.nama = request.user
            art.save()
        return redirect(artikel)
    else:
        forms_artikel = ArtikelForms(instance=a)
    
    context = {
        'title' : 'edit artikel',
        'artikel' : a,
        'forms_artikel' : forms_artikel
    }
    return render(request, template_name, context)

@login_required
def delete_artikel(request, id):
    Artikel.objects.get(id=id).delete()
    return redirect(artikel)

@login_required
@user_passes_test(is_operator)
def users(request):
    template_name = "back/tabel_users.html"
    list_user = User.objects.all()
    context = {
        'title':'tabel users',
        'list_user' : list_user
    }
    return render(request, template_name, context)

    """
    Retrieve, update or delete a code snippet.
    """
    try:
        Artikel = Artikel.objects.get(pk=pk)
    except Artikel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        Artikel = ArtikelSerializer(Artikel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        Artikel = ArtikelSerializer(Artikel, data=request.data)
        if Artikel.is_valid():
            Artikel.save()
            return Response(Artikel.data)
        return Response(Artikel.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Artikel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)