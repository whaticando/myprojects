import json
import os
import random
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib import auth, messages
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfileForm, UserForm, EmailForm, PasswordForm
from .models import Ouser
# from django.contrib.auth import authenticate
from utils.random_code import Valid_code
from Myblog1 import settings


@csrf_exempt
def register_view(request):
    if request.is_ajax():
        form = UserForm(request.POST)
        response = {'user': None, "msg": None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")

            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            avatar_obj = request.FILES.get('avatar')
            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
            Ouser.objects.create_user(username=user, password=pwd, email=email, **extra)
        else:
            response["msg"] = form.errors
        return JsonResponse(response)

    form = UserForm()
    return render(request, 'account/signup.html', {"form": form})


# Create your views here.
# class register_view(View):
#     '''
#       注册功能
#     '''
#
#     def get(self, request):
#         user_form = UserForm()
#         return render(request, 'account/signup.html',locals())
#
#     def post(self, request):
#         if request.method == "POST":
#             user_form = UserForm(request.POST)
#             reg_response = {"user": None, "error_msg": None}
#             if user_form.is_valid():
#                 user = user_form.cleaned_data.get("user")
#                 pwd = user_form.cleaned_data.get('pwd')
#                 # re_pwd = user_form.cleaned_data.get('re_ped')
#                 email = user_form.cleaned_data.get('email')
#                 avatar = request.FILES.get('avatar')
#                 user_obj = Ouser.objects.create_user(username=user, password=pwd, email=email, avatar=avatar)
#                 reg_response['user'] = user_obj.username
#             else:
#                 reg_response['error_msg'] = user_form.errors
#             return HttpResponse(json.dumps(reg_response))

# email = request.POST.get('email')
# username = request.POST.get('username')
# pwd = request.POST.get('pwd')
# re_pwd = request.POST.get('re_pwd')
#
# register_judge_result = self.register_info_judge(email, username, pwd, re_pwd)
#
# if not register_judge_result['error_msg']:
#     Ouser.objects.create_user(email=email, username=username, password=pwd)
#     register_judge_result['pass'] = True
#     return HttpResponse(json.dumps(register_judge_result))
# else:
#     register_judge_result['pass'] = False
#     return HttpResponse(json.dumps(register_judge_result))
# else:
#     pc = '不要搞骚操作!'
#     return HttpResponse(pc)  # 爬虫非Ajax提交

# def register_info_judge(self, email, username, pwd, re_pwd):
#     register_result = {"pass": None, "error_msg": []}
#     auth_user = Ouser.objects.filter(username=username)
#     if auth_user:
#         register_result['error_msg'].append('user_error')
#     if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[a-zA-Z]{2,3}$', email):
#         register_result['error_msg'].append('email_error')
#     if not re.match(r"^(?![0-9]+$)(?![a-z]+$)(?![A-Z]+$)(?!([^(0-9a-zA-Z)])+$).{6,20}$", pwd):
#         register_result['error_msg'].append('pwd_error')
#     if pwd != re_pwd:
#         register_result['error_msg'].append('re_pwd_error')
#
#     # todo 暂时是电话的功能没有添加
#     # elif user_tel or not re.match(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$',
#     #                             tel):
#     #     register_val["error_msg"].append('tel_error')
#     return register_result


# class User_Register(View):
#     def post(self, request):
#         if request.is_ajax():
#             response = { "is_reg": True, "error_msg": None}
#             user = request.POST.get('username')
#
#             auth_user = Ouser.objects.filter(username=user)
#             # auth_email = Ouser.objects.filter(email=email)
#             if auth_user:
#                 response["error_msg"] = '昵称已经被注册'
#             # elif auth_email:
#             #     response['error_msg'] = '邮箱已经被注册'
#             else:
#                 response["is_reg"] = False
#             return HttpResponse(json.dumps(response))
#         else:
#             pc = '不要搞骚操作!'
#             return HttpResponse(json.dumps(pc))  # 爬虫非Ajax提交

class Login_view(View):
    '''
       登录功能
    '''

    def get(self, request):
        return render(request, "account/login.html")

    def post(self, request):
        if request.is_ajax():
            username = request.POST.get('user')
            pwd = request.POST.get('pwd')
            email = request.POST.get('email')
            valid_code = request.POST.get('valid_code')
            print(username, pwd)
            random_code_str = request.session.get("random_code_str")

            print("random_code_str:", random_code_str)

            login_response = {"user": None, "error_msg": ""}
            if valid_code.upper() == random_code_str.upper():
                auth_user = auth.authenticate(username=username, password=pwd, email=email)
                if auth_user:
                    login_response["user"] = auth_user.username
                    auth.login(request, auth_user)  # {"user_id":1} request.user传到数据库中的auth
                else:
                    login_response["error_msg"] = "用户名或密码错误!"
            else:
                login_response["error_msg"] = "验证码错误!"
            return HttpResponse(json.dumps(login_response))


def logout_view(req):
    # 清理cookie里保存username
    next_to = req.GET.get('next', '/')
    if next_to == '':
        next_to = '/'
    auth.logout(req)
    return redirect(next_to)


# todo 尝试添加到已经有的类
def get_valid_img(request):
    valid_code = Valid_code()
    data = valid_code.get_random_code(request)
    return HttpResponse(data)


def index(request):
    # username = request.user
    return render(request, 'index.html')


@login_required
def profile_view(request):
    return render(request, 'oauth/profile.html')


@login_required
@csrf_exempt
def change_profile_view(request):
    if request.is_ajax():
        response = {"user": None, "msg": None}
        avatar_obj = request.FILES.get('avatar')
        if avatar_obj is None:
            response["msg"] = "头像为空"
        else:
            avatar_path = os.path.join(settings.MEDIA_ROOT, "avatar", str(avatar_obj))
            with open(avatar_path, "wb") as f:
                for line in avatar_obj:
                    f.write(line)  # pk 是主键的意思 primary key的缩写
            Ouser.objects.filter(pk=request.user.pk).update(avatar=avatar_path)
            response['user'] = request.user.username
        return JsonResponse(response)
    return render(request, 'oauth/change_profile.html', locals())


def change_pwd_view(request):
    if request.is_ajax():
        user = request.user
        response = {"user": None, "msg": None}
        form = PasswordForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data.get("pwd")
            Ouser.objects.filter(pk=user.pk).update(password=make_password(pwd))
            response["user"] = user.username
        else:
            response["msg"] = form.errors
        return JsonResponse(response)
    return render(request, "oauth/change_pwd.html", locals())


def change_email_view(request):
    if request.is_ajax():
        user = request.user
        response = {"user": None, "msg": None}
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            Ouser.objects.filter(pk=user.pk).update(email=email)
            response["user"] = user.username
        else:
            response["msg"] = form.errors
        return JsonResponse(response)
    return render(request, 'oauth/change_email.html', locals())
