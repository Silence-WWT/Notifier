from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from NFBasic.forms import *
from NFBasic.models import *


def index(request):
    return render_to_response('index.html', {'request': request})


def detail(request):
    pass


@csrf_exempt
def notify(request):
    if request.method == 'POST':
        nf_form = NotificationForm(request.POST)
        if nf_form.is_valid():
            if request.user.is_authenticated():
                nf_data = nf_form.cleaned_data
                title = nf_data['title']
                content = nf_data['content']
                files = nf_data['file']
                grade = Grade.objects.filter(grade=nf_data['grade'])
                if not grade:
                    grade = Grade.objects.create(grade=nf_data['grade'])
                else:
                    grade = grade[0]
                user = request.user
                notification = Notification.objects.create(title=title, content=content, user=user, grade=grade,
                                                           file=files)
            else:
                return HttpResponse('user not exist!')
    else:
        nf_form = NotificationForm()
        return render_to_response('notify.html', {'nf_form': nf_form})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/Notifier/')
            else:
                error_message = 'wrong username or password!'
                return HttpResponseRedirect('/Notifier/')
        else:
            return HttpResponse('alksdjf')
    else:
        login_form = LoginForm()
        return render_to_response('login.html', {'login_form': login_form})


def user_logout(request):
    logout(request)
    return render_to_response('index.html', {})