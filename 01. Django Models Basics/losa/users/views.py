from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def test_func(request):
    return HttpResponse('Hello there boys and girls :)')


def show_all_users(request):
    all = User.objects.filter(name__startswith='A')
    payload = {'users': all, 'result': 'Emil'}

    return render(request, 'users/all-users.html', payload)