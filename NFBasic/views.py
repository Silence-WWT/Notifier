from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from NFBasic.forms import *
from NFBasic.models import *
from datetime import datetime


def index(request):
    recent_list = Notification.objects.all().order_by('modified_time').reverse()[:10]
    return render_to_response('index.html', {'user': request.user.username, 'recent_list': recent_list})


def detail(request, pid):
    notification = get_object_or_404(Notification, pk=pid)
    nf_list = list(Notification.objects.order_by('created_time').reverse())
    nf_index = nf_list.index(notification)
    if nf_index > 0:
        next_notification = nf_list[nf_index - 1]
    else:
        next_notification = None
    if nf_index < len(nf_list) - 1:
        last_notification = nf_list[nf_index + 1]
    else:
        last_notification = None
    context = {'request': request, 'notification': notification, 'next': next_notification, 'last': last_notification,
               'archive_dict_list': get_archive_dict_list(), 'grade_dict_list': get_grade_dict_list()}
    return render_to_response('detail.html', context)


def view(request, page=''):
    nf_list = list(Notification.objects.all().order_by('modified_time').reverse())
    return pageinate(request, nf_list, page)


def get_archive(request, time, page=''):
    archive_time = datetime(int(time[:4]), int(time[5:]), 1)
    archive_month = get_object_or_404(NotificationMonth, month=archive_time)
    nf_list = list(archive_month.notification_set.all().order_by('modified_time').reverse())
    if not nf_list:
        return Http404
    archive_month = archive_month.month.strftime('%Y-%m')
    return pageinate(request, nf_list, page, archive_month)


def get_archive_dict_list():
    archive_list = list(NotificationMonth.objects.all().order_by('month').reverse())
    archive_dict_list = []
    for month in archive_list:
        archive_dict_list.append({'month': month.month.strftime('%Y-%m'), 'num': month.notification_set.count()})
    return archive_dict_list


def get_grade(request, grade, page=''):
    grade = get_object_or_404(Grade, grade=grade)
    nf_list = list(grade.notification_set.all())
    if not nf_list:
        return Http404
    return pageinate(request, nf_list, page, grade=grade)


def get_grade_dict_list():
    grade_list = list(Grade.objects.all())
    grade_dict_list = []
    for grade in grade_list:
        if grade.notification_set.count():
            grade_dict_list.append({'grade': grade.grade, 'num': grade.notification_set.count()})
    return grade_dict_list


def pageinate(request, nf_list, page, archive_month=None, grade=None):
    try:
        page = int(page)
    except TypeError:
        page = 1
    pages = int((len(nf_list) + 10 - 1) / 10)
    if page > pages or page < 1:
        return HttpResponseRedirect('/views/')
    context = {'nf_list': nf_list, 'pages': pages,
               'archive_dict_list': get_archive_dict_list(), 'archive_month': archive_month,
               'grade_dict_list': get_grade_dict_list(), 'grade': grade}
    if pages > 1:
        context['nf_list'] = nf_list[(page-1)*10: page*10]
        context['page'] = page
        context['last_page'] = page - 1
        context['next_page'] = page + 1
        context['range'] = range(1, pages + 1)
    return render_to_response('notifications.html', context)


@csrf_exempt
def notify(request):
    if request.method == 'POST':
        nf_form = NotificationForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if nf_form.is_valid():
            if request.user.is_authenticated():
                nf_data = nf_form.cleaned_data
                title = nf_data['title']
                content = nf_data['content']
                grade = Grade.objects.filter(grade=nf_data['grade'])
                if not grade:
                    grade = Grade.objects.create(grade=nf_data['grade'])
                else:
                    grade = grade[0]
                created_time = datetime.now()
                created_time = datetime(created_time.year, created_time.month, 1)
                nf_month = NotificationMonth.objects.filter(month__exact=created_time)
                if not nf_month:
                    month = NotificationMonth.objects.create(month=created_time)
                else:
                    month = nf_month[0]
                user = request.user
                notification = Notification.objects.create(title=title, content=content, user=user, grade=grade,
                                                           month=month)
                if file_form.is_valid():
                    notification.file = request.FILES['file']
                    notification.save()
                return HttpResponse('notify successfully!')
            else:
                return HttpResponse('user not exist!')
        else:
            return HttpResponse('not valid!')
    else:
        nf_form = NotificationForm()
        file_form = FileForm()
        return render_to_response('notify.html', {'nf_form': nf_form, 'file_form': file_form})


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
                message = 'login successfully!'
                return render_to_response('redirect.html', {'message': message, 'request': request})
            else:
                message = 'Incorrect username or password!'
                return render_to_response('redirect.html', {'message': message})
        else:
            message = 'please input username and password!'
            return render_to_response('redirect.html', {'message': message})
    else:
        login_form = LoginForm()
        return render_to_response('login.html', {'login_form': login_form})


def user_logout(request):
    logout(request)
    message = 'logout successfully'
    return render_to_response('redirect.html', {'message': message})